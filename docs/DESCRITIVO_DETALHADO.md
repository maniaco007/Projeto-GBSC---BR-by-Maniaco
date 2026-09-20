# Descritivo Detalhado — GBS-Control PT-BR

Registro completo do que foi feito nesta versão do firmware GBS-Control (chip Tvia Trueview5725, controlador ESP8266 / Wemos D1 mini), mantida por **Maniaco Game Room**. Está organizado por área, com o motivo técnico de cada decisão.

**Números finais (v1.0.4):** firmware de ~903 KB (86% do limite de 1.044.464 bytes), 56 ícones de console, 51 animações de protetor de tela, 72 slots de perfil, 6 temas de cor, 2 idiomas na webui.

---

## 1. Tradução e localização

- Toda a **webui** (5 abas, textos de ajuda, alertas e mensagens de erro) e o **menu OLED** foram traduzidos para PT-BR.
- **Logo de boot** próprio do projeto no lugar da tela de inicialização padrão.
- **Seletor de idioma (Português/English)** na webui: o inglês é aplicado sobre o texto em português por um dicionário de texto exato (~110 entradas), cobrindo todas as abas, alertas, o placeholder da senha e o rótulo "Vazio/Empty". Escolha salva no navegador; sem escolha prévia, abre em inglês se o navegador não estiver em português. Custo: cerca de 0,5% de flash. *O menu OLED segue apenas em português (os textos dele são bitmaps pré-desenhados).*

## 2. Base técnica

- **Migração SPIFFS → LittleFS** (formato atual do ESP8266). A primeira inicialização formata a área de dados — por isso o tutorial exige backup antes.
- **Correção do menu OLED que não achava presets**: um arquivo ainda abria os presets pelo SPIFFS antigo enquanto a webui já usava LittleFS.
- **Persistência de preferências**: o arquivo `/preferencesv2.txt` é sequencial (um byte por campo, sempre no fim), e cada campo tem um índice documentado. Novos campos foram apenas acrescentados, com valores padrão seguros para arquivos antigos.
- **Arquivos auxiliares por slot** (1 byte por slot, no mesmo padrão dos ícones): `slot_icons.bin`, `slot_conn.bin`, `slot_input.bin` — sem alterar o formato de `slots.bin`, para não quebrar backups existentes.

## 3. Sistema de perfis (presets)

| Recurso | Descrição |
| --- | --- |
| Até **72 slots** | Letras A–Z, a–z, números e símbolos (`slotIndexMap`) |
| **Origem de vídeo por preset** | SCART / VGA / Componente / RGBS, escolhida ao salvar e mostrada no card. É uma etiqueta informativa: o chip não distingue eletricamente SCART/VGA/RGBS |
| **Perfil de Inicialização** | Força um slot específico a carregar ao ligar |
| **Aviso "Formato mudou"** | O OLED mostra a nova resolução por 3 s quando o preset ativo muda de formato |
| Ordem alfabética | Tanto na webui quanto no menu OLED |
| Nomes com até 24 caracteres | O card quebra a linha; o OLED rola o texto |

## 4. Ícones de console

- O seletor cresceu de **25 desenhos genéricos** (só o GameCube tinha arte real) para **56 ícones com arte real**: controles, logos de marca e gabinetes.
- Cada imagem foi processada automaticamente: recorte no conteúdo (com margem), fundo transparente, ajuste para quadrado e redimensionamento para **40×40 px**, embutida no HTML (base64).
- **Contraste**: um fundo claro atrás de cada ícone garante a visibilidade de traços escuros no tema escuro.
- **Seleção com confirmação**: tocar num ícone apenas o destaca; a gravação só acontece em **OK** (antes o toque gravava direto e havia reinício do aparelho).

## 5. Protetor de tela e tela de status do OLED

- **Modo Nome**: o nome do preset passeia pela tela; a fonte **diminui automaticamente** entre 4 tamanhos (URW Gothic 20/14, DejaVu Mono 12/10) até caber, usando a largura medida do texto — corrige nomes como "Super Nintendo" perdendo a última letra.
- **Modo Ícone**: animação de "quicar" de 4 quadros (32×32, 1 bit) para **51 dos 56 ícones**. Conversão com **threshold adaptativo** (método de Otsu, com fallback por percentil para evitar imagens todas pretas/brancas) e **contorno automático de silhueta** (ícones claros, como o controle branco do Wii, não somem contra o fundo).
- 5 ícones (Wii, Saturn "linha", Sega CD "logo", PS1 Slim "logo" e um de linha) não reduzem bem para 1 bit e ficaram **sem animação** — esses presets usam o protetor por nome.
- Nome/ícone do preset ativo na tela principal; nomes longos rolam alinhados à esquerda.

## 6. Redesign da interface web

