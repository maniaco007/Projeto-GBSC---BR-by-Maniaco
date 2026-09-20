# Manual de Uso — GBS-Control PT-BR

Este manual explica **todos os recursos** da versão PT-BR do GBS-Control (firmware do upscaler GBS com chip Tvia Trueview5725), mantida por **Maniaco Game Room**.

> Ainda não instalou o firmware? Veja primeiro o [Tutorial de Instalação](TUTORIAL_INSTALACAO.md).

---

## 1. Como acessar

Existem duas formas de controlar a GBS:

| Forma | Como |
| --- | --- |
| **Interface web (webui)** | No celular ou computador, abra o navegador e digite o endereço da GBS: `http://gbscontrol.local` ou o IP dela (ex.: `http://192.168.0.70`). O aparelho e a GBS precisam estar na **mesma rede Wi-Fi**. |
| **Menu OLED** | A telinha do aparelho (se sua GBS tiver o display instalado), controlada pelos botões / encoder físico. |

**Primeira vez, sem Wi-Fi configurado:** a GBS cria uma rede própria chamada `gbscontrol`. Conecte o celular nela e abra `http://192.168.4.1`. Depois vá em **Sistema → Wi-Fi** para ligar a GBS na sua rede de casa (veja a seção 8).

**Dica:** a webui detecta o idioma do navegador. Você pode trocar o idioma e o tema a qualquer momento em **Configurações** (seções 6.1 e 6.2).

---

## 2. Visão geral da tela

No topo ficam o logo e as **5 abas**:

| Ícone | Aba | Para que serve |
| --- | --- | --- |
| Entrada | **Perfis / Resolução** | Escolher a resolução de saída e carregar/salvar perfis |
| Setas | **Controles** | Ganho ADC e posição/escala da imagem |
| Grade | **Filtros** | Scanlines e filtros de imagem |
| Ajustes | **Configurações** | Idioma, tema, comportamento da GBS |
| Raio | **Sistema** | Wi-Fi, backup, atualização, reinício |

Existe ainda uma aba extra **Developer**, que só aparece com o *Modo Desenvolvedor* ligado (para depuração; a maioria das pessoas nunca precisa dela).

---

## 3. Aba Perfis / Resolução

### 3.1 Resolução de saída

Escolha uma das predefinições: **1920×1080, 1280×1024, 1280×960, 1280×720, 480p/576p**. A resolução escolhida também vira a de inicialização.

- **15KHz** — saída em 15 kHz (para monitores/TVs CRT que aceitam).
- **Passagem** (pass-through) — repassa o sinal sem escalar.

O botão da resolução ativa mostra o LED aceso na cor de destaque do tema.

### 3.2 Perfis (presets)

Um **perfil** guarda a configuração completa que você deixou boa para um console: resolução, filtros, scanlines, ganho, etc. O aparelho guarda até **72 perfis**.

Cada card de perfil mostra:
- o **nome** do perfil;
- a **origem de vídeo** (SCART, VGA, Componente ou RGBS);
- a **arte do console** ao fundo (o ícone que você escolheu).

**Botões abaixo dos cards:**

| Botão | Ação |
| --- | --- |
| **Carregar perfil** | Aplica o perfil selecionado |
| **Salvar perfil** | Grava as configurações atuais no slot selecionado |
| **Apagar perfil** | Remove o perfil selecionado (os seguintes sobem uma posição) |

#### Como criar um perfil novo

1. Deixe a imagem do console do jeito que você quer (resolução, filtros, ganho...).
2. Toque no card **Vazio** (é sempre o último da lista).
3. Toque em **Salvar perfil**.
4. Digite o **nome** (ex.: "Super Nintendo").
5. Escolha a **origem de vídeo**: SCART, VGA, Componente ou RGBS.
6. Toque **OK**, escolha o **ícone** do console (56 opções) e toque **OK** de novo.

Pronto: o perfil aparece na lista, em ordem alfabética.

#### Para sobrescrever um perfil existente
Toque no card dele e em **Salvar perfil** — o nome, o conector e o ícone são propostos de novo para você conferir.

#### Várias páginas e busca

- A lista mostra **quantos perfis couberem na tela** de uma vez (mais em telas altas). Passou disso, aparecem **setas ◀ ▶** e **bolinhas** de página; também dá pra **deslizar o dedo** para o lado.
- Ao abrir a tela, ela já vai para a página do perfil ativo.
- O card **Vazio** sempre existe: se a página encher, ele vai para a página seguinte.
- Com **mais de 12 perfis**, aparece o campo **Buscar perfil** (ignora acentos e maiúsculas).
- Embaixo aparece o contador **Perfis salvos: N/72**.

