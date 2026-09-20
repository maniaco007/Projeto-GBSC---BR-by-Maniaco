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
import glob
import hashlib
import json
import os
import queue
import re
import socket
import sys
import tempfile
import threading
import urllib.request

APP_NAME = "GBSC Updater"
APP_VERSION = "1.0"
OTA_PORT = 8266
CHUNK = 1460
MIN_FW = 200 * 1024
MAX_FW = 1044464  # tamanho maximo de programa da D1 mini (layout 4m1m)
GITHUB_REPO = "maniaco007/Projeto-GBSC---BR-by-Maniaco"


class UpdateError(Exception):
    pass


def resource_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


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
    usb_tab.columnconfigure(1, weight=1)
    refresh_ports()

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
                    if value:
                        messagebox.showerror(APP_NAME, value)
                    else:
                        messagebox.showinfo(APP_NAME, "Tudo certo! A GBS vai reiniciar.")
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

    def start():
        if state["busy"]:
            return
        use_usb = notebook.index(notebook.select()) == 1
        ip = ip_var.get().strip()
        path = (usb_file if use_usb else ota_file).get().strip()
        if not use_usb and (not ip or ip.endswith(".")):
            messagebox.showwarning(APP_NAME, "Digite o IP completo da GBS.")
            return
        if use_usb and not messagebox.askyesno(
            APP_NAME,
            "Isso regrava o firmware pelo USB.\nFaca um backup dos seus perfis antes "
            "(webui > Sistema > Baixar). Continuar?",
        ):
            return
        state["busy"] = True
        cancel.clear()
        progress["value"] = 0
        send_btn.configure(state="disabled")
        # Cancelar so tem efeito de verdade no envio por Wi-Fi: a gravacao por
        # USB (esptool) e uma chamada bloqueante que, uma vez iniciada, nao da
        # pra interromper com seguranca. Por isso o botao fica desabilitado
        # nessa aba, em vez de dar a falsa impressao de que cancelar funciona.
        cancel_btn.configure(state="disabled" if use_usb else "normal")

        def work():
            error = ""
            try:
                if use_usb:
                    usb_flash(port_var.get(), path, erase_var.get(), log)
                else:
                    ota_upload(ip, path, log, lambda v: messages.put(("progress", v)), cancel)
            except UpdateError as exc:
                error = str(exc)
                log("ERRO: " + error)
            except Exception as exc:  # noqa: BLE001
                error = "Erro inesperado: %s" % exc
                log(error)
            messages.put(("done", error))

        threading.Thread(target=work, daemon=True).start()

    send_btn.configure(command=start)
    cancel_btn.configure(command=cancel.set)
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
