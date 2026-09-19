# GBSC Updater

Programa para gravar o firmware **GBS-Control PT-BR** na sua GBS. Você só informa o **IP** da GBS (ou a porta USB) — o firmware já vem embutido.

- **Aba "Atualizar por Wi-Fi (OTA)"** — GBS já com GBS-Control, na mesma rede.
- **Aba "Gravar por USB"** — primeira instalação, com cabo USB de dados.

Instruções para leigos: [`docs/TUTORIAL_INSTALACAO.md`](../../docs/TUTORIAL_INSTALACAO.md).

## Usando o Python (qualquer sistema)

```bash
pip install esptool
python gbsc_updater.py                              # abre a janela
python gbsc_updater.py --ota 192.168.0.70 firmware/GBSC-PTBR-v1.0.2.bin
python gbsc_updater.py --usb COM5 firmware/GBSC-PTBR-v1.0.2.bin
```

## Gerando o `.exe` (Windows)

```bat
pip install pyinstaller esptool
build_exe.bat
```

O resultado fica em `dist\GBSC-Updater.exe` (o firmware da pasta `firmware\` é embutido nele).

## Como funciona (OTA)

1. Chama `http://IP/sc?c` na GBS para ligar o serviço de OTA (equivale a *Sistema → Habilitar OTA*).
2. Envia um convite UDP para a porta 8266 com tamanho e MD5 do arquivo.
3. A GBS conecta de volta por TCP e o programa transmite o firmware, esperando a confirmação `OK`.

Como a GBS conecta de volta ao computador, o **Firewall do Windows** pode pedir permissão na primeira vez.

## Atualizando o firmware embutido

Copie o novo `.bin` (saída do PlatformIO: `.pio/build/d1_mini/firmware.bin`) para `firmware/` e gere o `.exe` de novo. O programa usa o arquivo `.bin` mais recente (ordem alfabética) dessa pasta.
