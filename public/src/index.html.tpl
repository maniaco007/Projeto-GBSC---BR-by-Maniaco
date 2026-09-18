<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <title>GBS-Control</title>
    <link rel="manifest" href="${manifest}" />
    <style>
      ${styles}
    </style>
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <link rel="icon" type="image/png" href="${favicon}" />
    <link rel="apple-touch-icon" href="${icon1024}" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black" />
    <meta
      name="viewport"
      content="viewport-fit=cover, user-scalable=no, width=device-width, initial-scale=1, maximum-scale=1"
    />
  </head>
  <body tabindex="0" class="gbs-help-hide gbs-output-hide">
    <svg style="display: none" aria-hidden="true">
      <symbol id="gbs-slot-icon-0" viewBox="0 0 24 24">
        <path d="M6 9a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H9a3 3 0 0 1-3-3V9zm3-1a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H9z"/>
        <circle cx="12" cy="12" r="1.6"/>
      </symbol>
      <symbol id="gbs-slot-icon-1" viewBox="0 0 24 24">
        <rect x="7" y="3" width="10" height="18" rx="2"/>
        <rect x="9" y="6" width="6" height="9" fill="#3ea6ff" opacity="0.9"/>
        <circle cx="12" cy="17.5" r="1" fill="#000" opacity="0.85"/>
      </symbol>
      <symbol id="gbs-slot-icon-2" viewBox="0 0 24 24">
        <rect x="2.5" y="9" width="19" height="7" rx="1"/>
        <rect x="5" y="10.4" width="2" height="4.2" fill="#8a5a2b"/>
        <rect x="8" y="10.4" width="2" height="4.2" fill="#8a5a2b"/>
        <rect x="11" y="10.4" width="2" height="4.2" fill="#8a5a2b"/>
      </symbol>
      <symbol id="gbs-slot-icon-3" viewBox="0 0 24 24">
        <rect x="2.5" y="9.5" width="19" height="6" rx="1"/>
        <circle cx="8.5" cy="12.5" r="2" fill="#e8823c"/>
        <circle cx="15.5" cy="12.5" r="2" fill="#e8823c"/>
      </symbol>
      <symbol id="gbs-slot-icon-4" viewBox="0 0 24 24">
        <rect x="2.5" y="8.5" width="19" height="8" rx="1.2"/>
        <circle cx="9" cy="12.5" r="2.6" fill="#d9541f"/>
        <circle cx="16" cy="12.5" r="2.6" fill="#d9541f"/>
      </symbol>
      <symbol id="gbs-slot-icon-5" viewBox="0 0 24 24">
        <path d="M9 2h6l1.5 2.2v15.6L15 22H9l-1.5-2.2V4.2z"/>
        <rect x="10.3" y="5" width="3.4" height="12" fill="#3d7bff" opacity="0.9"/>
      </symbol>
      <symbol id="gbs-slot-icon-6" viewBox="0 0 24 24">
        <rect x="2.5" y="7" width="19" height="10" rx="2.5"/>
        <circle cx="12" cy="12" r="2.6" fill="#3aa757"/>
      </symbol>
      <symbol id="gbs-slot-icon-7" viewBox="0 0 24 24">
        <rect x="10" y="2" width="4" height="20" rx="2"/>
        <circle cx="12" cy="19" r="1.1" fill="#3ea6ff"/>
      </symbol>
      <symbol id="gbs-slot-icon-8" viewBox="0 0 24 24">
        <rect x="2.5" y="9" width="19" height="6.5" rx="1"/>
        <path d="M2.5 9h19l-3 6.5h-13z" fill="#d3242f" opacity="0.9"/>
      </symbol>
      <symbol id="gbs-slot-icon-9" viewBox="0 0 40 40">
        <image href="data:image/png;base64,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" width="40" height="40"/>
      </symbol>
      <symbol id="gbs-slot-icon-10" viewBox="0 0 24 24">
        <rect x="2.5" y="8" width="19" height="8" rx="4"/>
        <path d="M8 12a4 4 0 0 1 8 0" fill="none" stroke="#ff7a1a" stroke-width="1.6" stroke-linecap="round"/>
        <circle cx="12" cy="12.3" r="0.8" fill="#ff7a1a"/>
      </symbol>
      <symbol id="gbs-slot-icon-11" viewBox="0 0 24 24">
        <rect x="2.5" y="9" width="19" height="7" rx="1"/>
        <rect x="5" y="10.4" width="6" height="4.2" fill="#333" opacity="0.85"/>
        <circle cx="19" cy="12.5" r="1.1" fill="#d3242f"/>
      </symbol>
      <symbol id="gbs-slot-icon-12" viewBox="0 0 24 24">
        <rect x="2.5" y="10" width="19" height="6" rx="1"/>
        <circle cx="12" cy="9" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/>
        <circle cx="12" cy="9" r="1.6" fill="#9aa0a6"/>
      </symbol>
      <symbol id="gbs-slot-icon-13" viewBox="0 0 24 24">
        <rect x="2.5" y="7.5" width="19" height="9" rx="3.5"/>
        <circle cx="12" cy="12" r="3" fill="none" stroke="#8560ff" stroke-width="1.6"/>
      </symbol>
      <symbol id="gbs-slot-icon-14" viewBox="0 0 24 24">
        <rect x="2.5" y="9" width="19" height="7" rx="1.5"/>
        <circle cx="7" cy="12.5" r="1.2" fill="#3d7bff"/>
        <circle cx="10.4" cy="12.5" r="1.2" fill="#d3242f"/>
        <circle cx="13.8" cy="12.5" r="1.2" fill="#3aa757"/>
        <circle cx="17.2" cy="12.5" r="1.2" fill="#f2c218"/>
      </symbol>
      <symbol id="gbs-slot-icon-15" viewBox="0 0 24 24">
        <rect x="3" y="8" width="18" height="8" rx="1"/>
        <path d="M3 8h18v3H3z" fill="#5a6068" opacity="0.9"/>
      </symbol>
      <symbol id="gbs-slot-icon-16" viewBox="0 0 24 24">
        <rect x="3" y="7" width="18" height="10" rx="3"/>
        <circle cx="12" cy="12" r="2.6" fill="#d8b23a"/>
      </symbol>
      <symbol id="gbs-slot-icon-17" viewBox="0 0 24 24">
        <rect x="2.5" y="9" width="19" height="7" rx="1.2"/>
        <rect x="9.5" y="10.4" width="5" height="1.6" fill="#c9c9c9"/>
        <circle cx="18" cy="12.5" r="1" fill="#3aa757"/>
      </symbol>
      <symbol id="gbs-slot-icon-18" viewBox="0 0 24 24">
        <path d="M4 9h13l4 3.5-4 3.5H4z"/>
        <path d="M6 11h9v3H6z" fill="#d3242f" opacity="0.85"/>
      </symbol>
      <symbol id="gbs-slot-icon-19" viewBox="0 0 24 24">
        <rect x="4" y="6" width="16" height="12" rx="1.5"/>
        <circle cx="12" cy="12" r="2.4" fill="#e8e8e8"/>
      </symbol>
      <symbol id="gbs-slot-icon-20" viewBox="0 0 24 24">
        <rect x="7" y="8" width="10" height="8" rx="1"/>
        <circle cx="3.5" cy="12" r="2.6" fill="#d3242f"/>
        <circle cx="20.5" cy="12" r="2.6" fill="#e8e8e8"/>
      </symbol>
      <symbol id="gbs-slot-icon-21" viewBox="0 0 24 24">
        <rect x="1.5" y="10" width="21" height="4.5" rx="1"/>
        <circle cx="18" cy="12.3" r="1.6" fill="#d3242f"/>
      </symbol>
      <symbol id="gbs-slot-icon-22" viewBox="0 0 24 24">
        <rect x="3" y="9" width="18" height="9" rx="1"/>
        <path d="M4 9a8 8 0 0 1 16 0z" fill="none" stroke="#d8b23a" stroke-width="1.5"/>
      </symbol>
      <symbol id="gbs-slot-icon-23" viewBox="0 0 24 24">
        <rect x="2.5" y="9" width="19" height="7" rx="1"/>
        <rect x="5" y="10.2" width="12" height="4.6" fill="#8a5a2b"/>
        <rect x="14.5" y="10.9" width="1.4" height="1.4" fill="#e8e8e8"/>
        <rect x="16.4" y="10.9" width="1.4" height="1.4" fill="#e8e8e8"/>
        <rect x="18.3" y="10.9" width="1.4" height="1.4" fill="#e8e8e8"/>
      </symbol>
      <symbol id="gbs-slot-icon-24" viewBox="0 0 24 24">
        <rect x="3" y="7.5" width="18" height="9" rx="1"/>
        <circle cx="12" cy="12" r="2.4" fill="#3aa757"/>
      </symbol>
    </svg>
    <div class="gbs-container">
      <div class="gbs-menu">
        <svg
          version="1.0"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0,0,284,99"
          class="gbs-menu__logo"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            fill="#010101"
            d="M283.465 97.986H0V0h283.465v97.986z"
          />
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            fill="#00c0fb"
            d="M270.062 75.08V60.242h-17.04v10.079c0 2.604-2.67 5.02-5.075 5.02h-20.529c-4.983 0-5.43-4.23-5.43-8.298v-37.93c0-2.668 1.938-4.863 4.88-4.863h20.995c2.684 0 5.158 1.492 5.158 4.482V38.86h17.04V27.63c0-7.867-4.26-15.923-13.039-15.923H221.19c-7.309 0-15.604 4.235-15.604 12.652v50.387c0 6.508 4.883 13.068 12.42 13.068h38.47c6.606 0 13.587-5.803 13.587-12.734zM190.488 5.562H6.617L6.585 91.91h183.91l-.007-86.348z"
          />
          <text
            transform="translate(12.157 81.95)"
            fill="#010101"
            font-family="'AmsiPro-BoldItalic'"
            font-size="92.721"
            letter-spacing="-9"
          >
            GBS
          </text>
          <g>
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              fill="#010101"
              d="M586.93 97.986H303.464V0h283.464v97.986z"
            />
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              fill="#FFF"
              d="M573.526 75.08V60.242h-17.04v10.079c0 2.604-2.669 5.02-5.075 5.02h-20.528c-4.984 0-5.43-4.23-5.43-8.298v-37.93c0-2.668 1.937-4.863 4.88-4.863h20.995c2.683 0 5.157 1.492 5.157 4.482V38.86h17.04V27.63c0-7.867-4.26-15.923-13.038-15.923h-35.833c-7.31 0-15.605 4.235-15.605 12.652v50.387c0 6.508 4.884 13.068 12.42 13.068h38.471c6.606 0 13.586-5.803 13.586-12.734zM493.953 5.562H310.08l-.032 86.348h183.91l-.006-86.348z"
            />
            <text
              transform="translate(315.621 81.95)"
              fill="#010101"
              font-family="'AmsiPro-BoldItalic'"
              font-size="92.721"
              letter-spacing="-9"
            >
              GBS
            </text>
          </g>
        </svg>
        <button
          gbs-section="presets"
          class="gbs-button gbs-button__menu gbs-icon"
          active
        >
          input
        </button>
        <button
          gbs-section="control"
          class="gbs-button gbs-button__menu gbs-icon"
        >
          control_camera
        </button>
        <button
          gbs-section="filters"
          class="gbs-button gbs-button__menu gbs-icon"
        >
          blur_on
        </button>
        <button
          gbs-section="preferences"
          class="gbs-button gbs-button__menu gbs-icon"
        >
          tune
        </button>
        <button
          gbs-section="developer"
          class="gbs-button gbs-button__menu gbs-icon"
          hidden
        >
          developer_mode
        </button>
        <button
          gbs-section="system"
          class="gbs-button gbs-button__menu gbs-icon"
        >
          bolt
        </button>
      </div>
      <div class="gbs-scroll">
        <section name="presets">
          <fieldset class="gbs-fieldset" style="padding: 8px 2px">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">aspect_ratio</div>
              <div>Resolução</div>
            </legend>
            <!-- prettier-ignore -->
            <ul class="gbs-help">
              <li>Escolha uma resolução de saída entre estas predefinições.</li>
              <li>Sua seleção também será usada na inicialização. 1280x960 é recomendado para fontes NTSC, 1280x1024 para PAL.
              </li>
              <li>Use a opção "Perfis Combinados" para alternar entre as duas automaticamente (aba Preferências)
              </li>
              <li>Selecionar uma resolução também a torna a nova predefinição de inicialização.</li>
            </ul>
            <div class="gbs-resolution">
              <button
                class="gbs-button gbs-button__resolution"
                gbs-message="s"
                gbs-message-type="user"
                gbs-click="normal"
                gbs-element-ref="button1920x1080"
                gbs-role="preset"
              >
                1920 <span>x1080</span>
              </button>
              <button
                class="gbs-button gbs-button__resolution"
                gbs-message="p"
                gbs-message-type="user"
                gbs-click="normal"
                gbs-element-ref="button1280x1024"
                gbs-role="preset"
              >
                1280 <span>x1024</span>
              </button>
              <button
                class="gbs-button gbs-button__resolution"
                gbs-message="f"
                gbs-message-type="user"
                gbs-click="normal"
                gbs-element-ref="button1280x960"
                gbs-role="preset"
              >
                1280 <span>x960</span>
              </button>
              <button
                class="gbs-button gbs-button__resolution"
                gbs-message="g"
                gbs-message-type="user"
                gbs-click="normal"
                gbs-element-ref="button1280x720"
                gbs-role="preset"
              >
                1280 <span>x720</span>
              </button>
              <button
                class="gbs-button gbs-button__resolution"
                gbs-message="h"
                gbs-message-type="user"
                gbs-click="normal"
                gbs-element-ref="button720x480"
                gbs-role="preset"
              >
                480p 576p
              </button>
              <button
                gbs-message="L"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button gbs-button__resolution gbs-button__resolution--center gbs-button__secondary"
                gbs-element-ref="button15kHzScaleDown"
                gbs-role="preset"
              >
                <div class="gbs-icon">tv</div>
                <div>15KHz</div>
              </button>
              <button
                gbs-message="K"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__resolution gbs-button__resolution--center gbs-button__secondary"
                gbs-element-ref="buttonSourcePassThrough"
                gbs-role="preset"
              >
                <div class="gbs-icon">swap_calls</div>
                <div class="gbs-button__resolution--pass-through">
                  Passagem
                </div>
              </button>
            </div>
          </fieldset>
          <fieldset class="gbs-fieldset presets">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">input</div>
              <div>Perfis</div>
            </legend>
            <!-- prettier-ignore -->
            <ul class="gbs-help">
              <li>Para salvar suas customizações, primeiro selecione um slot para o novo perfil, depois salve ou carregue nele.</li>
              <li>Selecionar um slot também o torna o perfil de boot.</li>
            </ul>
            <div class="gbs-presets" gbs-slot-html></div>
            <div class="gbs-flex">
              <button
                class="gbs-button gbs-button__control-action"
                active
                gbs-element-ref="buttonLoadCustomPreset"
                gbs-role="preset"
                onclick="loadPreset()"
              >
                <div class="gbs-icon">play_arrow</div>
                <div>carregar perfil</div>
              </button>
              <button
                class="gbs-button gbs-button__control-action gbs-button__secondary"
                onclick="savePreset()"
                active
              >
                <div class="gbs-icon">fiber_manual_record</div>
                <div>salvar perfil</div>
              </button>
              <button
                class="gbs-button gbs-button__control-action gbs-delete-preset-button"
                onclick="deletePreset()"
                active
              >
                <div class="gbs-icon">delete_forever</div>
                <div>apagar perfil</div>
              </button>
            </div>
          </fieldset>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">stars</div>
              <div>Perfis Padrão do Projeto</div>
            </legend>
            <!-- prettier-ignore -->
            <ul class="gbs-help">
              <li>Importa os perfis pré-configurados deste projeto (um por slot: A, B, C...).</li>
              <li>Sobrescreve os slots correspondentes. Os demais slots ficam intactos.</li>
            </ul>
            <div class="gbs-flex">
              <button
                class="gbs-button gbs-button__control gbs-button__secondary gbs-custom-presets-button"
              >
                <div class="gbs-icon">download</div>
                <div>importar perfis padrão</div>
              </button>
            </div>
          </fieldset>
        </section>

        <section name="control" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">wb_sunny</div>
              <div>Ganho ADC (brilho)</div>
            </legend>
            <!-- prettier-ignore -->
            <ul class="gbs-help">
              <li>Ganho +/- ajusta o ganho do perfil carregado atualmente.</li>
              <li>Ganho Automático aumenta o ganho até áreas claras virarem brancas, depois reduz quando detecta clipping. Calibre por alguns segundos numa tela branca.</li>
            </ul>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button
                gbs-message="o"
                gbs-message-type="user"
                gbs-click="repeat"
                class="gbs-button gbs-button__control"
              >
                <div class="gbs-icon">remove_circle_outline</div>
                <div>ganho</div>
              </button>
              <button
                gbs-message="n"
                gbs-message-type="user"
                gbs-click="repeat"
                class="gbs-button gbs-button__control"
              >
                <div class="gbs-icon">add_circle_outline</div>
                <div>ganho</div>
              </button>
              <button
                gbs-message="T"
                gbs-message-type="action"
                gbs-click="normal"
                gbs-toggle="adcAutoGain"
                class="gbs-button gbs-button__control gbs-button__secondary"
              >
                <div class="gbs-icon">brightness_auto</div>
                <div>Ganho Auto</div>
              </button>
            </div>
            <!-- prettier-ignore -->
            <ul class="gbs-help">
              <li>Ajuste fino por canal (R/G/B), útil quando a placa tem uma tendência de cor (ex.: excesso de vermelho) que o ganho combinado não corrige. Desativa o Ganho Automático.</li>
            </ul>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control gbs-adc-gain-btn" gbs-adc-gain-channel="r" gbs-adc-gain-delta="1">
                <div class="gbs-icon">remove_circle_outline</div>
                <div>R</div>
              </button>
              <div class="gbs-button gbs-button__control" style="flex-grow: 0; text-align: center" gbs-adc-gain-readout="r">—</div>
              <button class="gbs-button gbs-button__control gbs-adc-gain-btn" gbs-adc-gain-channel="r" gbs-adc-gain-delta="-1">
                <div class="gbs-icon">add_circle_outline</div>
                <div>R</div>
              </button>
            </div>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control gbs-adc-gain-btn" gbs-adc-gain-channel="g" gbs-adc-gain-delta="1">
                <div class="gbs-icon">remove_circle_outline</div>
                <div>G</div>
              </button>
              <div class="gbs-button gbs-button__control" style="flex-grow: 0; text-align: center" gbs-adc-gain-readout="g">—</div>
              <button class="gbs-button gbs-button__control gbs-adc-gain-btn" gbs-adc-gain-channel="g" gbs-adc-gain-delta="-1">
                <div class="gbs-icon">add_circle_outline</div>
                <div>G</div>
              </button>
            </div>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control gbs-adc-gain-btn" gbs-adc-gain-channel="b" gbs-adc-gain-delta="1">
                <div class="gbs-icon">remove_circle_outline</div>
                <div>B</div>
              </button>
              <div class="gbs-button gbs-button__control" style="flex-grow: 0; text-align: center" gbs-adc-gain-readout="b">—</div>
              <button class="gbs-button gbs-button__control gbs-adc-gain-btn" gbs-adc-gain-channel="b" gbs-adc-gain-delta="-1">
                <div class="gbs-icon">add_circle_outline</div>
                <div>B</div>
              </button>
            </div>
          </fieldset>
          <fieldset class="gbs-fieldset gbs-controls">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">control_camera</div>
              <div>Controles de Imagem</div>
            </legend>
            <div class="gbs-flex">
              <button
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
                gbs-control-key="left"
              >
                keyboard_arrow_left
              </button>
              <button
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
                gbs-control-key="up"
              >
                keyboard_arrow_up
              </button>
              <button
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
                gbs-control-key="right"
              >
                keyboard_arrow_right
              </button>
            </div>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control gbs-icon" disabled>
                south_west
              </button>
              <button
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
                gbs-control-key="down"
              >
                keyboard_arrow_down
              </button>
              <button class="gbs-button gbs-button__control gbs-icon" disabled>
                south_east
              </button>
            </div>
            <div class="gbs-flex">
              <button
                class="gbs-button gbs-button__control"
                gbs-control-target="move"
                active
              >
                <div class="gbs-icon">open_with</div>
                <div>mover</div>
              </button>
              <button
                class="gbs-button gbs-button__control"
                gbs-control-target="scale"
              >
                <div class="gbs-icon">zoom_out_map</div>
                <div>escalar</div>
              </button>
              <button
                class="gbs-button gbs-button__control"
                gbs-control-target="borders"
              >
                <div class="gbs-icon">crop_free</div>
                <div>bordas</div>
              </button>
            </div>
          </fieldset>
          <fieldset class="gbs-fieldset gbs-controls__desktop">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">control_camera</div>
              <div>Controles de Imagem</div>
            </legend>
            <div class="gbs-flex">
              <button
                gbs-message="7"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_left
              </button>
              <button
                gbs-message="*"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_up
              </button>
              <button
                gbs-message="6"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_right
              </button>
            </div>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control" active>
                <div class="gbs-icon">open_with</div>
                <div>mover</div>
              </button>
              <button
                gbs-message="/"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_down
              </button>
              <button class="gbs-button gbs-button__control gbs-icon" disabled>
                south_east
              </button>
            </div>

            <div class="gbs-flex">
              <button
                gbs-message="h"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_left
              </button>
              <button
                gbs-message="4"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_up
              </button>
              <button
                gbs-message="z"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_right
              </button>
            </div>

            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control" active>
                <div class="gbs-icon">zoom_out_map</div>
                <div>escalar</div>
              </button>
              <button
                gbs-message="5"
                gbs-message-type="action"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_down
              </button>
              <button class="gbs-button gbs-button__control gbs-icon" disabled>
                south_east
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="B"
                gbs-message-type="user"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_left
              </button>
              <button
                gbs-message="C"
                gbs-message-type="user"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_up
              </button>
              <button
                gbs-message="A"
                gbs-message-type="user"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_right
              </button>
            </div>

            <div class="gbs-flex gbs-margin__bottom--16">
              <button
                class="gbs-button gbs-button__control"
                gbs-control-target="borders"
                active
              >
                <div class="gbs-icon">crop_free</div>
                <div>bordas</div>
              </button>
              <button
                gbs-message="D"
                gbs-message-type="user"
                gbs-click="repeat"
                class="gbs-button gbs-button__control gbs-icon gbs-button__secondary"
              >
                keyboard_arrow_down
              </button>
              <button class="gbs-button gbs-button__control gbs-icon" disabled>
                south_east
              </button>
            </div>
          </fieldset>

          <!-- <fieldset class="gbs-fieldset controls-desktop">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">control_camera</div>
              <div>Controles de Imagem</div>
            </legend>
            <div class="">
              <button active class="gbs-button direction">
                <div class="gbs-icon">open_with</div>
                <div>mover</div>
              </button>
              <div class="keyboard">
                <div>
                  <button
                    gbs-message="7"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_left
                  </button>
                  <button
                    gbs-message="*"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_up
                  </button>
                  <button
                    gbs-message="6"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_right
                  </button>
                </div>

                <div class="gbs-margin__bottom--16">
                  <button class="gbs-button gbs-icon" disabled>
                    south_west
                  </button>
                  <button
                    gbs-message="/"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_down
                  </button>
                  <button class="gbs-button gbs-icon" disabled>
                    south_east
                  </button>
                </div>
              </div>
            </div>
            <div class="">
              <button class="gbs-button direction" active>
                <div class="gbs-icon">zoom_out_map</div>
                <div>escalar</div>
              </button>
              <div class="keyboard">
                <div>
                  <button
                    gbs-message="h"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_left
                  </button>
                  <button
                    gbs-message="4"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_up
                  </button>
                  <button
                    gbs-message="z"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_right
                  </button>
                </div>

                <div class="gbs-margin__bottom--16">
                  <button class="gbs-button gbs-icon" disabled>
                    south_west
                  </button>
                  <button
                    gbs-message="5"
                    gbs-message-type="action"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_down
                  </button>
                  <button class="gbs-button gbs-icon" disabled>
                    south_east
                  </button>
                </div>
              </div>
            </div>
            <div class="">
              <button class="gbs-button direction" active>
                <div class="gbs-icon">crop_free</div>
                <div>bordas</div>
              </button>
              <div class="keyboard">
                <div>
                  <button
                    gbs-message="B"
                    gbs-message-type="user"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_left
                  </button>
                  <button
                    gbs-message="C"
                    gbs-message-type="user"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_up
                  </button>
                  <button
                    gbs-message="A"
                    gbs-message-type="user"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_right
                  </button>
                </div>

                <div class="gbs-margin__bottom--16">
                  <button class="gbs-button gbs-icon" disabled>
                    south_west
                  </button>
                  <button
                    gbs-message="D"
                    gbs-message-type="user"
                    gbs-click="repeat"
                    class="gbs-button gbs-icon gbs-button__secondary"
                  >
                    keyboard_arrow_down
                  </button>
                  <button class="gbs-button gbs-icon" disabled>
                    south_east
                  </button>
                </div>
              </div>
            </div>
          </fieldset> -->
        </section>

        <section name="filters" hidden>
          <fieldset class="gbs-fieldset filters">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">blur_on</div>
              <div>Filtros</div>
            </legend>
            <div class="gbs-margin__bottom--16">
              <div class="gbs-flex gbs-margin__bottom--16">
                <button
                  gbs-message="7"
                  gbs-message-type="user"
                  gbs-click="normal"
                  gbs-toggle="scanlines"
                  class="gbs-button gbs-button__control gbs-button__secondary"
                >
                  <div class="gbs-icon">gradient</div>
                  <div>scanlines</div>
                </button>
                <button
                  gbs-message="K"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-button gbs-button__control"
                >
                  <div class="gbs-icon">gradientbolt</div>
                  <div>intensidade</div>
                </button>
                <button
                  gbs-message="m"
                  gbs-message-type="user"
                  gbs-click="normal"
                  gbs-toggle="vdsLineFilter"
                  class="gbs-button gbs-button__control gbs-button__secondary"
                >
                  <div class="gbs-icon">power_input</div>
                  <div>filtro de linha</div>
                </button>
              </div>
              <ul class="gbs-help">
                <!-- prettier-ignore -->
                <li>Scanlines só funcionam com fontes 240p, ou 480i com desentrelaçamento Bob.</li>
                <li>O filtro de linha elimina artefatos de pixels quadriculados ao escalar acima de 480p, recomendado.</li>
                <li>Realce de brilho das scanlines compensa a perda de brilho/contraste que o efeito causa (parecido com o brilho dos fósforos numa CRT de verdade). 0 = desativado.</li>
              </ul>
              <div class="gbs-flex gbs-margin__bottom--16">
                <button class="gbs-button gbs-button__control gbs-scanline-boost-btn" gbs-scanline-boost-delta="-4">
                  <div class="gbs-icon">remove_circle_outline</div>
                  <div>realce scanlines</div>
                </button>
                <div class="gbs-button gbs-button__control" style="flex-grow: 0; text-align: center" gbs-scanline-boost-readout>—</div>
                <button class="gbs-button gbs-button__control gbs-scanline-boost-btn" gbs-scanline-boost-delta="4">
                  <div class="gbs-icon">add_circle_outline</div>
                  <div>realce scanlines</div>
                </button>
              </div>
              <div class="gbs-flex">
                <button
                  gbs-message="f"
                  gbs-message-type="action"
                  gbs-click="normal"
                  gbs-toggle="peaking"
                  class="gbs-button gbs-button__control gbs-button__secondary"
                >
                  <div class="gbs-icon">blur_linear</div>
                  <div>realce</div>
                </button>
                <button
                  gbs-message="V"
                  gbs-message-type="action"
                  gbs-click="normal"
                  gbs-toggle="step"
                  class="gbs-button gbs-button__control gbs-button__secondary"
                >
                  <div class="gbs-icon">grain</div>
                  <div>resposta de degrau</div>
                </button>
              </div>
              <ul class="gbs-help">
                <!-- prettier-ignore -->
                <li>Realce aumenta o contraste em transições horizontais de brilho, recomendado.</li>
                <li>Resposta de degrau aumenta a nitidez das transições horizontais de cor, recomendado.</li>
              </ul>
            </div>
          </fieldset>
        </section>

        <section name="preferences" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">tune</div>
              <div>Configurações</div>
            </legend>
            <table class="gbs-preferences">
              <tr>
                <td>
                  Perfis Combinados
                  <ul class="gbs-help">
                    <!-- prettier-ignore -->
                    <li>Se ativo, usa 1280x960 para NTSC 60 e 1280x1024 para PAL 50 (não se aplica para perfis 720p / 1080p).</li>
                  </ul>
                </td>
                <td
                  gbs-message="Z"
                  gbs-message-type="action"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="matched"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td>
                  Altura Total
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Alguns perfis não usam toda a resolução vertical de saída, deixando algumas linhas pretas.</li>
                    <li>Com Altura Total ativa, esses perfis escalam para preencher mais a altura da tela.</li>
                    <li>(Atualmente afeta apenas 1920 x 1080)</li>
                  </ul>
                </td>
                <td
                  gbs-message="v"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="fullHeight"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td>
                  Baixa Res: Usar Upscaling
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Entrada VGA de baixa resolução: Passagem direta ou Upscale</li>
                    <li>Fontes de baixa resolução podem ser passadas diretamente ou escaladas.</li>
                    <li>Upscaling pode ter problemas de borda/escala, mas é mais compatível com telas.</li>
                    <li>Taxas de atualização diferentes de 60Hz ainda não têm bom suporte.</li>
                    <li>"Baixa resolução" hoje é definida como menor ou igual a 640x480 (525 linhas ativas).</li>
                  </ul>
                </td>
                <td
                  gbs-message="x"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="preferScalingRgbhv"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td>
                  Saída RGBHV/Componente
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>O modo de saída padrão é RGBHV, ideal para cabos VGA ou conversores HDMI.</li>
                    <li>Um modo experimental YPbPr também pode ser selecionado. A compatibilidade ainda é instável.</li>
                  </ul>
                </td>
                <td
                  gbs-message="L"
                  gbs-message-type="action"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="wantOutputComponent"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td colspan="2">
                  Entrada Manual
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Por padrão a entrada (RGB/RGBS ou Componente) é detectada automaticamente. Force uma delas se você tem as duas fontes conectadas ao mesmo tempo e quer trocar manualmente.</li>
                  </ul>
                  <div class="gbs-flex">
                    <button class="gbs-button gbs-button__control gbs-input-lock-btn" gbs-input-lock-value="0">
                      <div>Automático</div>
                    </button>
                    <button class="gbs-button gbs-button__control gbs-input-lock-btn" gbs-input-lock-value="1">
                      <div>RGB/RGBS</div>
                    </button>
                    <button class="gbs-button gbs-button__control gbs-input-lock-btn" gbs-input-lock-value="2">
                      <div>Componente</div>
                    </button>
                  </div>
                </td>
              </tr>
              <tr>
                <td>
                  Taxa de Quadros: Forçar PAL 50Hz para 60Hz
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Se sua TV não suporta fontes 50Hz (exibindo formato desconhecido, independente do perfil), tente esta opção.
                    </li>
                    <li>O frame rate não será tão suave. Requer reinício.</li>
                  </ul>
                </td>
                <td
                  gbs-message="0"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="palForce60"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td>
                  Desabilitar Gerador de Clock Externo
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Por padrão o gerador de clock externo é ativado quando instalado.</li>
                    <li>Você pode desativá-lo se tiver problemas com outras opções, como Forçar PAL 50Hz para 60Hz.
                    Requer reinício.</li>
                  </ul>
                </td>
                <td
                  gbs-message="X"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="disableExternalClockGenerator"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td>
                  Calibração ADC
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>O Gbscontrol calibra os offsets do ADC no boot.</li>
                    <li>Em caso de problemas de desvio de cor, tente desabilitar esta função.</li>
                  </ul>
                </td>
                <td
                  gbs-message="w"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="enableCalibrationADC"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td colspan="2" class="gbs-preferences__child">
                  Trava de FrameTime
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Esta opção mantém alinhados os tempos de entrada e saída, corrigindo a linha de "tearing" horizontal que pode aparecer.</li>
                    <li>Dois métodos disponíveis. Tente alternar se a tela ficar preta ou deslocar verticalmente.</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td class="gbs-padding__left-16">Travar FrameTime</td>
                <td
                  class="gbs-icon"
                  gbs-message="5"
                  gbs-message-type="user"
                  gbs-click="normal"
                  gbs-toggle-switch="frameTimeLock"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td class="gbs-padding__left-16">Alternar Método de Trava</td>
                <td
                  class="gbs-icon"
                  gbs-message="i"
                  gbs-message-type="user"
                  gbs-click="normal"
                  style="cursor: pointer"
                >
                  swap_horiz
                </td>
              </tr>
              <tr>
                <td colspan="2" class="gbs-preferences__child">
                  Método de Desentrelaçamento
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>O Gbscontrol detecta conteúdo entrelaçado e alterna o desentrelaçamento automaticamente.</li>
                    <li>Método Bob: praticamente sem desentrelaçamento, sem lag adicional mas cintila, pode combinar com scanlines</li>
                    <li>Adaptativo por Movimento: remove o flicker mas mostra alguns artefatos em detalhes em movimento</li>
                    <li>Se possível, configure a fonte para saída progressiva. Caso contrário, recomenda-se o Adaptativo por Movimento.</li>
                  </ul>
                </td>
              </tr>
              <tr>
                <td class="gbs-padding__left-16">Adaptativo por Movimento</td>
                <td
                  gbs-message="r"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="bob"
                >
                  toggle_off
                </td>
              </tr>
              <tr>
                <td class="gbs-padding__left-16">Bob</td>
                <td
                  gbs-message="q"
                  gbs-message-type="user"
                  gbs-click="normal"
                  class="gbs-icon"
                  gbs-toggle-switch="motionAdaptive"
                >
                  toggle_off
                </td>
              </tr>
              <tr gbs-dev-switch>
                <td>
                  Modo Desenvolvedor
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Habilita o menu de desenvolvedor com várias ferramentas de debug</li>
                  </ul>
                </td>
                <td class="gbs-icon">toggle_off</td>
              </tr>
              <tr gbs-slot-custom-filters>
                <td>
                  Salvar Filtros por Slot
                  <!-- prettier-ignore -->
                  <ul class="gbs-help">
                    <li>Quando ativo, slots salvos recuperam suas próprias preferências de filtro.</li>
                    <li>Quando desativo, slots salvos mantêm os filtros atuais.</li>
                  </ul>
                </td>
                <td class="gbs-icon">toggle_off</td>
              </tr>
            </table>
          </fieldset>
        </section>

        <section name="developer" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">input</div>
              <div>Developer</div>
            </legend>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button" gbs-output-toggle>
                <div class="gbs-icon">code</div>
                <div>Toggle Console</div>
              </button>
            </div>
            <div class="gbs-flex gbs-margin__bottom--16">
              <button
                gbs-message="-"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">keyboard_arrow_left</div>
                <div>MEM Left</div>
              </button>
              <button
                gbs-message="+"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">keyboard_arrow_right</div>
                <div>MEM Right</div>
              </button>
              <button
                gbs-message="1"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">keyboard_arrow_left</div>
                <div>HS Left</div>
              </button>
              <button
                gbs-message="0"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">keyboard_arrow_right</div>
                <div>HS Right</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="e"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">list</div>
                <div>List Options</div>
              </button>
              <button
                gbs-message="i"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">info</div>
                <div>Print Info</div>
              </button>
              <button
                gbs-message=","
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">alarm</div>
                <div>Get Video Timings</div>
              </button>
            </div>

            <div class="gbs-flex">
              <button
                gbs-message="F"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button gbs-margin__bottom--16"
              >
                <div class="gbs-icon">add_a_photo</div>
                <div>Freeze Capture</div>
              </button>
            </div>

            <div class="gbs-flex">
              <button
                gbs-message="F"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">wb_sunny</div>
                <div>ADC Filter</div>
              </button>
              <button
                gbs-message="l"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">memory</div>
                <div>Cycle SDRAM</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="D"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">bug_report</div>
                <div>Debug View</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="a"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">add_circle_outline</div>
                <div>HTotal++</div>
              </button>
              <button
                gbs-message="A"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">remove_circle_outline</div>
                <div>HTotal--</div>
              </button>
              <button
                gbs-message="."
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">sync_problem</div>
                <div>Resync HTotal</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="n"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">calculate</div>
                <div>PLL divider++</div>
              </button>
              <button
                gbs-message="8"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">invert_colors</div>
                <div>Invert Sync</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="m"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">devices_other</div>
                <div>SyncWatcher</div>
              </button>

              <button
                gbs-message="l"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">settings_backup_restore</div>
                <div>SyncProcessor</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="o"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">insights</div>
                <div>Oversampling</div>
              </button>
              <button
                gbs-message="S"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">settings_input_hdmi</div>
                <div>60/50Hz HDMI</div>
              </button>

              <button
                gbs-message="E"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">bug_report</div>
                <div>IF Auto Offset</div>
              </button>
            </div>
            <div class="gbs-flex">
              <button
                gbs-message="z"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button"
              >
                <div class="gbs-icon">format_align_justify</div>
                <div>SOG Level--</div>
              </button>

              <button
                gbs-message="q"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__secondary"
              >
                <div class="gbs-icon">model_training</div>
                <div>Reset Chip</div>
              </button>
            </div>
          </fieldset>
        </section>

        <section name="system" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">bolt</div>
              <div>Sistema</div>
            </legend>
            <div class="gbs-flex">
              <button
                gbs-message="c"
                gbs-message-type="action"
                gbs-click="normal"
                class="gbs-button gbs-button__control"
              >
                <div class="gbs-icon">system_update_alt</div>
                <div>Habilitar OTA</div>
              </button>
              <button
                gbs-message="a"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button gbs-button__control"
              >
                <div class="gbs-icon">settings_backup_restore</div>
                <div>Reiniciar</div>
              </button>
              <button
                gbs-message="1"
                gbs-message-type="user"
                gbs-click="normal"
                class="gbs-button gbs-button__control gbs-button__secondary"
              >
                <div class="gbs-icon">settings_backup_restore offline_bolt</div>
                <div>Restaurar Padrões</div>
              </button>
            </div>
          </fieldset>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend gbs-fieldset__legend--help">
              <div class="gbs-icon">sd_card</div>
              <div>Cópia [para o mesmo aparelho]</div>
            </legend>
            <!-- prettier-ignore -->
            <ul class="gbs-help">
              <li>Cópia / Restauração dos arquivos de configuração</li>
              <li>A cópia é válida apenas no aparelho atual</li>
              <!-- <li>A cópia é válida entre aparelhos com a mesma revisão de hardware</li> -->
            </ul>
            <div class="gbs-flex">
              <button
                class="gbs-button gbs-button__control gbs-button__secondary gbs-backup-button"
              >
                <div class="gbs-icon">cloud_download</div>
                <div gbs-progress gbs-progress-backup>Baixar</div>
              </button>
              <button
                class="gbs-button gbs-button__control gbs-button__secondary"
              >
                <div class="gbs-icon">cloud_upload</div>
                <input type="file" class="gbs-backup-input" accept=".bin"/>
                <div gbs-progress gbs-progress-restore>Restaurar</div>
              </button>
            </div>
          </fieldset>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">wifi</div>
              <div>Wi-Fi</div>
            </legend>

            <div class="gbs-flex gbs-margin__bottom--16">
              <button class="gbs-button gbs-button__control" gbs-wifi-ap>
                <div class="gbs-icon">location_on</div>
                <div>Ponto de Acesso</div>
              </button>
              <button class="gbs-button gbs-button__control" gbs-wifi-station>
                <div class="gbs-icon">radio</div>
                <div gbs-wifi-station-ssid>Estação</div>
              </button>
            </div>
            <fieldset class="gbs-fieldset" gbs-wifi-list hidden>
              <legend class="gbs-fieldset__legend">
                <div class="gbs-icon">router</div>
                <div>Selecionar Rede</div>
              </legend>
              <table class="gbs-wifi__list"></table>
            </fieldset>
            <fieldset class="gbs-fieldset gsb-wifi__connect" hidden>
              <legend class="gbs-fieldset__legend">
                <div class="gbs-icon">login</div>
                <div>Conectar à Rede</div>
              </legend>
              <div class="gbs-flex">
                <input
                  class="gbs-button gbs-wifi__input"
                  placeholder="SSID"
                  type="text"
                  readonly
                  gbs-input="ssid"
                />
              </div>
              <div class="gbs-flex">
                <input
                  class="gbs-button gbs-wifi__input"
                  placeholder="senha"
                  type="password"
                  gbs-input="password"
                />
              </div>
              <div class="gbs-flex">
                <button
                  gbs-wifi-connect-button
                  class="gbs-button gbs-button__control gbs-button__secondary"
                >
                  <div class="gbs-icon">network_check</div>
                  <div>Conectar</div>
                </button>
              </div>
            </fieldset>
          </fieldset>
        </section>
        <section name="prompt" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">keyboard</div>
              <div gbs-prompt-content>Prompt</div>
            </legend>
            <div class="gbs-flex gbs-margin__bottom--16">
              <input
                class="gbs-button"
                type="text"
                gbs-input="prompt-input"
                maxlength="25"
              />
            </div>
            <div class="gbs-flex">
              <button gbs-prompt-cancel class="gbs-button gbs-button__control">
                <div class="gbs-icon">close</div>
                <div>CANCELAR</div>
              </button>
              <button
                gbs-prompt-ok
                class="gbs-button gbs-button__control gbs-button__secondary"
              >
                <div class="gbs-icon">done</div>
                <div>OK</div>
              </button>
            </div>
          </fieldset>
        </section>
        <section name="alert" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">warning</div>
              <div>ALERTA</div>
            </legend>
            <div
              class="gbs-flex gbs-padding__hor-16 gbs-modal__message"
              gbs-alert-content
            ></div>
            <div class="gbs-flex">
              <button class="gbs-button gbs-button__control" disabled></button>
              <button
                gbs-alert-ok
                class="gbs-button gbs-button__control gbs-button__secondary"
              >
                <div class="gbs-icon">done</div>
                <div>OK</div>
              </button>
            </div>
          </fieldset>
        </section>
        <section name="iconpicker" hidden>
          <fieldset class="gbs-fieldset">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">stadia_controller</div>
              <div>Escolha um ícone</div>
            </legend>
            <div class="gbs-flex gbs-icon-picker" gbs-icon-picker-grid></div>
            <div class="gbs-flex">
              <button gbs-icon-picker-cancel class="gbs-button gbs-button__control">
                <div class="gbs-icon">close</div>
                <div>CANCELAR</div>
              </button>
            </div>
          </fieldset>
        </section>
        <div class="gbs-output">
          <fieldset class="gbs-fieldset gbs-fieldset-output">
            <legend class="gbs-fieldset__legend">
              <div class="gbs-icon">code</div>
              <div>Saída</div>
            </legend>
            <div class="gbs-flex gbs-margin__bottom--16" gbs-output-clear>
              <button class="gbs-button gbs-icon">delete_outline</button>
            </div>
            <div class="gbs-flex">
              <textarea
                id="outputTextArea"
                class="gbs-output__textarea"
              ></textarea>
            </div>
          </fieldset>
        </div>
      </div>
      <div class="gbs-loader"><img /></div>
    </div>
    <div class="gbs-wifi-warning" id="websocketWarning">
      <div class="gbs-icon blink_me">signal_wifi_off</div>
    </div>
    <script>
      ${js}
    </script>
  </body>
</html>
