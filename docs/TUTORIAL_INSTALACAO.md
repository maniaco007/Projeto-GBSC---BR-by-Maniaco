# Tutorial de Instalação — GBS-Control PT-BR

Passo a passo para colocar esta versão na **sua** GBS, em casa, sem saber programar.

> **Tempo:** 10 a 15 minutos · **Precisa de:** um computador com Windows, a GBS ligada e (para a 1ª instalação) um cabo USB de dados.

---

## Antes de começar: qual é o seu caso?

| Situação | Vá para |
| --- | --- |
| Minha GBS **já roda o GBS-Control** e conecta no Wi-Fi da minha casa | **[Caminho A — Atualizar pelo Wi-Fi](#caminho-a--atualizar-pelo-wi-fi-o-mais-fácil)** |
| Minha GBS **nunca teve** GBS-Control, ou **não conecta no Wi-Fi** | **[Caminho B — Instalar pelo cabo USB](#caminho-b--instalar-pelo-cabo-usb-primeira-vez)** |

**Compatibilidade:** placa GBS-8200/GBS-8220 com módulo **Wemos D1 mini (ESP8266, 4 MB)** — o mesmo hardware do GBS-Control original. O display OLED é opcional.

---

## Passo 0 — Baixe os arquivos

1. Abra a página de **Releases** do projeto no GitHub:
   `https://github.com/maniaco007/Projeto-GBSC---BR-by-Maniaco/releases`
2. Baixe o arquivo **`GBSC-Updater-Windows.zip`**.
3. Clique com o botão direito no zip → **Extrair tudo**.
4. Dentro da pasta extraída está o programa **`GBSC-Updater.exe`** (o firmware já vem dentro dele).

> **O Windows avisou "o Windows protegeu o computador"?** É normal para programas novos. Clique em **Mais informações → Executar assim mesmo**.

---

## Passo 1 — Sobre backup: você está protegido em duas camadas

Todo o processo de atualização foi pensado pra que você **nunca perca seus presets** e sempre possa **voltar atrás** se algo não sair como esperado:

1. **Automático:** ao clicar em Enviar no Caminho A (ou no Caminho B, se você informar o IP da GBS), o **GBSC-Updater já baixa sozinho** uma cópia dos seus presets e configurações antes de gravar qualquer coisa — e, se achar no GitHub, guarda também o firmware que estava rodando. Se esse backup falhar por qualquer motivo, o programa **cancela a atualização** em vez de arriscar seus dados.
2. **Manual (opcional, mas recomendado):** se você já usa o GBS-Control, pode também baixar uma cópia pela webui, como camada extra:
   - Abra a webui da GBS no navegador (`http://gbscontrol.local` ou o IP dela).
   - Vá na aba **Sistema** (ícone de raio) → **Cópia** → **Baixar**.
   - Guarde o arquivo baixado.

Se depois de atualizar você quiser desfazer, veja **[Voltar para a versão anterior](#voltar-para-a-versão-anterior)** no final deste tutorial — é bem mais simples do que parece.

---

## Caminho A — Atualizar pelo Wi-Fi (o mais fácil)

### A.1 Descubra o IP da GBS
- Olhe na **telinha OLED**: menu **Wi-Fi** mostra o IP; **ou**
- Abra a lista de aparelhos conectados no seu **roteador** e procure `gbscontrol`; **ou**
- Tente `http://gbscontrol.local` no navegador.

O IP tem cara de `192.168.0.70`.

### A.2 Envie o firmware
1. Abra o **`GBSC-Updater.exe`**.
2. Fique na aba **"Atualizar por Wi-Fi"**.
3. Em **IP da GBS**, digite o IP (ex.: `192.168.0.70`).
4. O campo **Firmware** já vem preenchido com o firmware incluído. *(Se quiser usar outro arquivo `.bin`, clique em **Escolher...**.)*
5. Clique em **Enviar / Gravar**.

### A.3 Se o Windows perguntar sobre o Firewall
Na **primeira vez** o Windows pode abrir uma janela **"Firewall do Windows Defender"**. Clique em **Permitir acesso**. Isso é necessário porque a GBS precisa se conectar de volta ao seu computador para receber o arquivo. O programa tenta 3 vezes sozinho, então basta permitir e esperar.

### A.4 Espere terminar
A barra de progresso vai até 100% e aparece **"Pronto! A GBS vai reiniciar sozinha"**. **Não desligue a GBS** durante o envio. Em cerca de 15 segundos ela volta com a nova versão.

Recarregue a página da webui — pronto! ✅

---

## Caminho B — Instalar pelo cabo USB (primeira vez)

### B.1 Prepare o cabo e o driver
- Use um cabo **USB de dados** (alguns cabos só carregam e **não funcionam**). Se o computador não reconhecer a GBS, troque o cabo.
- A maioria das placas D1 mini usa o chip **CH340**. Se a porta **COM** não aparecer no programa, instale o driver CH340 (procure "driver CH340 Windows") e reconecte o cabo.

### B.2 Conecte
1. **Desligue** a GBS da energia (fonte).
2. Ligue o cabo USB no conector da **placa D1 mini** (o módulo pequeno em cima da GBS) e no computador.

### B.3 Grave
1. Abra o **`GBSC-Updater.exe`** e vá na aba **"Gravar por USB (primeira vez)"**.
2. Em **Porta (COM)**, escolha a porta que apareceu (se a lista estiver vazia, clique em **Atualizar lista**).
3. O firmware já vem preenchido.
4. Deixe **"Apagar tudo antes"** **desmarcado** (marque só se algo der problema).
5. Clique em **Enviar / Gravar** e confirme.
6. Aguarde a barra do log chegar em **"Hash of data verified" / "Pronto!"** (uns 30 a 60 segundos).
7. Desconecte o USB e ligue a GBS na energia normalmente.

### B.4 Configure o Wi-Fi
1. Ao ligar, a GBS cria a rede **`gbscontrol`**. Conecte o celular nela.
2. Abra `http://192.168.4.1` no navegador do celular.
3. Vá em **Sistema → Wi-Fi → Estação → Selecionar Rede**, escolha a rede da sua casa, digite a senha e toque **Conectar**.
4. A GBS reinicia e passa a responder em `http://gbscontrol.local`.

> Se você tinha um backup, vá em **Sistema → Cópia → Restaurar** e envie o arquivo.

---

## Deu problema? Soluções rápidas

| Problema | O que fazer |
| --- | --- |
| "Não consegui falar com a GBS" | Confira o IP; a GBS e o computador precisam estar na **mesma rede Wi-Fi**. Teste `http://IP` no navegador |
| "A GBS aceitou, mas não conseguiu se conectar de volta" | É o **Firewall**. Clique em **Permitir acesso** quando o Windows perguntar (marque *rede privada e pública*) e tente de novo |
| "A GBS não respondeu ao convite" | Espere 30 s e tente de novo. Se persistir, desligue e ligue a GBS da energia |
| Lista de portas COM vazia (USB) | Troque o cabo (precisa ser de dados), instale o driver **CH340**, reconecte |
| "A gravação por USB falhou" | Feche outros programas que usem a porta (Arduino, PlatformIO), tente outra porta USB e, se precisar, marque **Apagar tudo antes** |
| Perfis sumiram, ou não gostou da atualização | Use a aba **Restaurar backup** do GBSC-Updater (veja [Voltar para a versão anterior](#voltar-para-a-versão-anterior)) — ou, se preferiu o backup manual, **Sistema → Cópia → Restaurar** na webui |
| A GBS ficou sem responder após atualizar | Desligue da energia, espere 10 s e ligue de novo. Se persistir, refaça pelo **Caminho B** (USB) |

---

## Voltar para a versão anterior

Não gostou de uma atualização, ou algo não ficou do jeito esperado? Como o GBSC-Updater fez um backup automático antes de gravar (Passo 1), desfazer é simples:

1. Abra o **GBSC-Updater.exe** e vá na aba **"Restaurar backup"**.
2. Em **IP da GBS**, digite o IP do aparelho.
3. Em **Backup**, escolha o backup da lista (mostra a data e a versão de quando foi feito).
4. Clique em **Restaurar**.

Isso regrava o firmware de antes (quando o programa conseguiu guardar uma cópia dele) **e** reenvia os seus presets e configurações — do jeito que estavam antes da atualização. Não precisa ter guardado nada manualmente: os backups automáticos do Passo 1 ficam na pasta `backups`, do lado do `GBSC-Updater.exe`.

**Se quiser voltar para o GBS-Control original** (sem a versão PT-BR), baixe o `.bin` dele no projeto oficial (`ramapcsx2/gbs-control`) e grave pelo Caminho A ou B, usando o botão **Escolher...** para selecionar esse arquivo em vez do incluído. Nesse caso, restaure seus presets só se o formato de arquivo ainda for compatível — o mais seguro é considerar essa troca como uma reinstalação do zero.

---
