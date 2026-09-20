<div align="center">
  <h1>🎮 GBS-Control PT-BR</h1>
 <p align="center">
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/20d8317b-a3f9-400b-9a3c-2786cef7beb5" />
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/4200d12c-4bb3-441f-a1df-8953fcfcbd89" />
</p>



  <p><b>Versão brasileira e aprimorada do firmware do upscaler Tvia Trueview5725 (ESP8266 / Wemos D1 mini)</b></p>
  <p>Mantida por <strong>Willian Nascimento (<a href="https://www.maniacogameroom.com.br/">Maniaco Game Room</a>)</strong></p>
  <p>
    Tradução completa para PT-BR, sistema de perfis com automações avançadas, novos ícones para o display OLED e correções profundas no sistema de arquivos. Desenvolvido para a comunidade de hardware retro no Brasil.
  </p>
</div>

<hr>

<h2>📊 Números da Versão (v1.0.4)</h2>
<ul>
  <li><strong>Firmware Otimizado:</strong> ~903 KB (86% do limite de 1.044.464 bytes)</li>
  <li><strong>Customização:</strong> 56 ícones de console, 51 animações de protetor de tela</li>
  <li><strong>Capacidade:</strong> 72 slots de perfil</li>
  <li><strong>Visual:</strong> 6 temas de cor, 2 idiomas integrados na WebUI</li>
</ul>

<h2>🛡️ Segurança: ninguém perde a própria GBS</h2>
<p>Uma auditoria completa do firmware, da webui e das ferramentas de atualização (~20 bugs corrigidos, incluindo um que podia travar/reiniciar o aparelho) deixou claro que corrigir bugs não bastava — o próprio processo de atualizar precisava ser à prova de imprevisto. Por isso:</p>
<ul>
  <li><strong>Backup automático antes de atualizar:</strong> o <a href="tools/gbsc-updater/">GBSC Updater</a> baixa sozinho seus presets e configurações (e, quando encontra no GitHub, o firmware anterior também) antes de gravar qualquer coisa. Se o backup falhar, a atualização é cancelada.</li>
  <li><strong>Restaurar com um clique:</strong> não gostou da versão nova, ou algo deu errado? A aba <strong>"Restaurar backup"</strong> regrava o firmware anterior e reenvia seus presets, sem precisar guardar nada manualmente.</li>
  <li><strong>Aviso de atualização disponível:</strong> a WebUI e o ícone piscando no visor OLED avisam quando há uma versão nova, comparando com os releases publicados aqui no GitHub.</li>
  <li><strong>Verificação de integridade:</strong> todo <code>.bin</code>/<code>.exe</code> publicado nos <a href="https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/releases">releases</a> vem com um <code>SHA256SUMS.txt</code> com o checksum oficial de cada arquivo — confira antes de gravar, pra ter certeza de que baixou o arquivo genuíno e não uma versão adulterada por terceiros.</li>
</ul>
<p><em>Veja a seção 12 do <a href="https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/blob/ptbr-import/docs/DESCRITIVO_DETALHADO.md">descritivo técnico</a> para os detalhes de como isso funciona por baixo dos panos.</em></p>
✨ Novidades
Checagem de atualização pelo GitHub

A webui compara sua versão com o release mais recente deste repositório e mostra um aviso discreto quando há algo novo.
O GBSC Updater ganhou um botão "Verificar atualização no GitHub": busca o .bin mais recente automaticamente, sem precisar baixar manualmente.
Alerta de atualização no visor OLED

Quando a webui encontra uma atualização, ela também avisa a GBS: um ícone de triângulo de alerta piscando aparece no menu e por cima do protetor de tela, pra você não deixar passar.
<h2>🌍 Tradução e Redesign da Interface (WebUI)</h2>
<p>Todo o ecossistema do firmware foi localizado e redesenhado, entregando uma experiência 100% nativa e agradável:</p>
<ul>
  <li><strong>Tradução e Seletor de Idioma:</strong> WebUI (abas, textos de ajuda, alertas e erros) e menu OLED traduzidos. O seletor (Português/English) aplica o inglês sobre o texto em português via dicionário exato (~110 entradas).</li>
  <li><strong>Boot Logo Customizado:</strong> Arte própria do projeto no lugar da tela de inicialização padrão.</li>
  <li><strong>Design Aprimorado:</strong> Cabeçalho novo, painéis escuros com títulos em barra metálica e botões com LED que acendem na cor do tema. Paginação adaptativa com base na altura da tela, facilitando o uso no celular.</li>
  <li><strong>Temas de Cor:</strong> 6 opções baseadas em variáveis CSS (Padrão, Verde Fósforo, Synthwave, Âmbar CRT, Rubi Famicom, Roxo GameCube).</li>
  <li><strong>Cards de Perfil:</strong> Arte do console ao fundo com contorno neon no perfil selecionado, sistema de busca inteligente (ignora acentos e maiúsculas) e contador de perfis.</li>
