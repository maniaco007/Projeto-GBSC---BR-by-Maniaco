#!/usr/bin/env python3
"""
GBSC Updater - grava o firmware GBS-Control PT-BR na sua GBS.

Duas formas de uso:
  1. Atualizar por Wi-Fi (OTA): a GBS ja esta rodando o GBS-Control e ligada na
     mesma rede. So informar o IP e escolher o arquivo do firmware.
  2. Gravar por USB: primeira instalacao (ou aparelho que nao liga mais o
     Wi-Fi). Liga a GBS no computador com um cabo USB.

Modo texto (sem janela), util para testes:
    python gbsc_updater.py --ota 192.168.0.70 firmware/GBSC-PTBR.bin
"""

import argparse
import datetime
import glob
import hashlib
import json
import os
import queue
import re
import socket
import struct
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

APP_NAME = "GBSC Updater"
APP_VERSION = "1.0"
OTA_PORT = 8266
CHUNK = 1460
MIN_FW = 200 * 1024
MAX_FW = 1044464  # tamanho maximo de programa da D1 mini (layout 4m1m)
GITHUB_REPO = "maniaco007/Projeto-GBSC---BR-by-Maniaco"
BACKUP_INFO_FILE = "info.json"
BACKUP_DATA_FILE = "data.bin"
BACKUP_FIRMWARE_FILE = "firmware.bin"


class UpdateError(Exception):
    pass