#### Origem de vídeo (SCART / VGA / Componente / RGBS)
É só uma **etiqueta informativa** que ajuda você a saber qual cabo/entrada usar com aquele perfil. Ela é mostrada no card e não muda o comportamento da imagem.

#### Ícones de console
Há **56 ícones** com arte real: controles, logos e gabinetes de Nintendo (NES, Famicom, SNES, N64, GameCube, Wii, Game Boy Advance/Micro), Sega (Master System, Mega Drive/Genesis, Saturn, Dreamcast, Sega CD), NEC/PC Engine, SNK Neo Geo, Sony (PS1, PS2, PS3, PSP), Microsoft (Xbox, Xbox 360), Atari, Philips (Odyssey, CD-i), 3DO e outros. Toque num ícone para selecioná-lo (ele destaca) e confirme em **OK**.

---

## 4. Aba Controles

### 4.1 Ganho ADC (brilho)

Controla o quanto a GBS "amplifica" o sinal de entrada — em prática, o **brilho/contraste** da imagem.

- **ganho −/+** — ajusta o ganho do perfil carregado (segure o botão para repetir).
- **Ganho Auto** — a GBS aumenta o ganho até as áreas claras virarem branco e recua quando detecta estouro. Para calibrar, deixe uma **tela branca** por alguns segundos.

### 4.2 Controles de Imagem

Setas para ajustar a imagem na tela, com três modos:

| Modo | O que move |
| --- | --- |
| **mover** | Posição da imagem (esquerda, direita, cima, baixo) |
| **escalar** | Tamanho da imagem |
| **bordas** | Recorte/bordas da imagem |

---

## 5. Aba Filtros

| Botão | Efeito |
| --- | --- |
| **scanlines** | Liga as linhas de varredura estilo CRT. Só funciona com fontes 240p, ou 480i com desentrelaçamento Bob |
| **intensidade** | Força das scanlines |
| **filtro de linha** | Elimina artefatos de pixels quadriculados ao escalar acima de 480p (recomendado) |
| **realce** | Aumenta o contraste em transições horizontais de brilho (recomendado) |
| **resposta de degrau** | Aumenta a nitidez das transições horizontais de cor (recomendado) |

---

## 6. Aba Configurações

### 6.1 Idioma / Language
**Português (BR)** ou **English**. Se você nunca escolheu, a página abre em inglês quando o navegador não estiver em português. A escolha fica salva no navegador. *(O menu OLED continua em português.)*

### 6.2 Tema
Troca **apenas as cores de destaque** da interface. Temas: **Padrão** (ciano + âmbar), **Verde Fósforo**, **Synthwave**, **Âmbar CRT**, **Rubi Famicom** e **Roxo GameCube**. Fica salvo no navegador.

### 6.3 Comportamento da imagem

| Opção | O que faz |
| --- | --- |
| **Perfis Combinados** | Se ativo, usa 1280×960 para NTSC 60 Hz e 1280×1024 para PAL 50 Hz (não vale para 720p/1080p) |
| **Altura Total** | Alguns perfis não usam toda a altura da saída (deixam linhas pretas); com esta opção eles preenchem mais a tela (hoje só afeta 1920×1080) |
| **Baixa Res: Usar Upscaling** | Fontes de baixa resolução (≤ 640×480) podem ser repassadas direto ou escaladas. Upscale é mais compatível com telas, mas pode ter problemas de borda |
| **Saída RGBHV/Componente** | Escolhe a saída: RGBHV (padrão, ideal para cabo VGA ou conversores HDMI) ou YPbPr experimental |
| **Taxa de Quadros: Forçar PAL 50 Hz para 60 Hz** | Para TVs que não aceitam 50 Hz. A imagem fica menos fluida. Requer reinício |
| **Desabilitar Gerador de Clock Externo** | Desliga o gerador de clock externo, se instalado. Requer reinício |
| **Calibração ADC** | Calibra os offsets do ADC ao ligar. Desative se notar desvio de cor |
| **Trava de FrameTime** | Mantém entrada e saída alinhadas (corrige a linha de "tearing"). Dois métodos: use **Alternar Método de Trava** se a tela ficar preta ou deslocar |
| **Método de Desentrelaçamento** | **Adaptativo por Movimento** (remove o cintilar, com artefatos leves em movimento) ou **Bob** (sem lag, mas cintila; combina com scanlines) |
| **Salvar Filtros por Slot** | Se ativo, cada perfil lembra seus próprios filtros; se desativo, mantém os filtros atuais |

### 6.4 Recursos do OLED e do boot

| Opção | O que faz |
| --- | --- |
| **Visor OLED: Exibição** | Escolhe o que a tela OLED mostra quando há um perfil carregado: **Nome** ou **Ícone**. Vale também para o protetor de tela (veja a seção 7) |
| **Perfil de Inicialização** | Por padrão a GBS lembra o último perfil/resolução. Escolha um perfil aqui para **sempre carregá-lo ao ligar** |

