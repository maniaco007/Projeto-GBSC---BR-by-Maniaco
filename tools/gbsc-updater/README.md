# GBSC Updater

Programa para gravar o firmware **GBS-Control PT-BR** na sua GBS. Você só informa o **IP** da GBS (ou a porta USB) — o firmware já vem embutido.

- **Aba "Atualizar por Wi-Fi (OTA)"** — GBS já com GBS-Control, na mesma rede.
- **Aba "Gravar por USB"** — primeira instalação, com cabo USB de dados.
- **Aba "Restaurar backup"** — desfaz uma atualização com um clique (veja abaixo).

Instruções para leigos: [`docs/TUTORIAL_INSTALACAO.md`](../../docs/TUTORIAL_INSTALACAO.md).

## 🛡️ Segurança em primeiro lugar: backup automático + desfazer com um clique

Todo esse programa foi pensado em volta de uma ideia: **ninguém deveria perder os presets da sua GBS, ou ficar sem saída, por causa de uma atualização.** Por isso:

- **Antes de gravar qualquer firmware novo** (por Wi-Fi, ou por USB se você informar o IP), o programa baixa **sozinho** uma cópia completa dos seus presets e configurações — e, se achar no GitHub, também guarda o firmware que estava rodando. Isso fica salvo numa pasta `backups/` do lado do programa, com data e versão no nome.
- **Se o backup falhar, a gravação é cancelada.** O programa não segue "no escuro" — prefere parar e avisar a arriscar seus dados.
- **Não gostou da atualização, ou algo saiu errado?** Vá na aba **"Restaurar backup"**, escolha o backup da lista e clique em **Restaurar**: ele regrava o firmware de antes e reenvia todos os seus presets, do jeito que estavam. Você não precisa ter guardado nada manualmente — o programa já guardou pra você.

Isso é **além** do backup manual que a webui já oferece (Sistema → Cópia → Baixar) — pense nos dois como duas camadas da mesma proteção, não um substituindo o outro.

## Usando o Python (qualquer sistema)

```bash
pip install esptool
python gbsc_updater.py                              # abre a janela
python gbsc_updater.py --ota 192.168.0.70 firmware/GBSC-PTBR-v1.0.4.bin
python gbsc_updater.py --usb COM5 firmware/GBSC-PTBR-v1.0.4.bin
```

Os comandos `--ota`/`--usb` acima são o modo direto (sem janela, útil pra testes) e **não fazem** o backup automático — esse é um recurso da interface gráfica. Pra ter o backup, abra o programa sem argumentos e use os botões normalmente.

## Gerando o `.exe` (Windows)

```bat
pip install pyinstaller esptool
build_exe.bat
```

O resultado fica em `dist\GBSC-Updater.exe` (o firmware da pasta `firmware\` é embutido nele).

## Verificar atualização no GitHub

Na aba **"Atualizar por Wi-Fi"**, o botão **"Verificar atualização no GitHub"** consulta o release mais recente deste repositório, compara com a versão que a GBS informa estar rodando (`/gbs/version`) e, se houver algo novo, baixa o `.bin` sozinho e já deixa pronto pra você clicar em **Enviar / Gravar**. Não precisa ir atrás do arquivo manualmente.

## Como funciona (OTA)

1. Chama `http://IP/sc?c` na GBS para ligar o serviço de OTA (equivale a *Sistema → Habilitar OTA*).
2. Envia um convite UDP para a porta 8266 com tamanho e MD5 do arquivo.
3. A GBS conecta de volta por TCP e o programa transmite o firmware, esperando a confirmação `OK`.

Como a GBS conecta de volta ao computador, o **Firewall do Windows** pode pedir permissão na primeira vez.

## Como funciona (backup e restauração)

O backup usa os mesmos endpoints que a webui já expõe em Sistema → Cópia (`/spiffs/dir`, `/spiffs/download`, `/spiffs/upload`) — o programa só automatiza o processo e adiciona uma cópia do firmware anterior (baixada do GitHub pela tag da versão, quando existe um release publicado com aquela versão). Restaurar primeiro regrava o firmware salvo (se houver) e espera a GBS voltar, depois reenvia os dados — nessa ordem, porque regravar firmware reinicia o aparelho.

## Atualizando o firmware embutido

Copie o novo `.bin` (saída do PlatformIO: `.pio/build/d1_mini/firmware.bin`) para `firmware/` e gere o `.exe` de novo. O programa usa o `.bin` de versão mais alta dessa pasta (comparação numérica: `v1.0.10` é reconhecido como mais novo que `v1.0.9`, não por ordem alfabética).