</ul>

<h2>⚙️ Base Técnica & Sistema de Arquivos</h2>
<ul>
  <li><strong>Migração de SPIFFS para LittleFS:</strong> O sistema de arquivos foi modernizado para o formato atual do ESP8266, garantindo maior confiabilidade. <em>Atenção: A primeira inicialização formata a área de dados (é necessário backup prévio).</em></li>
  <li><strong>Persistência Segura:</strong> O arquivo <code>/preferencesv2.txt</code> é sequencial. Novos campos foram acrescentados com valores padrão seguros para não quebrar backups existentes. Arquivos auxiliares por slot mantêm o mesmo padrão.</li>
</ul>

<h2>💾 Sistema de Perfis (Presets) e Automações</h2>
<p>O gerenciamento foi reescrito para suportar até <strong>72 slots</strong> (A-Z, a-z, 0-9 e símbolos), ordenados alfabeticamente tanto na WebUI quanto no OLED.</p>

<table width="100%">
  <thead>
    <tr>
      <th align="left">Recurso</th>
      <th align="left">Como Funciona</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Origem de Vídeo por Preset</strong></td>
      <td>Ao salvar, você escolhe a entrada (SCART / VGA / Componente / RGBS). É uma etiqueta informativa exibida no card (o chip não distingue eletricamente).</td>
    </tr>
    <tr>
      <td><strong>Perfil de Inicialização</strong></td>
      <td>Força um slot específico a ser carregado sempre que o aparelho liga, ignorando o "último usado".</td>
    </tr>
    <tr>
      <td><strong>Aviso de Mudança</strong></td>
      <td>O display OLED exibe "Formato mudou" seguido da nova resolução por 3 segundos ao alternar presets.</td>
    </tr>
    </tbody>
</table>

<h2>📺 Menu OLED & Ícones de Console</h2>
<p>Nova funcionalidade criada, seletor de icone para presets, ideal para quem gerencia coleções grandes com switches de vídeo.</p>
<ul>
  <li><strong>Diponiveis 56 ícones:</strong> O seletor permite escolher entre (controles, logos e gabinetes) de sistemas Nintendo, Sega, NEC, SNK, Sony, Microsoft, Atari, Panasonic 3DO, entre outros.</li>
  <li><strong>Processamento de Imagem:</strong> Cada arte teve recorte de bordas, fundo transparente e redimensionamento exato (40x40px). Na WebUI, um fundo claro atrás do ícone garante contraste no tema escuro.</li>
  <li><strong>Protetor de Tela Inteligente:</strong>
    <ul>
      <li><strong>Modo Nome:</strong> O nome do preset passeia pela tela. A fonte diminui dinamicamente (URW Gothic 20/14, DejaVu Mono 12/10) usando a largura do texto para evitar cortes (ex: "Super Nintendo").</li>
      <li><strong>Modo Ícone (Bounce):</strong> 51 dos 56 ícones ganharam animação de "quicar" de 4 quadros (32x32px, 1-bit). Conversão feita com threshold adaptativo (método de Otsu) e contorno automático de silhueta para não sumir no fundo preto. <em>(5 ícones complexos usam o Modo Nome como fallback).</em></li>
    </ul>
  </li>
  <li><strong>Status Ativo:</strong> Nome e ícone do preset ativo ficam fixos na tela principal, com rolagem alinhada à esquerda para nomes longos.</li>
</ul>

<h2>🛠️ Correções de Bugs (Bugfixes)</h2>