### 6.5 Modo Desenvolvedor
Habilita a aba **Developer** com ferramentas de depuração (console, timings, HTotal etc.). Uso avançado.

---

## 7. Menu OLED

O menu da telinha tem estas entradas:

| Entrada | Função |
| --- | --- |
| **OSD** | Liga/desliga o menu na tela da TV |
| **Resolução** | Lista de resoluções + rebaixar (15 kHz) + passagem |
| **Perfis** | Lista dos perfis salvos, em ordem alfabética; selecione para carregar |
| **Wi-Fi** | Mostra rede conectada, endereço `gbscontrol.local` e IP (ou os dados do modo Ponto de Acesso) |
| **Atual** | Tela de status: com perfil carregado mostra **nome ou ícone** do perfil; sem perfil, mostra a resolução |
| **Reset / Restaurar** | Reiniciar a GBS, restaurar padrões de fábrica, apagar o Wi-Fi salvo |

**Recursos da tela de status:**
- **Nomes longos** rolam automaticamente.
- **Aviso "Formato mudou"**: quando o preset ativo muda o formato, a tela mostra a nova resolução e a taxa por 3 segundos.
- **Protetor de tela** com dois modos (escolhidos em *Visor OLED: Exibição*):
  - **Nome:** o nome do perfil passeia pela tela; a fonte **diminui sozinha** para nomes compridos não serem cortados.
  - **Ícone:** o ícone do console do perfil aparece **animado** (uma animação de "quicar" gerada para 51 dos 56 ícones). Perfis cujo ícone não tem animação usam o protetor por nome.

---

## 8. Aba Sistema

### 8.1 Habilitar OTA
Liga o serviço de **atualização de firmware pelo Wi-Fi**. O programa *GBSC Updater* liga isso sozinho — você só precisa do botão manualmente se usar outra ferramenta. Ele desliga sozinho após reiniciar.

### 8.2 Reiniciar / Restaurar Padrões
- **Reiniciar:** reinicia a GBS.
- **Restaurar Padrões:** volta as configurações ao padrão de fábrica.

### 8.3 Cópia (backup)
- **Baixar:** baixa um arquivo com **todos os seus perfis e configurações**. Faça isso **antes de atualizar o firmware**.
- **Restaurar:** envia um arquivo de cópia de volta para a GBS.
- A cópia vale para **o mesmo aparelho**.

> **Isso é uma camada extra, não a única proteção.** O programa **GBSC Updater** (usado para atualizar o firmware) já faz esse mesmo backup **sozinho**, automaticamente, antes de gravar qualquer coisa — e cancela a atualização se o backup falhar. Ele também tem uma aba **Restaurar backup** que desfaz uma atualização com um clique (regrava o firmware anterior e reenvia os presets), sem você precisar ter guardado nada manualmente. Veja o [Tutorial de Instalação](TUTORIAL_INSTALACAO.md#voltar-para-a-versão-anterior).

### 8.4 Wi-Fi
- **Ponto de Acesso:** a GBS cria a própria rede (`gbscontrol`).
- **Estação:** a GBS entra na sua rede: toque em **Selecionar Rede**, escolha a rede, digite a senha em **Conectar à Rede** e toque **Conectar**. A GBS reinicia e passa a responder em `http://gbscontrol.local`.

---

## 9. Perguntas frequentes

**Meus perfis sumiram depois de atualizar.**
Se você usou o **GBSC Updater**, ele já fez um backup automático antes de gravar — abra o programa, aba **Restaurar backup**, escolha o backup da lista e clique em **Restaurar**. Se você tinha um backup manual (baixado pela webui), use **Cópia → Restaurar**. Se vinha do firmware original (que usava outro sistema de arquivos), a primeira inicialização formata a memória de dados — por isso essas duas camadas de backup existem.

**Atualizei e não gostei, dá pra voltar?**
Sim — é exatamente pra isso que serve a aba **Restaurar backup** do GBSC Updater: desfaz a atualização regravando o firmware anterior e reenviando seus presets, com um clique. Veja [Voltar para a versão anterior](TUTORIAL_INSTALACAO.md#voltar-para-a-versão-anterior) no tutorial de instalação.

**A página abriu em inglês.**
Vá em **Configurações → Idioma / Language → Português (BR)**.

**Não acho o IP da GBS.**
Veja no menu OLED → Wi-Fi, ou na lista de aparelhos do seu roteador, ou tente `http://gbscontrol.local`.

**A imagem ficou escura/clara demais.**
Aba Controles → ajuste o **ganho**, ou use **Ganho Auto** com uma tela branca.

**Onde vejo o que mudou nesta versão?**
No [Descritivo Detalhado](DESCRITIVO_DETALHADO.md).
