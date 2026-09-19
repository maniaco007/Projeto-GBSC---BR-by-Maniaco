# GBS-Control PT-BR by Maniaco — Documentação de Recursos

Atualizado em 18-09-2029.

## Visão Geral

Este projeto é uma tradução e evolução em PT-BR do firmware [GBS-Control](https://github.com/ramapcsx2/gbs-control) (upstream original), que roda num ESP8266 (D1 Mini) e controla o chip Tvia Trueview5725 (TV5725) — o "cérebro" de placas upscaler/linedoubler tipo GBS-8200/GBS-C, usadas pra converter vídeo analógico de consoles retrô (RGB/Componente) em VGA/HDMI com baixa latência.

**Repositório:** `github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco` (remote `origin-maniaco`), com o upstream original como remote `origin`.

**Branches:**

| Branch | Papel |
| --- | --- |
| `master` | Espelho do upstream original (inglês, sem modificações) |
| `ptbr-import` | Base "de produção": tradução completa PT-BR + logo próprio + presets embarcados |
| `feature-lab` | Onde os novos recursos (Tier 1/2 e além) estão sendo desenvolvidos e testados no aparelho real, antes de consolidar de volta em `ptbr-import` |

## Como Atualizar o Firmware (OTA)

Como não dá pra plugar o aparelho via USB no ambiente onde o código é gerado, toda atualização vai por Wi-Fi (OTA — Over-The-Air). Passo a passo:

1. A GBS precisa estar ligada e conectada na sua rede Wi-Fi.
2. Habilita o modo OTA no aparelho: `curl http://<ip-da-gbs>/sc?c` (ou acessando essa URL pelo navegador). Isso liga o receptor ArduinoOTA por um tempo limitado.
3. Envia o firmware novo: `pio run -e d1_mini -t upload --upload-port <ip-da-gbs>`.
4. O aparelho reinicia sozinho com o firmware novo (leva uns 10-15s).

O IP pode ser descoberto por `gbscontrol.local` (mDNS) quando a rede suporta, ou direto pelo roteador.

**Backup antes de mudanças arriscadas:** sempre que uma atualização mexe no sistema de arquivos (como a migração SPIFFS→LittleFS), é feito um backup completo antes (presets, `preferencesv2.txt`, `slots.bin`, `slot_icons.bin`) via `/spiffs/dir` + download de cada arquivo, do jeito que a própria webui espera pra restaurar.

## Novos Controles na Webui

Todos ficam nas abas **Preferências** e **Sistema**, com botões do tipo "segurar pra repetir" (mantém pressionado pra incrementar/decrementar rápido) onde faz sentido.

| Controle | Onde | O que faz |
| --- | --- | --- |
| Ajuste Fino de HTotal (++/--) | Developer | Trim manual do HTotal que agora é **persistido** e reaplicado automaticamente depois de carregar um preset fixo (antes se perdia a cada troca de preset) |
| Visor OLED: Preset Carregado | Preferências | Escolhe se a telinha do aparelho mostra o **nome** do preset customizado ativo ou um **ícone** genérico, no lugar da resolução — só aparece quando um preset customizado está carregado |

Todos esses valores são salvos em `/preferencesv2.txt` no aparelho (persistem entre reinicializações) e usam um sistema de debounce: mudanças rápidas (segurando o botão) só gravam no flash 800ms depois do último clique, pra não sobrecarregar o loop principal nem gerar falsos avisos de "wifi desconectado".

## Sistema de Perfis (Presets)

A aba **Perfis** da webui guarda até 72 slots customizados (A-Z, a-z, 0-9...), cada um com nome, ícone e a configuração completa de registradores do chip pra um console específico.

**Salvar um perfil:**
1. Ajusta a imagem do jeito que quer (filtros, scanlines, resolução etc) com o console conectado.
2. Escolhe um slot vazio ("Vazio") ou um já usado (sobrescreve).
3. Clica em **salvar perfil**, digita um nome (até 24 caracteres).
4. Escolhe a **origem de vídeo** (SCART, VGA, Componente ou RGBS) na grade logo abaixo do nome.
5. Escolhe um ícone na tela **"Escolha um ícone"** (clique só seleciona; confirma no botão OK, ou cancela pra manter o ícone atual/genérico).

**Carregar um perfil:** seleciona o slot na lista e clica em **carregar perfil**.

**Apagar um perfil:** seleciona o slot e clica em **apagar perfil** (pede confirmação — remove os arquivos do slot e desloca os seguintes pra cima).

**Seletor de ícone:** grade de ícones (hoje 25 opções, id 0-24) que ficam salvos em `/slot_icons.bin` (1 byte por slot). Esse mesmo id é o que conecta o ícone ao **protetor de tela animado do OLED** (ver seção abaixo) — hoje só o ícone do GameCube (id 9) tem arte real de animação, os outros usam símbolos genéricos abstratos na webui e não têm animação no OLED ainda.

**Origem de vídeo por preset:** escolha manual (não é detectada automaticamente — o chip só distingue "caminho RGB/RGBS" de "caminho Componente" a nível de registrador, não o conector físico) entre SCART, VGA, Componente ou RGBS, salva em `/slot_conn.bin` (1 byte por slot, 0 = não definido pra presets salvos antes dessa opção existir). Aparece no card do preset na lista, entre o nome e o ícone:

```
Super Nintendo
SCART
[ícone]
```

## Menu OLED do Aparelho

A telinha OLED (SSD1306 128x64) tem um menu navegado pelo encoder rotativo/botões físicos do aparelho:

- **Resolução:** escolhe entre as saídas fixas (1280x960, 1280x1024, 1280x720, 1920x1080, 480/576), downscale ou passthrough.
- **Perfis:** lista os presets customizados salvos (nome alinhado à esquerda; nomes maiores que a tela rolam automaticamente enquanto selecionados, igual já acontecia com SSID longo no menu de WiFi). Selecionar um carrega o preset na hora.
- **WiFi:** mostra SSID conectado, IP e o endereço `gbscontrol.local`.
- **Configuração Atual:** tela de status com resolução/taxa de quadros/tipo de entrada ao vivo.
- **Resetar/Restaurar:** reset do chip GBS, restaurar configurações de fábrica, resetar WiFi.

**Tela principal (quando ocioso):** por padrão mostra a resolução ativa, taxa de quadros e formato de entrada (RGB/YPbPr). Quando um **preset customizado** está carregado, passa a mostrar o **nome do preset** (ou um ícone genérico de controle, conforme a opção "Visor OLED: Preset Carregado" nas Preferências) no lugar da resolução. Sem preset customizado carregado, o texto de resolução continua exatamente como sempre foi.

## Protetor de Tela Animado ("GIF" por Preset)

Depois de 1 minuto sem uso, o OLED entra em modo protetor de tela. Se houver um preset customizado carregado **e** o ícone dele já tiver uma animação cadastrada, o protetor de tela mostra essa animação (vários quadros em sequência) em vez do texto padrão "GBS-Control" quicando pela tela. Sem preset customizado, ou ícone sem animação, continua o comportamento padrão. A posição continua trocando aleatoriamente a cada redesenho, pra não queimar pixel do OLED (mesma lógica de sempre).

O display é monocromático (1-bit) e não decodifica `.gif` de verdade — a "animação" é uma sequência de bitmaps XBM pré-convertidos e embutidos no firmware (mesma técnica já usada pro logo de boot).

**Como adicionar a animação de um console novo:**

1. Salva a imagem de origem em `assets_in/icons/` — pode ser um `.gif` animado (os quadros são extraídos automaticamente) ou uma imagem estática.
2. Adiciona uma entrada em `assets_in/icons/animations_manifest.json` com o `iconId` (tem que ser o mesmo número do ícone lá na webui), o caminho do arquivo e o tamanho desejado em pixels (ex: 32). Pra imagem estática sem animação pronta, dá pra usar `synthBounceFrames` pra gerar um efeito simples de "quicar" automaticamente.
3. Roda `python3 scripts/make_icon_animation.py`, que regenera `OLEDIconAnimations.cpp` com os quadros de todos os ícones do manifesto.
4. Recompila e manda o OTA — nenhum outro arquivo precisa ser tocado.

**Custo de flash:** bem baixo — essa primeira animação (infraestrutura + 4 quadros) usou cerca de 900 bytes dos ~322KB livres. Um ícone típico 32x32 com uns 8-10 quadros fica em torno de 1,3KB; pros ~24 consoles do projeto, isso daria uns 30-40KB no total — tranquilamente dentro do espaço disponível.

## Migração SPIFFS → LittleFS

O ESP8266 guarda os presets, preferências e ícones num sistema de arquivos dentro da memória flash. O firmware original usava SPIFFS, que está descontinuado no framework do ESP8266 (sem manutenção, mais lento e com mais risco de corromper dados). A migração trocou pra LittleFS — mais rápido e mais resistente a corrupção em quedas de energia.

**O que isso significa na prática:** os dois sistemas de arquivo não são compatíveis no formato bruto da flash, então a primeira vez que o firmware novo liga, ele formata a área de dados (apagando o que estava lá) e recomeça do zero.

Essa migração também foi a origem de um bug corrigido nesta rodada: um arquivo (`OLEDMenuImplementation.cpp`, responsável pelo menu físico do OLED) tinha ficado pra trás abrindo os presets pelo SPIFFS antigo, então a aba Perfis do menu OLED nunca encontrava nada, mesmo com presets salvos e visíveis na webui (que já usava LittleFS corretamente).

## Estado Atual e Pendências

- [x] Tradução completa da webui e menu OLED pra PT-BR
- [x] Logo de boot próprio
- [x] Migração SPIFFS → LittleFS
- [x] Seleção de ícone por preset na webui (56 ícones com arte real: controles, logos e gabinetes de console)
- [x] Menu OLED: aba Perfis funcionando, nome/ícone do preset ativo na tela principal, nomes longos rolando e alinhados à esquerda, fonte do protetor de tela (modo Nome) encolhe automaticamente pra não cortar nomes longos
- [x] Protetor de tela animado por preset modo ícone ou nome.
- [x] Aviso de mudança de formato no OLED por 3s — ideia do OSSC. (O "Link Perfil↔Entrada" foi implementado, mas só atuava junto com a Entrada Manual, removida depois; hoje o firmware apenas anota o último perfil por entrada, sem efeito.)
- [x] Origem de vídeo por preset (SCART/VGA/Componente/RGBS) escolhida ao salvar, mostrada no card do preset entre o nome e o ícone
- [ ] Ajuste de OFFSET (nível de preto) por canal ADC (R/G/B) — ideia do OSSC ainda não implementada; os registradores (`ADC_ROFCTRL`/`GOFCTRL`/`BOFCTRL`) já existem no código mas não são usados. Precisa investigar a interação com a rotina de auto-calibração antes de expor no menu/webui
- [x] Corrigido bug de mapeamento slot→letra: código passou a usar `slotIndexMap` (as 72 posições A-Z/a-z/0-9/símbolos) em vez da conta `'A' + índice`, que só funcionava certo pros primeiros 26 slots