<details>
  <summary><strong>Clique para expandir as correções técnicas aplicadas</strong></summary>
  <br>
  <table width="100%">
    <thead>
      <tr>
        <th align="left">Bug Original</th>
        <th align="left">Causa Raiz</th>
        <th align="left">Solução Aplicada</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>OLED não achava presets</strong></td>
        <td>Dessincronia de sistema de arquivos (OLED lia SPIFFS, WebUI lia LittleFS).</td>
        <td>Unificação total no LittleFS.</td>
      </tr>
      <tr>
        <td><strong>Slot quebrava no 27º perfil</strong></td>
        <td>Código calculava slot por 'A' + índice (limitado a 26 posições).</td>
        <td>Implementada tabela estática de 72 caracteres (<code>slotIndexMap</code>) no firmware inteiro.</td>
      </tr>
      <tr>
        <td><strong>Origem de vídeo falhava no card</strong></td>
        <td>3 requisições paralelas excediam o limite de conexões do ESP8266.</td>
        <td>Requisições sequenciadas com rotina de retry.</td>
      </tr>
      <tr>
        <td><strong>Ganho ADC "sem efeito"</strong></td>
        <td>O resync restaurava o padrão de fábrica se não houvesse preset carregado.</td>
        <td>Valores ajustados de ganho agora sobrevivem e são restaurados após o reset.</td>
      </tr>
      <tr>
        <td><strong>Overflow horizontal mobile</strong></td>
        <td>A tag <code>&lt;fieldset&gt;</code> ignorava propriedades grid/flex e passava da tela.</td>
        <td>CSS ajustado na interface (<code>min-width: 0</code> + grid <code>minmax</code>).</td>
      </tr>
      <tr>
        <td><strong>Menu OLED travava e reiniciava (v1.0.3)</strong></td>
        <td>Com 17+ presets nomeados, faltava reservar espaço pro aviso de "muitos presets" numa lista limitada a 16 posições.</td>
        <td>Menu reserva a última posição pro aviso quando não cabem todos.</td>
      </tr>
      <tr>
        <td><strong>Wi-Fi não reconectava sozinho (v1.0.3)</strong></td>
        <td>A supervisão de reconexão só existia na inicialização; uma queda depois disso deixava a GBS desconectada até reboot manual.</td>
        <td>Detecção de queda + reconexão automática, com retentativa periódica.</td>
      </tr>
      <tr>
        <td><strong>XSS no scan de Wi-Fi da webui (v1.0.3)</strong></td>
        <td>Nome de rede escaneada entrava direto no HTML sem ser filtrado.</td>
        <td>Nome da rede escapado antes de entrar na página.</td>
      </tr>
    </tbody>
  </table>
</details>

<br>

<h2>💻 Ferramentas e Documentação</h2>
<ul>
  <li><strong>GBSC Updater:</strong> Programa próprio para Windows (ou Python em qualquer OS), com três abas: <strong>Atualizar por Wi-Fi</strong> (informando o IP), <strong>Gravar por USB</strong> (primeira instalação) e <strong>Restaurar backup</strong> (desfaz uma atualização com um clique). Faz backup automático dos presets antes de gravar, verifica atualizações no GitHub, lida sozinho com o serviço OTA do ESP8266 e contorna o Firewall do Windows.</li>
  <li><strong>Pipeline de Mídia:</strong> Script <code>make_icon_animation.py</code> que gera automaticamente o código em C++ (<code>OLEDIconAnimations.cpp</code>) a partir dos assets.</li>
  <li><strong>Documentação Inclusa:</strong> <a href="https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/blob/ptbr-import/docs/MANUAL_DE_USO.md">Manual de Uso</a>, <a href="https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/blob/ptbr-import/docs/TUTORIAL_INSTALACAO.md">Tutorial de Instalação</a> passo a passo (Wi-Fi/USB) e este <a href="https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/blob/ptbr-import/docs/DESCRITIVO_DETALHADO.md">descritivo técnico</a>.</li>
</ul>

<h2>📌 Pendências Conhecidas (Roadmap)</h2>
<ul>
  <li><strong>Offset por Canal (Nível de Preto):</strong> A ideia de ajustar o offset por canal ADC está mapeada (registradores já existem no código), mas a interação com a rotina de auto-calibração precisa de mais testes.</li>
  <li><strong>Automação para Switches SCART / Componente:</strong> Em fase de mapeamento/desenvolvimento.</li>
  <li><strong>Menu OLED:</strong> Atualmente restrito ao PT-BR (textos baseados em bitmaps pré-desenhados).</li>
  </ul>

<h2>📜 Licença e Atribuição</h2>
<p>Este projeto é distribuído sob a <a href="LICENSE"><strong>GNU General Public License v3.0 (GPLv3)</strong></a>, a mesma licença do <a href="https://github.com/ramapcsx2/gbs-control">gbs-control</a> original do qual este é um fork. Isso significa, na prática:</p>
<ul>
  <li>Você pode usar, estudar, modificar e redistribuir este firmware livremente — inclusive para fins comerciais.</li>
  <li><strong>Mas</strong>: qualquer fork, modificação ou redistribuição (comercial ou não) precisa continuar sob a <strong>GPLv3</strong>, manter o <strong>código-fonte aberto e disponível</strong> a quem recebe o binário, e preservar os <strong>avisos de copyright e créditos</strong> aos autores originais e a este fork.</li>
  <li>Não é permitido "fechar" o código, vender uma versão proprietária sem disponibilizar o fonte, ou remover a atribuição — isso violaria os termos da GPLv3 e os direitos dos autores originais.</li>
</ul>
<p>Veja o arquivo <a href="LICENSE">LICENSE</a> para o texto completo.</p>
