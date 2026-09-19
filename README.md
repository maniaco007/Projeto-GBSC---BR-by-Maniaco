<div align="center">
  <h1>🎮 GBS-Control PT-BR</h1>
  <p>
    <strong>Versão brasileira e aprimorada do firmware do upscaler Tvia Trueview5725</strong><br>
    Mantida por <a href="https://maniacogameroom.com.br/" target="_blank">Willian Nascimento (Maniaco Game Room)</a>
  </p>
  <p>
    Tradução completa para PT-BR, sistema de perfis com automações avançadas, novos ícones para o display OLED e correções profundas no sistema de arquivos do ESP8266.
  </p>
  <br>
</div>

<h2>🇧🇷 Tradução </h2>
<p>Todo o ecossistema do firmware foi localizado, entregando uma experiência 100% nativa:</p>
<ul>
  <li><strong>WebUI Completa:</strong> Todas as abas, textos de ajuda e mensagens de erro traduzidos.</li>
  <li><strong>Menu OLED:</strong> Navegação, nomes de opções e telas de status em português.</li>
  <li><strong>Boot Logo Customizado:</strong> Arte própria do projeto substituindo a tela de inicialização padrão.</li>
  <li><strong>Seletor de Linguagem:</strong> Escolha a linguagem que mais te agrada em poucos cliques.</li>
</ul>

<hr>

<h2>⚙️ Base Técnica & Sistema de Arquivos</h2>
<blockquote>
  <p><strong>Migração de SPIFFS para LittleFS:</strong> O sistema de arquivos interno foi modernizado para o formato atual do ESP8266. Isso garante maior confiabilidade e <strong>corrigiu um bug crítico</strong> onde o menu OLED (aba Perfis) não encontrava os presets salvos, pois tentava ler o FS antigo enquanto a WebUI já operava no novo.</p>
</blockquote>

<hr>

<h2>💾 Sistema de Perfis (Presets) e Automações</h2>
<p>O gerenciamento de perfis foi reescrito para suportar até <strong>72 slots</strong> (<kbd>A-Z</kbd>, <kbd>a-z</kbd>, <kbd>0-9</kbd> e símbolos) e ganhou automações focadas em setups com múltiplos consoles:</p>

<table>
  <thead>
    <tr>
      <th align="left">Recurso</th>
      <th align="left">O que faz</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Origem de vídeo por preset</strong></td>
      <td>Ao salvar um perfil, você escolhe o conector (SCART / VGA / Componente / RGBS). A informação é exibida no card do preset.</td>
    </tr>
    <tr>
      <td><strong>Link Perfil ↔ Entrada</strong></td>
      <td>O GBS-C lembra qual preset foi usado em cada entrada física e o recarrega automaticamente ao detectar a fonte.</td>
    </tr>
    <tr>
      <td><strong>Perfil de Inicialização</strong></td>
      <td>Força um slot específico para ser carregado sempre que o aparelho liga (ignorando o "último usado").</td>
    </tr>
    <tr>
      <td><strong>Aviso de Mudança de Formato</strong></td>
      <td>O display OLED exibe <em>"Formato mudou"</em> + a nova resolução por 3 segundos ao alternar presets.</td>
    </tr>
  </tbody>
</table>

<hr>

<h2>📺 Menu OLED & Ícones de Console</h2>
<p>A interface física do aparelho foi amplamente expandida, ideal para quem gerencia coleções grandes com switches de vídeo.</p>

<h3>Navegação e Display</h3>
<ul>
  <li><strong>Aba Perfis:</strong> Navegação e seleção de presets salvos, ordenados alfabeticamente.</li>
  <li><strong>Status Ativo:</strong> Nome e ícone do preset ativo ficam fixos na tela principal. Nomes longos rolam automaticamente e ficam alinhados à esquerda.</li>
</ul>

<h3>Seletor de Ícones Expandido (De 25 para 56 Consoles)</h3>
<p>O seletor original tinha apenas desenhos genéricos. Esta versão inclui <strong>56 ícones com arte real</strong> (controles, logos e gabinetes) cobrindo sistemas da Nintendo, Sega, NEC, SNK, Sony, Microsoft, Atari, Philips, Panasonic 3DO, entre outros.</p>
<ul>
  <li><em>Processamento:</em> Cada imagem passou por recorte de bordas, fundo transparente e redimensionamento exato (40x40px).</li>
  <li><em>Contraste:</em> Adicionado um fundo claro atrás de cada ícone na WebUI para garantir a visibilidade de traços escuros.</li>
</ul>

<h3>Protetor de Tela Inteligente e Animações</h3>
<p>O screensaver do OLED agora possui dois modos:</p>
<ol>
  <li><strong>Modo Nome:</strong> Usa uma fonte dinâmica que encolhe automaticamente em até 4 tamanhos para evitar cortes em nomes longos.</li>
  <li><strong>Modo Ícone (Bounce):</strong> 51 dos 56 ícones ganharam uma animação de "quicar" de 4 quadros. Gerada em 1-bit com <em>threshold adaptativo</em> e contorno automático de silhuetas para garantir leitura no display pequeno.</li>
</ol>

<hr>

<h2>🛠️ Correções de Bugs (Bugfixes)</h2>
<details>
  <summary><strong>Clique para expandir as correções técnicas</strong></summary>
  <br>
  <table>
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
        <td>Dessincronia de File System (SPIFFS vs LittleFS).</td>
        <td>Unificação total no LittleFS.</td>
      </tr>
      <tr>
        <td><strong>Slot quebrava no 27º perfil</strong></td>
        <td>Código calculava slot por <code>'A' + índice</code> (limitado a 26).</td>
        <td>Implementada tabela de 72 caracteres (<code>slotIndexMap</code>).</td>
      </tr>
      <tr>
        <td><strong>Origem de vídeo sumia do card</strong></td>
        <td>3 requisições paralelas excediam limite do ESP8266.</td>
        <td>Requisições sequenciadas com rotina de <em>retry</em>.</td>
      </tr>
      <tr>
        <td><strong>Reboot ao salvar ícone</strong></td>
        <td>Variáveis grandes na pilha em handler assíncrono.</td>
        <td>Variáveis movidas para a memória estática.</td>
      </tr>
      <tr>
        <td><strong>Ganho ADC manual resetando</strong></td>
        <td>O resync restaurava o padrão se não houvesse preset carregado.</td>
        <td>Valores manuais agora sobrevivem ao resync.</td>
      </tr>
      <tr>
        <td><strong>Overflow horizontal mobile</strong></td>
        <td>O <code>&lt;fieldset&gt;</code> ignorava propriedades flex/grid.</td>
        <td>CSS ajustado na UI (<code>min-width: 0</code> + grid minmax).</td>
      </tr>
    </tbody>
  </table>
</details>

<h2>📌 Pendências Conhecidas (Roadmap)</h2>
<ul>
  <li><strong>Offset por Canal (Nível de Preto):</strong> A ideia de ajustar o offset por canal ADC (R/G/B) está mapeada. Os registradores já existem no código, mas a interação com a rotina de auto-calibração precisa de mais testes.</li>
  <li><strong>Automação para Switchs Scart \ Video Componente:</strong> Em desenvolvimento.</li>
</ul>

<br>
<div align="center">
  <p><em>Desenvolvido para a comunidade de hardware retro no Brasil.</em></p>
</div>

Documentation: https://ramapcsx2.github.io/gbs-control/