- **Cabeçalho novo** com logo, "by Maniaco Game Room" e as abas no topo em qualquer tamanho de tela.
- **Painéis** escuros com títulos em barra metálica, **botões táteis** e botões de resolução metálicos com **LED** (aceso na cor do tema quando ativo).
- **Cards de perfil** com a **arte do console ao fundo** (reaproveita os ícones já embutidos, sem custo de flash) e contorno neon no selecionado. O ícone pequeno do canto foi removido por ficar redundante.
- **Paginação adaptativa**: a quantidade de perfis por página é calculada pela altura visível (mais em telas altas), com setas, bolinhas clicáveis e **deslize do dedo**. O card "Vazio" sempre existe e passa para a página seguinte quando a atual enche.
- **Busca** de perfil (aparece com mais de 12 perfis; ignora acentos e maiúsculas).
- Contador **"Perfis salvos: N/72"**.
- **6 temas de cor** (só cores de destaque): Padrão, Verde Fósforo, Synthwave, Âmbar CRT, Rubi Famicom, Roxo GameCube. Baseados em variáveis CSS; escolha salva no navegador.
- Camada do modal corrigida (os cards não ficam mais por cima do diálogo de salvar).

## 7. Correções de bugs

| Bug | Causa | Correção |
| --- | --- | --- |
| Menu OLED não achava presets salvos | Lia o sistema de arquivos antigo (SPIFFS) | Unificado no LittleFS |
| Slots a partir do 27º quebravam | Letra do slot calculada como `'A' + índice` (válido só até 26) | Tabela de 72 caracteres em todos os pontos (webui e OLED, incluindo o Perfil de Inicialização) |
| Origem de vídeo não aparecia no card | 3 requisições paralelas excediam o limite de conexões simultâneas do ESP8266 (que já mantém um WebSocket aberto) e uma falhava em silêncio | Requisições sequenciadas, com nova tentativa |
| Aparelho reiniciava ao salvar preset com ícone | Variáveis grandes na pilha de um handler assíncrono (estouro de pilha) | Variáveis movidas para memória estática |
| Nomes longos cortados no protetor de tela | Fonte fixa | Fonte automática (item 5) |
| Ganho ADC "sem efeito" | O reset de fábrica do ADC era reaplicado a cada resync quando não havia preset customizado carregado | O ganho ajustado passa a ser restaurado após o reset |
| Console do modo Developer vazio | O firmware derruba o WebSocket quando a memória livre cai abaixo de 20 KB (limite do upstream) e esta versão fica em ~20–24 KB; além disso, dois buffers estáticos de 2,3 KB ocupavam RAM | Buffers movidos para o heap por requisição e limite de log reduzido para 11 KB (`WS_LOG_MIN_HEAP`) |
| Overflow horizontal do seletor no celular | O `<fieldset>` tem largura mínima implícita | `min-width: 0` + grid com `minmax(0, 1fr)` |
| Voltava para a página 1 ao escolher o slot vazio | O "pulo para a página do perfil ativo" disparava de novo quando o aparelho re-sincronizava o perfil ativo | O pulo só vale na abertura; depois de qualquer navegação/toque a página não muda sozinha |

## 8. Recursos implementados e depois removidos

Para manter o firmware enxuto e isolar um relato de comportamento estranho no ganho ADC, foram removidos (firmware, endpoints e interface):

- **Perfis de fábrica embarcados** (5 presets gravados no firmware e botão "importar perfis padrão");
- **Entrada Manual** (forçar RGB/RGBS ou Componente; a detecção automática continua);
- **Timer de Desligar**;
- **Realce de Scanlines** (ganho extra de luma com scanlines ativas);
- **Ganho ADC por canal (R/G/B)**.

O **Ganho ADC combinado (+/−)** e o **Ganho Automático** — recursos originais — foram mantidos e confirmados funcionando.

> **Nota sobre "Link Perfil ↔ Entrada":** essa automação (lembrar o último preset por entrada e recarregá-lo) só atuava junto com a Entrada Manual. Com a remoção dela, o firmware ainda anota o último perfil por entrada, mas **não o recarrega mais**. O recurso está, na prática, desativado.

Os bytes desses campos permanecem no arquivo de preferências (sem uso) para não deslocar os campos seguintes e não corromper configurações já salvas.

## 9. Ferramentas e distribuição

- **GBSC Updater** (`tools/gbsc-updater/`): programa para Windows (também roda em qualquer sistema com Python) com três abas — **Atualizar por Wi-Fi (OTA)**, em que basta informar o IP da GBS; **Gravar por USB** para a primeira instalação; e **Restaurar backup**, que desfaz uma atualização com um clique. Implementa o protocolo OTA do ESP8266 (convite UDP na porta 8266 + envio por TCP), liga o serviço OTA da GBS automaticamente, valida o arquivo (cabeçalho `0xE9` e tamanho) e trata o Firewall do Windows com novas tentativas automáticas. Tem também um botão que consulta o release mais recente no GitHub e baixa o `.bin` sozinho. Veja o [Tutorial](TUTORIAL_INSTALACAO.md) e a seção 12 (backup automático).
- **Documentação**: [Manual de Uso](MANUAL_DE_USO.md), [Tutorial de Instalação](TUTORIAL_INSTALACAO.md) e este descritivo.
- Pipeline de mídia reprodutível: `scripts/make_icon_animation.py` gera `OLEDIconAnimations.cpp` a partir de `assets_in/icons/animations_manifest.json`.