def resource_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def app_dir():
    """Onde o proprio executavel (ou script) mora - diferente de
    resource_dir(): num .exe onefile, resource_dir() aponta pra uma pasta
    temporaria (_MEIPASS) que e apagada quando o programa fecha, entao
    coisas que precisam sobreviver entre execucoes (backups) nao podem
    ir la."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def backups_dir():
    d = os.path.join(app_dir(), "backups")
    os.makedirs(d, exist_ok=True)
    return d


def list_backups():
    """Lista os backups salvos (mais recente primeiro), cada um como
    (pasta, info_dict)."""
    result = []
    for name in sorted(os.listdir(backups_dir()), reverse=True):
        folder = os.path.join(backups_dir(), name)
        info_path = os.path.join(folder, BACKUP_INFO_FILE)
        if os.path.isfile(info_path):
            try:
                with open(info_path, "r", encoding="utf-8") as f:
                    info = json.load(f)
            except Exception:  # noqa: BLE001
                continue
            result.append((folder, info))
    return result


_FIRMWARE_VERSION_RE = re.compile(r"[vV](\d+)\.(\d+)\.(\d+)")


def _firmware_sort_key(path):
    """Chave de ordenacao ciente de versao: extrai X.Y.Z do nome do arquivo
    (ex.: GBSC-PTBR-v1.0.10.bin) e ordena pela tupla numerica, para que
    v1.0.10 nao fique "menor" que v1.0.9 como aconteceria numa ordenacao
    puramente lexicografica. Nomes que nao batem com o padrao ficam sempre
    antes dos que batem (nunca viram "o mais novo" por engano) e, entre si,
    mantem o antigo desempate lexicografico."""
    match = _FIRMWARE_VERSION_RE.search(os.path.basename(path))
    if match:
        return (1, tuple(int(part) for part in match.groups()), path)
    return (0, (), path)


def bundled_firmware():
    files = sorted(
        glob.glob(os.path.join(resource_dir(), "firmware", "*.bin")),
        key=_firmware_sort_key,
    )
    return files[-1] if files else ""


def _parse_version(v):
    """Extrai os numeros de uma string de versao tipo 'v1.0.10' ou '1.0.10'
    para comparar numericamente - uma comparacao de texto colocaria
    "1.0.10" antes de "1.0.9"."""
    numbers = tuple(int(n) for n in re.findall(r"\d+", v or ""))
    return numbers or (0,)


def is_newer_version(remote, local):
    return _parse_version(remote) > _parse_version(local)


def fetch_latest_release_info():
    """Consulta a API do GitHub e retorna (tag, url_do_bin, nome_do_arquivo)
    do release mais recente publicado no repositorio do projeto."""
    url = "https://api.github.com/repos/%s/releases/latest" % GITHUB_REPO
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": APP_NAME}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
    except Exception as exc:  # noqa: BLE001
        raise UpdateError(
            "Nao consegui checar atualizacoes no GitHub (%s).\n"
            "Confira sua conexao com a internet." % exc
        )
    tag = data.get("tag_name", "")
    asset = next(
        (a for a in data.get("assets", []) if a.get("name", "").lower().endswith(".bin")),
        None,
    )
    if not tag or not asset:
        raise UpdateError("O release mais recente no GitHub nao tem um arquivo .bin anexado.")
    return tag, asset["browser_download_url"], asset["name"]


def fetch_device_version(ip):
    """Pergunta pra GBS qual firmware ela esta rodando (endpoint
    /gbs/version). Retorna string vazia se nao responder ou for um
    firmware antigo sem esse endpoint - tratado como "desconhecido" por
    quem chama, nao como erro."""
    try:
        with urllib.request.urlopen("http://%s/gbs/version" % ip, timeout=6) as resp:
            return json.load(resp).get("version", "")
    except Exception:  # noqa: BLE001
        return ""


def fetch_release_by_tag(tag):
    """Como fetch_latest_release_info(), mas pra uma tag especifica (ex.:
    'v1.0.2'). Retorna (url_do_bin, nome_do_arquivo) ou None se essa tag
    nao existir no GitHub ou nao tiver um .bin anexado - usado pra tentar
    guardar o firmware antigo junto do backup, e e opcional: se nao
    achar, o backup dos dados ainda acontece normalmente."""
    url = "https://api.github.com/repos/%s/releases/tags/%s" % (GITHUB_REPO, tag)
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": APP_NAME}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
    except Exception:  # noqa: BLE001
        return None
    asset = next(
        (a for a in data.get("assets", []) if a.get("name", "").lower().endswith(".bin")),
        None,
    )
    if not asset:
        return None
    return asset["browser_download_url"], asset["name"]


def _wait_online(ip, log, timeout=60):
    """Espera a GBS voltar a responder por HTTP depois de um reboot (pos
    gravacao). Nao levanta erro se o tempo esgotar - quem chama decide o
    que fazer (normalmente so avisar e seguir, ja que o reboot pode
    demorar mais numa rede lenta)."""
    log("Aguardando a GBS voltar (nao desligue) ...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen("http://%s/gbs/heap" % ip, timeout=3).read()
            log("GBS respondendo de novo.")
            return True
        except Exception:  # noqa: BLE001
            time.sleep(2)
    log("A GBS ainda nao respondeu apos %ds - pode estar demorando mais que o normal." % timeout)
    return False


def _multipart_upload(ip, filename, data, timeout=15):
    """POST bruto pro /spiffs/upload da GBS (mesmo endpoint que a webui
    usa pra restaurar arquivos), sem depender de nenhuma biblioteca alem
    da padrao do Python."""
    boundary = uuid.uuid4().hex
    body = (
        ('--%s\r\n' % boundary).encode()
        + ('Content-Disposition: form-data; name="file"; filename="%s"\r\n' % filename).encode()
        + b"Content-Type: application/octet-stream\r\n\r\n"
        + data
        + ("\r\n--%s--\r\n" % boundary).encode()
    )
    req = urllib.request.Request(
        "http://%s/spiffs/upload" % ip,
        data=body,
        headers={
            "Content-Type": "multipart/form-data; boundary=%s" % boundary,
            "Content-Length": str(len(body)),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        resp.read()


def backup_device(ip, dest_path, log, progress, cancel=None):
    """Baixa TODOS os arquivos do LittleFS da GBS e empacota num unico
    arquivo, no MESMO formato que a webui ja usa (Sistema > Copia >
    Baixar) - 4 bytes de tamanho (big-endian) + um JSON {caminho:
    tamanho} + o conteudo bruto de cada arquivo em seguida, na mesma
    ordem. Compativel com a tela de restauracao que ja existe na webui,
    e o formato que restore_device() espera."""
    try:
        with urllib.request.urlopen("http://%s/spiffs/dir" % ip, timeout=10) as resp:
            files = json.load(resp)
    except Exception as exc:  # noqa: BLE001
        raise UpdateError("Nao consegui listar os arquivos da GBS para o backup (%s)." % exc)

    total = len(files) or 1
    contents = []
    for i, path in enumerate(files):
        if cancel and cancel.is_set():
            raise UpdateError("Cancelado.")
        url = "http://%s/spiffs/download?file=%s" % (ip, urllib.parse.quote(path))
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                contents.append(resp.read())
        except Exception as exc:  # noqa: BLE001
            raise UpdateError("Falha ao baixar '%s' da GBS durante o backup (%s)." % (path, exc))
        progress((i + 1) / float(total))

    header_obj = {path: len(data) for path, data in zip(files, contents)}
    header_json = json.dumps(header_obj).encode("ascii")
    with open(dest_path, "wb") as f:
        f.write(struct.pack(">I", len(header_json)))
        f.write(header_json)
        for data in contents:
            f.write(data)
    log("Backup dos dados da GBS salvo (%d arquivos)." % len(files))


def restore_device(ip, backup_path, log, progress, cancel=None):
    """Le um arquivo no formato de backup_device()/da webui e reenvia
    cada arquivo pra GBS via /spiffs/upload."""
    with open(backup_path, "rb") as f:
        raw = f.read()
    if len(raw) < 6 or raw[4:6] != b'{"':
        raise UpdateError("Arquivo de backup invalido ou corrompido.")
    header_size = struct.unpack(">I", raw[0:4])[0]
    try:
        header_obj = json.loads(raw[4:4 + header_size].decode("ascii"))
    except Exception:  # noqa: BLE001
        raise UpdateError("Arquivo de backup invalido ou corrompido.")

    offset = 4 + header_size
    total = len(header_obj) or 1
    for i, (path, size) in enumerate(header_obj.items()):
        if cancel and cancel.is_set():
            raise UpdateError("Cancelado.")
        data = raw[offset:offset + size]
        offset += size
        try:
            _multipart_upload(ip, path.lstrip("/"), data)
        except Exception as exc:  # noqa: BLE001
            raise UpdateError("Falha ao restaurar '%s' na GBS (%s)." % (path, exc))
        progress((i + 1) / float(total))
    log("Dados restaurados na GBS (%d arquivos)." % len(header_obj))


def save_backup_snapshot(ip, log, progress, cancel=None):
    """Snapshot completo antes de atualizar: dados da GBS + (se achar no
    GitHub) o firmware que ela esta rodando agora, numa pasta com data e
    versao, pronta pra restaurar depois com restore_backup(). Levanta
    UpdateError se o backup dos dados falhar - a atualizacao nao deve
    prosseguir sem isso."""
    version = fetch_device_version(ip)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    folder_name = "%s_v%s" % (stamp, version) if version else stamp
    folder = os.path.join(backups_dir(), folder_name)
    os.makedirs(folder, exist_ok=True)

    def data_progress(v):
        progress(v * 0.7)

    backup_device(ip, os.path.join(folder, BACKUP_DATA_FILE), log, data_progress, cancel)

    has_firmware = False
    if version:
        found = fetch_release_by_tag("v%s" % version)
        if found:
            fw_url, fw_name = found
            log("Guardando tambem o firmware atual (%s) para poder desfazer depois ..." % fw_name)
            try:
                download_github_asset(
                    fw_url, os.path.join(folder, BACKUP_FIRMWARE_FILE), log,
                    lambda v: progress(0.7 + v * 0.3),
                )
                has_firmware = True
            except Exception as exc:  # noqa: BLE001
                log("Nao consegui baixar o firmware atual do GitHub (%s) - "
                    "o backup dos dados foi feito normalmente, so nao vai dar "
                    "pra reverter o firmware automaticamente depois." % exc)
    progress(1.0)

    info = {
        "ip": ip,
        "device_version": version,
        "timestamp": stamp,
        "has_firmware": has_firmware,
    }
    with open(os.path.join(folder, BACKUP_INFO_FILE), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    log("Backup completo em: %s" % folder)
    return folder


def restore_backup(ip, backup_folder, log, progress, cancel=None):
    """O oposto de save_backup_snapshot(): regrava o firmware que estava
    rodando na epoca do backup (se foi salvo) e depois reenvia os dados -
    nessa ordem, porque regravar o firmware reinicia a GBS e apaga
    qualquer estado em RAM, mas nao mexe no LittleFS."""
    info_path = os.path.join(backup_folder, BACKUP_INFO_FILE)
    if not os.path.isfile(info_path):
        raise UpdateError("Pasta de backup invalida (sem %s)." % BACKUP_INFO_FILE)
    with open(info_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    firmware_path = os.path.join(backup_folder, BACKUP_FIRMWARE_FILE)
    if info.get("has_firmware") and os.path.isfile(firmware_path):
        log("Regravando o firmware da epoca do backup (v%s) ..." % info.get("device_version", "?"))
        ota_upload(ip, firmware_path, log, lambda v: progress(v * 0.6), cancel)
        _wait_online(ip, log)
    else:
        log("Esse backup nao tem o firmware salvo - restaurando so os dados, "
            "por cima do firmware que estiver rodando agora na GBS.")

    log("Restaurando presets e configuracoes ...")
    restore_device(
        ip, os.path.join(backup_folder, BACKUP_DATA_FILE), log,
        lambda v: progress(0.6 + v * 0.4), cancel,
    )
    progress(1.0)
    log("Restauracao concluida!")


def download_github_asset(url, dest_path, log, progress):
    req = urllib.request.Request(url, headers={"User-Agent": APP_NAME})
    downloaded = 0
    with urllib.request.urlopen(req, timeout=30) as resp:
        total = int(resp.headers.get("Content-Length", 0)) or MAX_FW
        with open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                progress(min(downloaded / float(total), 1.0))
    if downloaded < MIN_FW:
        raise UpdateError("O download do GitHub veio incompleto ou invalido.")
    log("Baixado: %s (%d KB)" % (os.path.basename(dest_path), downloaded // 1024))


def check_firmware_file(path):
    if not path or not os.path.isfile(path):
        raise UpdateError("Escolha o arquivo do firmware (.bin).")
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        magic = f.read(1)
    if magic != b"\xe9" or size < MIN_FW or size > MAX_FW:
        raise UpdateError(
            "Esse arquivo nao parece ser um firmware valido para a GBS.\n"
            "Use o arquivo .bin do GBS-Control PT-BR (cerca de 900 KB)."
        )
    return size


def enable_ota_http(ip, log):
    """Pede pra GBS ligar o servico de OTA (mesmo que o botao 'Habilitar OTA' da webui)."""
    try:
        urllib.request.urlopen("http://%s/sc?c" % ip, timeout=6).read()
        log("Servico de atualizacao ligado na GBS.")
    except Exception as exc:  # noqa: BLE001
        raise UpdateError(
            "Nao consegui falar com a GBS em %s (%s).\n"
            "Confira o IP, se ela esta ligada e na mesma rede Wi-Fi que este computador." % (ip, exc)
        )


def ota_upload(ip, path, log, progress, cancel=None):
    size = check_firmware_file(path)
    with open(path, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()

    log("Verificando a GBS em %s ..." % ip)
    enable_ota_http(ip, log)

    log("ATENCAO: se o Windows abrir um aviso do Firewall, clique em 'Permitir acesso'.")
    conn = None
    server = None
    try:
        for attempt in range(1, 4):
            if cancel and cancel.is_set():
                raise UpdateError("Cancelado.")
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("", 0))
            server.listen(1)
            host_port = server.getsockname()[1]
            invite = ("0 %d %d %s\n" % (host_port, size, md5)).encode()
            log("Convidando a GBS para receber o firmware (tentativa %d de 3) ..." % attempt)
            accepted = False
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
                udp.settimeout(1.5)
                for _ in range(8):
                    if cancel and cancel.is_set():
                        raise UpdateError("Cancelado.")
                    udp.sendto(invite, (ip, OTA_PORT))
                    try:
                        answer = udp.recv(64).decode(errors="ignore")
                    except socket.timeout:
                        continue
                    if answer.startswith("OK"):
                        accepted = True
                        break
                    if answer.startswith("AUTH"):
                        raise UpdateError("Essa GBS pede senha de OTA, o que este programa nao suporta.")
            if not accepted:
                server.close()
                continue
            server.settimeout(25)
            try:
                conn, _addr = server.accept()
                break
            except socket.timeout:
                log("A GBS nao conseguiu se conectar de volta (Firewall?). Tentando de novo ...")
                server.close()
                continue
        if conn is None:
            raise UpdateError(
                "Nao consegui completar a conexao com a GBS.\n"
                "1) Confira o IP e se a GBS esta na mesma rede Wi-Fi.\n"
                "2) Se o Firewall do Windows perguntou algo, clique em 'Permitir acesso' "
                "(rede privada) e tente de novo.\n"
                "3) Se persistir, desligue e ligue a GBS."
            )

        log("Enviando o firmware (nao desligue a GBS) ...")
        sent = 0
        response = ""
        with open(path, "rb") as f:
            while True:
                if cancel and cancel.is_set():
                    raise UpdateError("Cancelado. A GBS continua com o firmware anterior.")
                chunk = f.read(CHUNK)
                if not chunk:
                    break
                conn.settimeout(15)
                conn.sendall(chunk)
                sent += len(chunk)
                progress(sent / float(size))
                try:
                    response += conn.recv(16).decode(errors="ignore")
                except socket.timeout:
                    raise UpdateError("A GBS parou de responder durante o envio.")

        log("Envio concluido. Aguardando a GBS confirmar ...")
        conn.settimeout(15)
        try:
            while "OK" not in response:
                data = conn.recv(32).decode(errors="ignore")
                if not data:
                    break
                response += data
        except socket.timeout:
            pass
        if "OK" not in response:
            raise UpdateError("A GBS nao confirmou a gravacao. Espere ela reiniciar e confira se atualizou.")
        progress(1.0)
        log("Pronto! A GBS vai reiniciar sozinha em instantes.")
    finally:
        # Garante que os sockets nunca vazem, mesmo se uma excecao nao prevista
        # (OSError, ConnectionResetError, etc.) sair de qualquer ponto acima.
        if conn is not None:
            conn.close()
        if server is not None:
            server.close()


def list_serial_ports():
    try:
        from serial.tools import list_ports

        return [p.device for p in list_ports.comports()]
    except Exception:  # noqa: BLE001
        return []


class _LogWriter:
    def __init__(self, log):
        self.log = log
        self.buf = ""

    def write(self, text):
        self.buf += text.replace("\r", "\n")
        while "\n" in self.buf:
            line, self.buf = self.buf.split("\n", 1)
            if line.strip():
                self.log(line.rstrip())

    def flush(self):
        pass


def usb_flash(port, path, erase, log):
    check_firmware_file(path)
    if not port:
        raise UpdateError("Escolha a porta USB (COM) da GBS.")
    import esptool

    writer = _LogWriter(log)
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = writer
    try:
        base = ["--chip", "esp8266", "--port", port, "--baud", "460800"]
        if erase:
            log("Apagando a memoria da GBS (isso apaga presets e Wi-Fi salvos) ...")
            esptool.main(base + ["erase-flash"])
        log("Gravando o firmware pelo cabo USB (NAO desconecte a GBS ate terminar) ...")
        esptool.main(base + ["write-flash", "0x0", path])
    except SystemExit as exc:
        if exc.code not in (0, None):
            raise UpdateError(
                "A gravacao por USB falhou.\n"
                "Confira o cabo (precisa ser de dados), o driver CH340 e se nenhum outro "
                "programa esta usando a porta."
            )
    finally:
        sys.stdout, sys.stderr = old_out, old_err
    log("Pronto! Desconecte e reconecte a GBS.")


def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("%s %s - GBS-Control PT-BR" % (APP_NAME, APP_VERSION))
    root.geometry("620x620")
    root.minsize(560, 560)

    messages = queue.Queue()
    cancel = threading.Event()
    state = {"busy": False}

    def log(msg):
        messages.put(("log", msg))

    fw_default = bundled_firmware()

    header = ttk.Label(
        root,
        text="GBS-Control PT-BR  -  Atualizador",
        font=("Segoe UI", 15, "bold"),
    )
    header.pack(pady=(12, 0))
    ttk.Label(root, text="by Maniaco Game Room", foreground="#666").pack()

    notebook = ttk.Notebook(root)
    notebook.pack(fill="x", padx=12, pady=10)

    # ---- aba OTA ----
    ota_tab = ttk.Frame(notebook, padding=12)
    notebook.add(ota_tab, text="  Atualizar por Wi-Fi  ")
    ttk.Label(
        ota_tab,
        text="1) Descubra o IP da GBS (aparece na tela OLED ou no roteador)\n"
        "2) Digite o IP abaixo\n3) Clique em Enviar",
        justify="left",
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
    ttk.Label(ota_tab, text="IP da GBS:").grid(row=1, column=0, sticky="w")
    ip_var = tk.StringVar(value="192.168.0.")
    ttk.Entry(ota_tab, textvariable=ip_var, width=24).grid(row=1, column=1, sticky="w", padx=6)
    ttk.Label(ota_tab, text="Firmware:").grid(row=2, column=0, sticky="w", pady=(8, 0))
    ota_file = tk.StringVar(value=fw_default)
    ttk.Entry(ota_tab, textvariable=ota_file, width=44).grid(row=2, column=1, sticky="we", padx=6, pady=(8, 0))

    def pick(var):
        chosen = filedialog.askopenfilename(
            title="Escolha o firmware (.bin)", filetypes=[("Firmware", "*.bin"), ("Todos", "*.*")]
        )
        if chosen:
            var.set(chosen)

    ttk.Button(ota_tab, text="Escolher...", command=lambda: pick(ota_file)).grid(row=2, column=2, pady=(8, 0))
    check_update_btn = ttk.Button(ota_tab, text="Verificar atualizacao no GitHub")
    check_update_btn.grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 0))
    ota_tab.columnconfigure(1, weight=1)

    # ---- aba USB ----
    usb_tab = ttk.Frame(notebook, padding=12)
    notebook.add(usb_tab, text="  Gravar por USB (primeira vez)  ")
    ttk.Label(
        usb_tab,
        text="Ligue a GBS no computador com um cabo USB de DADOS\n"
        "(ligada por USB na placa D1 mini), escolha a porta e clique em Gravar.",
        justify="left",
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
    ttk.Label(usb_tab, text="Porta (COM):").grid(row=1, column=0, sticky="w")
    port_var = tk.StringVar()
    port_box = ttk.Combobox(usb_tab, textvariable=port_var, width=22, state="readonly")
    port_box.grid(row=1, column=1, sticky="w", padx=6)

    def refresh_ports():
        ports = list_serial_ports()
        port_box["values"] = ports
        if ports and not port_var.get():
            port_var.set(ports[0])
        if not ports:
            port_var.set("")

    ttk.Button(usb_tab, text="Atualizar lista", command=refresh_ports).grid(row=1, column=2)
    ttk.Label(usb_tab, text="Firmware:").grid(row=2, column=0, sticky="w", pady=(8, 0))
    usb_file = tk.StringVar(value=fw_default)
    ttk.Entry(usb_tab, textvariable=usb_file, width=44).grid(row=2, column=1, sticky="we", padx=6, pady=(8, 0))
    ttk.Button(usb_tab, text="Escolher...", command=lambda: pick(usb_file)).grid(row=2, column=2, pady=(8, 0))
    erase_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(
        usb_tab,
        text="Apagar tudo antes (some com presets e Wi-Fi salvos - so se der problema)",
        variable=erase_var,
    ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(8, 0))
    ttk.Label(usb_tab, text="IP da GBS (opcional):").grid(row=4, column=0, sticky="w", pady=(8, 0))
    ttk.Entry(usb_tab, textvariable=ip_var, width=24).grid(row=4, column=1, sticky="w", padx=6, pady=(8, 0))
    ttk.Label(
        usb_tab,
        text="Se a GBS ainda responder pela rede, informe o IP pra fazer\n"
        "backup dos presets antes de gravar. Se o Wi-Fi parou de\n"
        "funcionar (por isso o USB), pode deixar em branco.",
        foreground="#888",
        justify="left",
    ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(2, 0))
    usb_tab.columnconfigure(1, weight=1)
    refresh_ports()

    # ---- aba Restaurar backup ----
    restore_tab = ttk.Frame(notebook, padding=12)
    notebook.add(restore_tab, text="  Restaurar backup  ")
    ttk.Label(
        restore_tab,
        text="Desfaz uma atualizacao: regrava o firmware de quando o backup\n"
        "foi feito (se foi salvo) e reenvia os presets e configuracoes.",
        justify="left",
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
    ttk.Label(restore_tab, text="IP da GBS:").grid(row=1, column=0, sticky="w")
    ttk.Entry(restore_tab, textvariable=ip_var, width=24).grid(row=1, column=1, sticky="w", padx=6)
    ttk.Label(restore_tab, text="Backup:").grid(row=2, column=0, sticky="nw", pady=(8, 0))
    backup_var = tk.StringVar()
    backup_box = ttk.Combobox(restore_tab, textvariable=backup_var, width=42, state="readonly")
    backup_box.grid(row=2, column=1, sticky="we", padx=6, pady=(8, 0))
    backup_paths = []

    def refresh_backups():
        backups = list_backups()
        backup_paths[:] = [folder for folder, _info in backups]
        labels = []
        for folder, info in backups:
            ts = info.get("timestamp", os.path.basename(folder))
            ver = info.get("device_version") or "?"
            fw_note = "com firmware" if info.get("has_firmware") else "so dados"
            labels.append("%s - v%s (%s)" % (ts, ver, fw_note))
        backup_box["values"] = labels
        if labels and not backup_var.get():
            backup_box.current(0)
        if not labels:
            backup_var.set("")

    ttk.Button(restore_tab, text="Atualizar lista", command=refresh_backups).grid(row=2, column=2, pady=(8, 0))

    def open_backups_folder():
        os.startfile(backups_dir())  # noqa: S606 - Windows-only tool, user-initiated

    ttk.Button(restore_tab, text="Abrir pasta de backups", command=open_backups_folder).grid(
        row=3, column=0, columnspan=3, sticky="w", pady=(8, 0)
    )
    restore_tab.columnconfigure(1, weight=1)
    refresh_backups()

    # ---- barra, botoes e log ----
    progress = ttk.Progressbar(root, maximum=100)
    progress.pack(fill="x", padx=12)
    buttons = ttk.Frame(root)
    buttons.pack(fill="x", padx=12, pady=8)
    send_btn = ttk.Button(buttons, text="Enviar / Gravar")
    send_btn.pack(side="left")
    cancel_btn = ttk.Button(buttons, text="Cancelar", state="disabled")
    cancel_btn.pack(side="left", padx=8)

    log_box = tk.Text(root, height=12, state="disabled", wrap="word", bg="#101010", fg="#d8d8d8")
    log_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def append_log(text):
        log_box.configure(state="normal")
        log_box.insert("end", text + "\n")
        log_box.see("end")
        log_box.configure(state="disabled")

    def pump():
        try:
            while True:
                kind, value = messages.get_nowait()
                if kind == "log":
                    append_log(value)
                elif kind == "progress":
                    progress["value"] = value * 100
                elif kind == "done":
                    state["busy"] = False
                    send_btn.configure(state="normal")
                    cancel_btn.configure(state="disabled")
                    on_tab_changed()
                    done_tab, error = value
                    if error:
                        messagebox.showerror(APP_NAME, error)
                    elif done_tab == TAB_RESTORE:
                        messagebox.showinfo(APP_NAME, "Restauracao concluida!")
                    else:
                        messagebox.showinfo(APP_NAME, "Tudo certo! A GBS vai reiniciar.")
                elif kind == "refresh_backups":
                    refresh_backups()
                elif kind == "update_check_error":
                    state["busy"] = False
                    check_update_btn.configure(state="normal")
                    messagebox.showerror(APP_NAME, value)
                elif kind == "update_check_result":
                    state["busy"] = False
                    check_update_btn.configure(state="normal")
                    tag, url, name, local_version = value
                    if local_version and not is_newer_version(tag, local_version):
                        messagebox.showinfo(
                            APP_NAME, "Voce ja esta na versao mais recente (%s)." % local_version
                        )
                        continue
                    msg = "Versao mais recente no GitHub: %s" % tag
                    msg += (
                        "\nVersao atual da GBS: %s" % local_version
                        if local_version
                        else "\n(nao consegui confirmar a versao atual da GBS - confira o IP)"
                    )
                    msg += "\n\nBaixar agora?"
                    if messagebox.askyesno(APP_NAME, msg):
                        dest = os.path.join(tempfile.gettempdir(), name)
                        state["busy"] = True
                        check_update_btn.configure(state="disabled")
                        progress["value"] = 0

                        def download_work(url=url, dest=dest):
                            derror = ""
                            try:
                                download_github_asset(
                                    url, dest, log, lambda v: messages.put(("progress", v))
                                )
                            except UpdateError as exc:
                                derror = str(exc)
                            except Exception as exc:  # noqa: BLE001
                                derror = "Erro inesperado: %s" % exc
                            messages.put(("update_downloaded", (dest, derror)))

                        threading.Thread(target=download_work, daemon=True).start()
                elif kind == "update_downloaded":
                    state["busy"] = False
                    check_update_btn.configure(state="normal")
                    dest, derror = value
                    if derror:
                        messagebox.showerror(APP_NAME, derror)
                    else:
                        ota_file.set(dest)
                        notebook.select(0)
                        messagebox.showinfo(
                            APP_NAME,
                            "Firmware baixado!\nClique em 'Enviar / Gravar' para atualizar a GBS agora.",
                        )
        except queue.Empty:
            pass
        root.after(100, pump)

    def check_for_update():
        if state["busy"]:
            return
        ip = ip_var.get().strip()
        state["busy"] = True
        check_update_btn.configure(state="disabled")

        def work():
            try:
                tag, url, name = fetch_latest_release_info()
            except UpdateError as exc:
                messages.put(("update_check_error", str(exc)))
                return
            except Exception as exc:  # noqa: BLE001
                messages.put(("update_check_error", "Erro inesperado: %s" % exc))
                return
            local_version = fetch_device_version(ip) if ip and not ip.endswith(".") else ""
            messages.put(("update_check_result", (tag, url, name, local_version)))

        threading.Thread(target=work, daemon=True).start()

    check_update_btn.configure(command=check_for_update)

    TAB_OTA, TAB_USB, TAB_RESTORE = 0, 1, 2
    BTN_LABELS = {TAB_OTA: "Enviar / Gravar", TAB_USB: "Enviar / Gravar", TAB_RESTORE: "Restaurar"}

    def on_tab_changed(_event=None):
        if not state["busy"]:
            send_btn.configure(text=BTN_LABELS.get(notebook.index(notebook.select()), "Enviar / Gravar"))

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    def start():
        if state["busy"]:
            return
        tab = notebook.index(notebook.select())
        ip = ip_var.get().strip()
        ip_ok = bool(ip) and not ip.endswith(".")
        backup_folder = None

        if tab == TAB_OTA and not ip_ok:
            messagebox.showwarning(APP_NAME, "Digite o IP completo da GBS.")
            return
        if tab == TAB_USB and not ip_ok and not messagebox.askyesno(
            APP_NAME,
            "Sem o IP da GBS nao da pra fazer backup dos presets antes de gravar "
            "(normal se o Wi-Fi parou de funcionar, por isso o USB).\n\n"
            "Continuar mesmo assim, sem backup?",
        ):
            return
        if tab == TAB_RESTORE:
            if not backup_paths or backup_box.current() < 0:
                messagebox.showwarning(APP_NAME, "Escolha um backup pra restaurar.")
                return
            if not ip_ok:
                messagebox.showwarning(APP_NAME, "Digite o IP completo da GBS.")
                return
            backup_folder = backup_paths[backup_box.current()]
            with open(os.path.join(backup_folder, BACKUP_INFO_FILE), encoding="utf-8") as f:
                info = json.load(f)
            warn = (
                "Isso vai SOBRESCREVER os presets e configuracoes atuais da GBS "
                "com os do backup de %s" % info.get("timestamp", "?")
            )
            if info.get("has_firmware"):
                warn += ", e regravar o firmware v%s por cima do atual" % info.get("device_version", "?")
            warn += ".\n\nContinuar?"
            if not messagebox.askyesno(APP_NAME, warn):
                return

        path = (usb_file if tab == TAB_USB else ota_file).get().strip()
        state["busy"] = True
        cancel.clear()
        progress["value"] = 0
        send_btn.configure(state="disabled")
        # Cancelar so tem efeito de verdade no envio por Wi-Fi (OTA/backup): a
        # gravacao por USB (esptool) e uma chamada bloqueante que, uma vez
        # iniciada, nao da pra interromper com seguranca. Por isso o botao
        # fica desabilitado nessa aba, em vez de dar a falsa impressao de que
        # cancelar funciona.
        cancel_btn.configure(state="disabled" if tab == TAB_USB else "normal")

        def work():
            error = ""
            made_backup = False
            try:
                if tab == TAB_OTA:
                    log("Fazendo backup dos dados da GBS antes de atualizar ...")
                    save_backup_snapshot(ip, log, lambda v: messages.put(("progress", v * 0.3)), cancel)
                    made_backup = True
                    messages.put(("progress", 0))
                    ota_upload(ip, path, log, lambda v: messages.put(("progress", v)), cancel)
                elif tab == TAB_USB:
                    if ip_ok:
                        log("Fazendo backup dos dados da GBS antes de gravar ...")
                        save_backup_snapshot(ip, log, lambda v: messages.put(("progress", v * 0.3)), cancel)
                        made_backup = True
                        messages.put(("progress", 0))
                    usb_flash(port_var.get(), path, erase_var.get(), log)
                else:
                    restore_backup(ip, backup_folder, log, lambda v: messages.put(("progress", v)), cancel)
            except UpdateError as exc:
                error = str(exc)
                log("ERRO: " + error)
            except Exception as exc:  # noqa: BLE001
                error = "Erro inesperado: %s" % exc
                log(error)
            messages.put(("done", (tab, error)))
            if made_backup:
                messages.put(("refresh_backups", None))

        threading.Thread(target=work, daemon=True).start()

    send_btn.configure(command=start)
    cancel_btn.configure(command=cancel.set)
    on_tab_changed()
    append_log("Pronto. Escolha uma aba, preencha os campos e clique em Enviar / Gravar.")
    if fw_default:
        append_log("Firmware incluido: " + os.path.basename(fw_default))
    pump()
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--ota", nargs=2, metavar=("IP", "ARQUIVO"), help="modo texto: envia por Wi-Fi")
    parser.add_argument("--usb", nargs=2, metavar=("PORTA", "ARQUIVO"), help="modo texto: grava por USB")
    args = parser.parse_args()
    try:
        if args.ota:
            ota_upload(args.ota[0], args.ota[1], print, lambda v: print("\r%3d%%" % int(v * 100), end=""))
        elif args.usb:
            usb_flash(args.usb[0], args.usb[1], False, print)
        else:
            run_gui()
    except UpdateError as exc:
        print("\nERRO:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