## 10. Pendências conhecidas

- **Offset (nível de preto) por canal ADC**: ideia mapeada (os registradores existem no código), sem uso ainda; precisa investigar a interação com a auto-calibração.
- Automação para switches SCART / vídeo componente.
- Menu OLED apenas em português.
- Código morto residual do "Link Perfil ↔ Entrada" (anotação do último perfil por entrada) pode ser removido numa limpeza futura.

## 11. Correções críticas — v1.0.3

Uma auditoria completa do firmware, da webui e das ferramentas de atualização encontrou e corrigiu cerca de 20 bugs. Os quatro abaixo foram validados na prática, em hardware real (não só por leitura de código ou compilação):

| Bug | Causa raiz | Correção |
| --- | --- | --- |
| **Menu OLED travava e reiniciava a GBS** com 17+ presets nomeados | O menu tenta listar todos os presets numa lista de no máximo 16 posições; faltava reservar espaço pro aviso de "muitos presets", então a 17ª entrada estourava o limite | O menu agora reserva a última posição pro aviso quando não cabem todos, em vez de tentar encaixar um item a mais |
| **A GBS não reconectava ao Wi-Fi sozinha** depois de uma queda de conexão | A supervisão de reconexão só existia na inicialização; depois de conectar uma vez, uma queda (roteador reiniciou, sinal caiu) deixava a GBS desconectada até um reboot manual | Detecção de queda + reconexão automática, incluindo retentativa periódica pra voltar do modo Ponto de Acesso quando a rede salva reaparece |
| **Apagar/salvar presets podia corromper dados** (nomes duplicados, contador errado) | Consequência do bug do menu OLED acima: um reinício no meio da gravação dos arquivos de preset deixava o índice de nomes (`slots.bin`) dessincronizado dos arquivos de dados reais | Corrigido na raiz (a causa do reinício); ver também seção 12 sobre a rede de segurança que cobre esse tipo de cenário daqui pra frente |
| **XSS na aba Wi-Fi da webui** | O nome de uma rede escaneada entrava direto no HTML da lista sem ser filtrado — uma rede com nome malicioso podia executar código na sessão da webui de quem escaneasse | Nome da rede escapado antes de entrar na página |

Lista completa das correções (menores, mas reais) nas [notas do release v1.0.3](https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/releases/tag/v1.0.3).

## 12. Segurança do processo de atualização (v1.0.3 / v1.0.4)

Depois de encontrar o bug do menu OLED acima — que reiniciava a GBS no pior momento possível, no meio de uma gravação de dados — ficou claro que "corrigir o bug" não bastava: o processo de atualizar o firmware em si precisava ser resistente a esse tipo de imprevisto. Três recursos novos, pensados juntos:

- **Checagem de atualização pelo GitHub**: a webui compara a versão da GBS (exposta em `/gbs/version`) com o release mais recente deste repositório e mostra um aviso quando há algo novo. O GBSC Updater tem o mesmo botão, que já baixa o `.bin` sozinho.
- **Alerta no visor OLED**: quando a webui encontra uma atualização, ela avisa a GBS (`/gbs/update-available`) pra acender um ícone de alerta piscando no menu e no protetor de tela — assim a pessoa não depende de estar olhando a webui no momento certo.
- **Backup automático + restauração de um clique no GBSC Updater**: antes de qualquer gravação, o programa baixa sozinho todos os presets/configurações da GBS (reaproveitando o mesmo formato e os mesmos endpoints do backup manual da webui, `/spiffs/dir` + `/spiffs/download` + `/spiffs/upload`) e, quando acha a versão atual publicada no GitHub, guarda também esse firmware. Se o backup falhar, a atualização é cancelada — o programa não segue adiante sem essa rede de segurança. A aba **Restaurar backup** faz o caminho inverso: regrava o firmware daquela época (se foi salvo) e reenvia os dados, nessa ordem (firmware primeiro, já que ele reinicia a GBS; dados depois).

A ideia por trás dos três: **ninguém deveria perder os presets da própria GBS, nem ficar sem um jeito fácil de voltar atrás, por causa de uma atualização** — nem quando o firmware novo tem um bug, nem quando a pessoa simplesmente prefere a versão anterior.

## 13. Verificação de integridade e licença

- **Checksums nos releases**: a partir da v1.0.4, cada release publicado inclui um `SHA256SUMS.txt` junto do `.bin`/`.exe`. Antes de gravar, é possível conferir (`Get-FileHash` no PowerShell, ou `sha256sum` no Linux/Mac) que o arquivo baixado é exatamente o publicado pelo autor, sem alteração de terceiros no caminho (mirror não oficial, download comprometido etc).
- **Licença**: o projeto é GPLv3, herdada do [gbs-control](https://github.com/ramapcsx2/gbs-control) original. Qualquer fork ou redistribuição — inclusive comercial — precisa manter a licença GPLv3, o código-fonte disponível a quem recebe o binário, e os créditos aos autores originais. A GPLv3 permite uso comercial, mas não permite fechar o código nem remover atribuição; ver [LICENSE](../LICENSE) e a seção "Licença e Atribuição" do [README](../README.md).
