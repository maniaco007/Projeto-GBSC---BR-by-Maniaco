const Structs = {
    slots: [
        { name: "name", type: "string", size: 25 },
        { name: "presetID", type: "byte", size: 1 },
        { name: "scanlines", type: "byte", size: 1 },
        { name: "scanlinesStrength", type: "byte", size: 1 },
        { name: "slot", type: "byte", size: 1 },
        { name: "wantVdsLineFilter", type: "byte", size: 1 },
        { name: "wantStepResponse", type: "byte", size: 1 },
        { name: "wantPeaking", type: "byte", size: 1 },
    ],
};
const StructParser = {
    pos: 0,
    parseStructArray(buff, structsDescriptors, struct) {
        const currentStruct = structsDescriptors[struct];
        this.pos = 0;
        buff = new Uint8Array(buff);
        if (currentStruct) {
            const structSize = StructParser.getSize(structsDescriptors, struct);
            return [...Array(buff.byteLength / structSize)].map(() => {
                return currentStruct.reduce((acc, structItem) => {
                    acc[structItem.name] = this.getValue(buff, structItem);
                    return acc;
                }, {});
            });
        }
        return null;
    },
    getValue(buff, structItem) {
        switch (structItem.type) {
            case "byte":
                return buff[this.pos++];
            case "string":
                const currentPos = this.pos;
                this.pos += structItem.size;
                return [...Array(structItem.size)]
                    .map(() => " ")
                    .map((_char, index) => {
                    if (buff[currentPos + index] > 31) {
                        return String.fromCharCode(buff[currentPos + index]);
                    }
                    return "";
                })
                    .join("")
                    .trim();
        }
    },
    getSize(structsDescriptors, struct) {
        const currentStruct = structsDescriptors[struct];
        return currentStruct.reduce((acc, prop) => {
            acc += prop.size;
            return acc;
        }, 0);
    },
};
/* GBSControl Global Object*/
const GBSControl = {
    buttonMapping: {
        1: "button1280x960",
        2: "button1280x1024",
        3: "button1280x720",
        4: "button720x480",
        5: "button1920x1080",
        6: "button15kHzScaleDown",
        8: "buttonSourcePassThrough",
        9: "buttonLoadCustomPreset",
    },
    controlKeysMobileMode: "move",
    controlKeysMobile: {
        move: {
            type: "loadDoc",
            left: "7",
            up: "*",
            right: "6",
            down: "/",
        },
        scale: {
            type: "loadDoc",
            left: "h",
            up: "4",
            right: "z",
            down: "5",
        },
        borders: {
            type: "loadUser",
            left: "B",
            up: "C",
            right: "A",
            down: "D",
        },
    },
    dataQueued: 0,
    isWsActive: false,
    maxSlots: 72,
    queuedText: "",
    scanSSIDDone: false,
    serverIP: "",
    slotIcons: new Uint8Array(72),
    slotConnectors: new Uint8Array(72),
    structs: null,
    timeOutWs: 0,
    ui: {
        backupButton: null,
        backupInput: null,
        customSlotFilters: null,
        developerSwitch: null,
        loader: null,
        outputClear: null,
        presetButtonList: null,
        progressBackup: null,
        progressRestore: null,
        slotButtonList: null,
        slotContainer: null,
        terminal: null,
        toggleList: null,
        toggleSwichList: null,
        updateBanner: null,
        webSocketConnectionWarning: null,
        wifiConnect: null,
        wifiConnectButton: null,
        wifiList: null,
        wifiListTable: null,
        wifiPasswordInput: null,
        wifiSSDInput: null,
        wifiApButton: null,
        wifiStaButton: null,
        wifiStaSSID: null,
        alert: null,
        alertOk: null,
        alertContent: null,
        prompt: null,
        promptOk: null,
        promptCancel: null,
        promptContent: null,
        promptInput: null,
        iconPicker: null,
        iconPickerGrid: null,
        iconPickerCancel: null,
        iconPickerOk: null,
    },
    updateTerminalTimer: 0,
    webSocketServerUrl: "",
    wifi: {
        mode: "ap",
        ssid: "",
    },
    ws: null,
    wsCheckTimer: 0,
    wsConnectCounter: 0,
    wsNoSuccessConnectingCounter: 0,
    wsTimeout: 0,
};
/** websocket services */
const checkWebSocketServer = () => {
    if (!GBSControl.isWsActive) {
        if (GBSControl.ws) {
            /*
                              0     CONNECTING
                              1     OPEN
                              2     CLOSING
                              3     CLOSED
                              */
            switch (GBSControl.ws.readyState) {
                case 1:
                case 2:
                    GBSControl.ws.close();
                    break;
                case 3:
                    GBSControl.ws = null;
                    break;
            }
        }
        if (!GBSControl.ws) {
            createWebSocket();
        }
    }
};
const timeOutWs = () => {
    console.log("timeOutWs");
    if (GBSControl.ws) {
        GBSControl.ws.close();
    }
    GBSControl.isWsActive = false;
    displayWifiWarning(true);
};
const createWebSocket = () => {
    if (GBSControl.ws && checkReadyState()) {
        return;
    }
    GBSControl.wsNoSuccessConnectingCounter = 0;
    GBSControl.ws = new WebSocket(GBSControl.webSocketServerUrl, ["arduino"]);
    GBSControl.ws.onopen = () => {
        console.log("ws onopen");
        displayWifiWarning(false);
        GBSControl.wsConnectCounter++;
        clearTimeout(GBSControl.wsTimeout);
        GBSControl.wsTimeout = setTimeout(timeOutWs, 6000);
        GBSControl.isWsActive = true;
        GBSControl.wsNoSuccessConnectingCounter = 0;
    };
    GBSControl.ws.onclose = () => {
        console.log("ws.onclose");
        clearTimeout(GBSControl.wsTimeout);
        GBSControl.isWsActive = false;
    };
    GBSControl.ws.onmessage = (message) => {
        clearTimeout(GBSControl.wsTimeout);
        GBSControl.wsTimeout = setTimeout(timeOutWs, 4000);
        GBSControl.isWsActive = true;
        try {
            const [messageDataAt0, messageDataAt1, messageDataAt2, messageDataAt3, messageDataAt4, messageDataAt5,] = message.data;
            if (messageDataAt0 != "#") {
                GBSControl.queuedText += message.data;
                GBSControl.dataQueued += message.data.length;
                if (GBSControl.dataQueued >= 70000) {
                    GBSControl.ui.terminal.value = "";
                    GBSControl.dataQueued = 0;
                }
            }
            else {
                const presetId = GBSControl.buttonMapping[messageDataAt1];
                const presetEl = document.querySelector(`[gbs-element-ref="${presetId}"]`);
                const activePresetButton = presetEl
                    ? presetEl.getAttribute("gbs-element-ref")
                    : "none";
                GBSControl.ui.presetButtonList.forEach(toggleButtonActive(activePresetButton));
                const slotId = "slot-" + messageDataAt2;
                const activeSlotButton = document.querySelector(`[gbs-element-ref="${slotId}"]`);
                if (activeSlotButton) {
                    GBSControl.ui.slotButtonList.forEach(toggleButtonActive(slotId));
                }
                if (messageDataAt3 && messageDataAt4 && messageDataAt5) {
                    const optionByte0 = messageDataAt3.charCodeAt(0);
                    const optionByte1 = messageDataAt4.charCodeAt(0);
                    const optionByte2 = messageDataAt5.charCodeAt(0);
                    const optionButtonList = [
                        ...nodelistToArray(GBSControl.ui.toggleList),
                        ...nodelistToArray(GBSControl.ui.toggleSwichList),
                    ];
                    const toggleMethod = (button, mode) => {
                        if (button.tagName === "TD") {
                            button.innerText = mode ? "toggle_on" : "toggle_off";
                        }
                        button = button.tagName !== "TD" ? button : button.parentElement;
                        if (mode) {
                            button.setAttribute("active", "");
                        }
                        else {
                            button.removeAttribute("active");
                        }
                    };
                    optionButtonList.forEach((button) => {
                        const toggleData = button.getAttribute("gbs-toggle") ||
                            button.getAttribute("gbs-toggle-switch");
                        switch (toggleData) {
                            case "adcAutoGain":
                                toggleMethod(button, (optionByte0 & 0x01) == 0x01);
                                break;
                            case "scanlines":
                                toggleMethod(button, (optionByte0 & 0x02) == 0x02);
                                break;
                            case "vdsLineFilter":
                                toggleMethod(button, (optionByte0 & 0x04) == 0x04);
                                break;
                            case "peaking":
                                toggleMethod(button, (optionByte0 & 0x08) == 0x08);
                                break;
                            case "palForce60":
                                toggleMethod(button, (optionByte0 & 0x10) == 0x10);
                                break;
                            case "wantOutputComponent":
                                toggleMethod(button, (optionByte0 & 0x20) == 0x20);
                                break;
                            /** 1 */
                            case "matched":
                                toggleMethod(button, (optionByte1 & 0x01) == 0x01);
                                break;
                            case "frameTimeLock":
                                toggleMethod(button, (optionByte1 & 0x02) == 0x02);
                                break;
                            case "motionAdaptive":
                                toggleMethod(button, (optionByte1 & 0x04) == 0x04);
                                break;
                            case "bob":
                                toggleMethod(button, (optionByte1 & 0x04) != 0x04);
                                break;
                            // case "tap6":
                            //   toggleMethod(button, (optionByte1 & 0x08) != 0x04);
                            //   break;
                            case "step":
                                toggleMethod(button, (optionByte1 & 0x10) == 0x10);
                                break;
                            case "fullHeight":
                                toggleMethod(button, (optionByte1 & 0x20) == 0x20);
                                break;
                            /** 2 */
                            case "enableCalibrationADC":
                                toggleMethod(button, (optionByte2 & 0x01) == 0x01);
                                break;
                            case "preferScalingRgbhv":
                                toggleMethod(button, (optionByte2 & 0x02) == 0x02);
                                break;
                            case "disableExternalClockGenerator":
                                toggleMethod(button, (optionByte2 & 0x04) == 0x04);
                                break;
                        }
                    });
                }
            }
        }
        catch (e) {
            console.warn("Malformed websocket message", e);
            return;
        }
    };
};
const checkReadyState = () => {
    if (GBSControl.ws.readyState == 2) {
        GBSControl.wsNoSuccessConnectingCounter++;
        if (GBSControl.wsNoSuccessConnectingCounter >= 7) {
            console.log("ws still closing, force close");
            GBSControl.ws = null;
            GBSControl.wsNoSuccessConnectingCounter = 0;
            /* fall through */
            createWebSocket();
            return false;
        }
        else {
            return true;
        }
    }
    else if (GBSControl.ws.readyState == 0) {
        GBSControl.wsNoSuccessConnectingCounter++;
        if (GBSControl.wsNoSuccessConnectingCounter >= 14) {
            console.log("ws still connecting, retry");
            GBSControl.ws.close();
            GBSControl.wsNoSuccessConnectingCounter = 0;
        }
        return true;
    }
    else {
        return true;
    }
};
const createIntervalChecks = () => {
    GBSControl.wsCheckTimer = setInterval(checkWebSocketServer, 500);
    GBSControl.updateTerminalTimer = setInterval(updateTerminal, 50);
};
/* API services */
const loadDoc = (link) => {
    return fetch(`http://${GBSControl.serverIP}/sc?${link}&nocache=${new Date().getTime()}`);
};
const loadUser = (link) => {
    if (link == "a" || link == "1") {
        GBSControl.isWsActive = false;
        GBSControl.ui.terminal.value += "\nRestart\n";
        GBSControl.ui.terminal.scrollTop = GBSControl.ui.terminal.scrollHeight;
    }
    return fetch(`http://${GBSControl.serverIP}/uc?${link}&nocache=${new Date().getTime()}`);
};
/** SLOT management */
const savePreset = () => {
    const currentSlot = document.querySelector('[gbs-role="slot"][active]');
    if (!currentSlot) {
        return;
    }
    const key = currentSlot.getAttribute("gbs-element-ref");
    const currentIndex = currentSlot.getAttribute("gbs-slot-id");
    const currentIconId = GBSControl.slotIcons[currentIndex] || 0;
    const currentConnector = GBSControl.slotConnectors[currentIndex] || 1;
    gbsPrompt(t("Nome do slot"), GBSControl.structs.slots[currentIndex].name || key, currentConnector)
        .then(({ name: currentName, connector }) => {
        if (currentName && currentName.trim() !== "Empty") {
            currentSlot.setAttribute("gbs-name", currentName);
            gbsIconPrompt(currentIconId)
                .catch(() => currentIconId)
                .then((iconId) => {
                fetch(`/slot/save?index=${currentIndex}&name=${currentName.substring(0, 24)}&icon=${iconId}&conn=${connector}&${+new Date()}`)
                    .then(() => {
                    loadUser("4").then(() => {
                        setTimeout(() => {
                            fetchSlotNames().then((success) => {
                                if (success) {
                                    updateSlotNames();
                                }
                            });
                        }, 500);
                    });
                })
                    .catch(() => {
                    gbsAlert(t("Erro ao salvar o preset")).catch(() => { });
                });
            });
        }
    })
        .catch(() => { });
};
const loadPreset = () => {
    loadUser("3").then(() => {
        if (GBSStorage.read("customSlotFilters") === true) {
            setTimeout(() => {
                fetch(`/gbs/restore-filters?${+new Date()}`);
            }, 250);
        }
    });
};
const deletePreset = () => {
    const currentSlot = document.querySelector('[gbs-role="slot"][active]');
    if (!currentSlot) {
        return;
    }
    const currentIndex = parseInt(currentSlot.getAttribute("gbs-slot-id") || "0", 10);
    const slotData = GBSControl.structs.slots[currentIndex];
    const slotName = slotData && slotData.name ? slotData.name.trim() : "";
    if (!slotName || slotName === "Empty") {
        return;
    }
    const ok = confirm(isEn()
        ? `Delete preset "${slotName}"?\n\nThis removes all files of this slot and shifts the following slots up.`
        : `Apagar o preset "${slotName}"?\n\nIsso remove todos os arquivos desse slot e desloca os slots seguintes para cima.`);
    if (!ok) {
        return;
    }
    fetch(`/slot/remove?1&${+new Date()}`)
        .then((r) => r.json())
        .then((success) => {
        if (success) {
            setTimeout(() => {
                fetchSlotNames().then((ok) => {
                    if (ok)
                        updateSlotNames();
                });
            }, 300);
        }
        else {
            gbsAlert(t("Falha ao apagar o preset")).catch(() => { });
        }
    })
        .catch(() => {
        gbsAlert(t("Erro ao apagar o preset")).catch(() => { });
    });
};
// ---- Profile cards: pagination (6 per page), swipe and search ----
const SLOT_ROW_HEIGHT = 88; // card min-height (80) + margins
let slotsPerPage = 6;
const SLOT_SEARCH_MIN_SAVED = 12;
const slotPager = { page: 0, query: "", userNavigated: false };
const normalizeSearch = (s) => s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .trim();
// Fit as many rows (2 cards each) as the visible area allows instead of a
// fixed 6 per page; keeps the previous value while the tab is hidden.
const computeSlotsPerPage = () => {
    const container = GBSControl.ui.slotContainer;
    const scroll = document.querySelector(".gbs-scroll");
    if (!container || !scroll || scroll.clientHeight === 0 || container.offsetParent === null) {
        return;
    }
    const top = container.getBoundingClientRect().top -
        scroll.getBoundingClientRect().top +
        scroll.scrollTop;
    const below = 160; // pager + counter + action buttons + padding
    const rows = Math.floor((scroll.clientHeight - top - below) / SLOT_ROW_HEIGHT);
    slotsPerPage = Math.max(3, Math.min(12, rows)) * 2;
};
const applySlotPagination = () => {
    const container = GBSControl.ui.slotContainer;
    if (!container) {
        return;
    }
    computeSlotsPerPage();
    const buttons = nodelistToArray(container.querySelectorAll('[gbs-role="slot"]'));
    const query = normalizeSearch(slotPager.query);
    const shown = [];
    let emptyPlaced = false;
    let savedCount = 0;
    buttons.forEach((button) => {
        const name = (button.getAttribute("gbs-name") || "").trim();
        const isEmpty = name === "Empty";
        if (!isEmpty) {
            savedCount++;
        }
        let visible;
        if (isEmpty) {
            visible = !query && !emptyPlaced;
            if (visible) {
                emptyPlaced = true;
            }
        }
        else {
            visible = !query || normalizeSearch(name).indexOf(query) >= 0;
        }
        button.classList.toggle("gbs-slot--filtered", !visible);
        if (visible) {
            shown.push(button);
        }
    });
    const pages = Math.max(1, Math.ceil(shown.length / slotsPerPage));
    slotPager.page = Math.max(0, Math.min(slotPager.page, pages - 1));
    shown.forEach((button, i) => {
        button.classList.toggle("gbs-slot--offpage", Math.floor(i / slotsPerPage) !== slotPager.page);
    });
    const searchWrap = document.querySelector("[gbs-slot-search-wrap]");
    if (searchWrap) {
        if (savedCount > SLOT_SEARCH_MIN_SAVED || slotPager.query) {
            searchWrap.removeAttribute("hidden");
        }
        else {
            searchWrap.setAttribute("hidden", "");
        }
    }
    if (pages > 1) {
        container.setAttribute("gbs-paged", "");
        container.style.minHeight = `${(slotsPerPage / 2) * SLOT_ROW_HEIGHT}px`;
    }
    else {
        container.style.minHeight = "";
        container.removeAttribute("gbs-paged");
    }
    const pager = document.querySelector("[gbs-pager]");
    const dots = document.querySelector("[gbs-pager-dots]");
    if (pager && dots) {
        if (pages > 1) {
            pager.removeAttribute("hidden");
            dots.innerHTML = "";
            for (let p = 0; p < pages; p++) {
                const dot = document.createElement("span");
                dot.className = "gbs-pager__dot";
                if (p === slotPager.page) {
                    dot.setAttribute("active", "");
                }
                dot.addEventListener("click", () => {
                    slotPager.userNavigated = true;
                    slotPager.page = p;
                    applySlotPagination();
                });
                dots.appendChild(dot);
            }
        }
        else {
            pager.setAttribute("hidden", "");
        }
    }
};
const changeSlotPage = (delta) => {
    slotPager.userNavigated = true;
    slotPager.page += delta;
    applySlotPagination();
};
// Only used to open on the active preset's page at load; once the user pages,
// searches or taps a card, never jump (the device re-syncs the active preset
// and would pull them back to its page, e.g. when picking an empty slot).
const showActiveSlotPage = () => {
    if (slotPager.userNavigated) {
        return;
    }
    const container = GBSControl.ui.slotContainer;
    const active = container && container.querySelector('[gbs-role="slot"][active]');
    if (!active) {
        return;
    }
    const visible = nodelistToArray(container.querySelectorAll('[gbs-role="slot"]:not(.gbs-slot--filtered)'));
    const index = visible.indexOf(active);
    if (index >= 0) {
        const page = Math.floor(index / slotsPerPage);
        if (page !== slotPager.page) {
            slotPager.page = page;
            applySlotPagination();
        }
    }
};
const initSlotPager = () => {
    const container = GBSControl.ui.slotContainer;
    const prev = document.querySelector("[gbs-pager-prev]");
    const next = document.querySelector("[gbs-pager-next]");
    if (prev) {
        prev.addEventListener("click", () => changeSlotPage(-1));
    }
    if (next) {
        next.addEventListener("click", () => changeSlotPage(1));
    }
    const search = document.querySelector("[gbs-slot-search]");
    if (search) {
        search.addEventListener("input", () => {
            slotPager.userNavigated = true;
            slotPager.query = search.value;
            slotPager.page = 0;
            applySlotPagination();
        });
    }
    if (container) {
        let startX = 0;
        let startY = 0;
        container.addEventListener("touchstart", (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        container.addEventListener("touchend", (e) => {
            const dx = e.changedTouches[0].clientX - startX;
            const dy = e.changedTouches[0].clientY - startY;
            if (Math.abs(dx) > 50 && Math.abs(dy) < 40) {
                changeSlotPage(dx < 0 ? 1 : -1);
            }
        });
        const markNavigated = () => {
            slotPager.userNavigated = true;
        };
        container.addEventListener("click", markNavigated, true);
        container.addEventListener("touchend", markNavigated, true);
        window.addEventListener("resize", () => applySlotPagination());
        // Jump to the page of the active preset whenever the active one changes.
        new MutationObserver(showActiveSlotPage).observe(container, {
            attributes: true,
            subtree: true,
            attributeFilter: ["active"],
        });
    }
    applySlotPagination();
};
// ---- Color themes (accent colors only; CSS does the rest via data-theme) ----
const GBS_THEMES = ["padrao", "fosforo", "synthwave", "ambar", "rubi", "roxo"];
const applyTheme = (theme) => {
    if (GBS_THEMES.indexOf(theme) < 0) {
        theme = "padrao";
    }
    document.documentElement.setAttribute("data-theme", theme);
    try {
        localStorage.setItem("gbs-theme", theme);
    }
    catch (e) { }
    nodelistToArray(document.querySelectorAll(".gbs-theme-btn")).forEach((b) => {
        if (b.getAttribute("gbs-theme-value") === theme) {
            b.setAttribute("active", "");
        }
        else {
            b.removeAttribute("active");
        }
    });
};
const initThemeSelector = () => {
    let stored = null;
    try {
        stored = localStorage.getItem("gbs-theme");
    }
    catch (e) { }
    nodelistToArray(document.querySelectorAll(".gbs-theme-btn")).forEach((button) => {
        button.addEventListener("click", () => applyTheme(button.getAttribute("gbs-theme-value")));
    });
    applyTheme(stored || "padrao");
};
// ---- Language selector (PT-BR default, English optional) ----
// Portuguese text lives directly in the HTML template / code. English is
// applied on top of it via this exact-text dictionary; anything not listed
// (slot names, technical labels) stays untouched.
const I18N_EN = {
    "Perfis salvos:": "Saved profiles:",
    "Buscar perfil": "Search profile",
    "Padrão": "Default",
    "Verde Fósforo": "Phosphor Green",
    "Âmbar CRT": "CRT Amber",
    "Rubi Famicom": "Famicom Ruby",
    "Roxo GameCube": "GameCube Purple",
    "Resolução": "Resolution",
    "Escolha uma resolução de saída entre estas predefinições.": "Choose an output resolution from these presets.",
    "Sua seleção também será usada na inicialização. 1280x960 é recomendado para fontes NTSC, 1280x1024 para PAL.": "Your selection will also be used for startup. 1280x960 is recommended for NTSC sources, 1280x1024 for PAL.",
    "Use a opção \"Perfis Combinados\" para alternar entre as duas automaticamente (aba Preferências)": "Use the \"Matched Presets\" option to switch between the two automatically (Preferences tab)",
    "Selecionar uma resolução também a torna a nova predefinição de inicialização.": "Selecting a resolution also makes it the new startup preset.",
    "Passagem": "Pass Through",
    "Perfis": "Presets",
    "Para salvar suas customizações, primeiro selecione um slot para o novo perfil, depois salve ou carregue nele.": "If you want to save your customizations, first select a slot for your new preset, then save to or load from that slot.",
    "Selecionar um slot também o torna o perfil de boot.": "Selecting a slot also makes it the new startup preset.",
    "carregar perfil": "load preset",
    "salvar perfil": "save preset",
    "apagar perfil": "delete preset",
    "Ganho ADC (brilho)": "ADC Gain (brightness)",
    "Ganho +/- ajusta o ganho do perfil carregado atualmente.": "Gain +/- adjusts the gain for the currently loaded preset.",
    "Ganho Automático aumenta o ganho até áreas claras virarem brancas, depois reduz quando detecta clipping. Calibre por alguns segundos numa tela branca.": "Auto Gain increases gain so bright areas are displayed as white, then decreases it when clipping is detected. Calibrate for a few seconds on a white screen.",
    "ganho": "gain",
    "Ganho Auto": "Auto Gain",
    "Controles de Imagem": "Picture Control",
    "mover": "move",
    "escalar": "scale",
    "bordas": "borders",
    "Filtros": "Filters",
    "intensidade": "intensity",
    "filtro de linha": "line filter",
    "Scanlines só funcionam com fontes 240p, ou 480i com desentrelaçamento Bob.": "Scanlines only work with 240p sources, or 480i with Bob deinterlacing.",
    "O filtro de linha elimina artefatos de pixels quadriculados ao escalar acima de 480p, recomendado.": "Line Filter eliminates blocky-pixel artifacts when upscaling beyond 480p, and is recommended.",
    "realce": "peaking",
    "resposta de degrau": "step response",
    "Realce aumenta o contraste em transições horizontais de brilho, recomendado.": "Peaking increases contrast around horizontal brightness steps, and is recommended.",
    "Resposta de degrau aumenta a nitidez das transições horizontais de cor, recomendado.": "Step Response increases the sharpness of horizontal color steps, and is recommended.",
    "Configurações": "Settings",
    "Perfis Combinados": "Matched Presets",
    "Se ativo, usa 1280x960 para NTSC 60 e 1280x1024 para PAL 50 (não se aplica para perfis 720p / 1080p).": "If enabled, default to 1280x960 for NTSC 60 and 1280x1024 for PAL 50 (does not apply for 720p / 1080p presets).",
    "Altura Total": "Full Height",
    "Alguns perfis não usam toda a resolução vertical de saída, deixando algumas linhas pretas.": "Some presets default to not using the entire vertical output resolution, leaving some lines black.",
    "Com Altura Total ativa, esses perfis escalam para preencher mais a altura da tela.": "With Full Height enabled, these presets will instead scale to fill more of the screen height.",
    "(Atualmente afeta apenas 1920 x 1080)": "(This currently only affects 1920 x 1080)",
    "Baixa Res: Usar Upscaling": "Low Res: Use Upscaling",
    "Entrada VGA de baixa resolução: Passagem direta ou Upscale": "Low Resolution VGA input: Pass-through or Upscale",
    "Fontes de baixa resolução podem ser passadas diretamente ou escaladas.": "Low resolution sources can be either passed on directly or get upscaled.",
    "Upscaling pode ter problemas de borda/escala, mas é mais compatível com telas.": "Upscaling may have some border / scaling issues, but is more compatible with displays.",
    "Taxas de atualização diferentes de 60Hz ainda não têm bom suporte.": "Also, refresh rates other than 60Hz are not well supported yet.",
    "\"Baixa resolução\" hoje é definida como menor ou igual a 640x480 (525 linhas ativas).": "\"Low resolution\" is currently set at below or equal to 640x480 (525 active lines).",
    "Saída RGBHV/Componente": "Output RGBHV/Component",
    "O modo de saída padrão é RGBHV, ideal para cabos VGA ou conversores HDMI.": "The default output mode is RGBHV, suitable for use with VGA cables or HDMI converters.",
    "Um modo experimental YPbPr também pode ser selecionado. A compatibilidade ainda é instável.": "An experimental YPbPr mode can also be selected. Compatibility is still spotty.",
    "Visor OLED: Exibição": "OLED Display: Content",
    "O que a telinha OLED mostra na tela principal quando um preset customizado (slot A-Z) está carregado.": "What the OLED screen shows on the main screen while a custom preset (slot A-Z) is loaded.",
    "Sem preset carregado, a tela continua mostrando a resolução normalmente. Também vale pro protetor de tela: no modo Nome ele usa a animação padrão, no modo Ícone ele anima o ícone do preset (quando existe uma animação cadastrada pra ele).": "With no preset loaded, the screen keeps showing the resolution as usual. This also applies to the screensaver: in Name mode it uses the default animation, in Icon mode it animates the preset's icon (when an animation exists for it).",
    "Nome": "Name",
    "Ícone": "Icon",
    "Perfil de Inicialização": "Startup Profile",
    "Por padrão a GBS lembra e recarrega o último preset/resolução usado. Escolha um perfil aqui pra sempre carregar ele ao ligar, independente do que estava ativo antes de desligar.": "By default the GBS remembers and reloads the last preset/resolution used. Pick a profile here to always load it on power-up, regardless of what was active before shutdown.",
    "Desativado (lembrar o último usado)": "Disabled (remember the last used)",
    "Taxa de Quadros: Forçar PAL 50Hz para 60Hz": "Output Frame Rate: Force PAL 50Hz to 60Hz",
    "Se sua TV não suporta fontes 50Hz (exibindo formato desconhecido, independente do perfil), tente esta opção.": "If your TV does not support 50Hz sources (displaying unknown format, no matter the preset), try this option.",
    "O frame rate não será tão suave. Requer reinício.": "The frame rate will not be as smooth. Reboot required.",
    "Desabilitar Gerador de Clock Externo": "Disable External Clock Generator",
    "Por padrão o gerador de clock externo é ativado quando instalado.": "By default the external clock generator is enabled when installed.",
    "Você pode desativá-lo se tiver problemas com outras opções, como Forçar PAL 50Hz para 60Hz. Requer reinício.": "You can disable it if you have issues with other options, e.g Force PAL 50Hz to 60Hz. Reboot required.",
    "Calibração ADC": "ADC calibration",
    "O Gbscontrol calibra os offsets do ADC no boot.": "Gbscontrol calibrates the ADC offsets on startup.",
    "Em caso de problemas de desvio de cor, tente desabilitar esta função.": "In case of color shift problems, try disabling this function.",
    "Trava de FrameTime": "FrameTime Lock",
    "Esta opção mantém alinhados os tempos de entrada e saída, corrigindo a linha de \"tearing\" horizontal que pode aparecer.": "This option keeps the input and output timings aligned, fixing the horizontal tear line that can appear sometimes.",
    "Dois métodos disponíveis. Tente alternar se a tela ficar preta ou deslocar verticalmente.": "Two methods are available. Try switching methods if your display goes blank or shifts vertically.",
    "Travar FrameTime": "Active FrameTime Lock",
    "Alternar Método de Trava": "Switch Lock Method",
    "Método de Desentrelaçamento": "Deinterlace Method",
    "O Gbscontrol detecta conteúdo entrelaçado e alterna o desentrelaçamento automaticamente.": "Gbscontrol detects interlaced content and automatically toggles deinterlacing.",
    "Método Bob: praticamente sem desentrelaçamento, sem lag adicional mas cintila, pode combinar com scanlines": "Bob Method: essentially no deinterlacing, no added lag but flickers, can be combined with scanlines",
    "Adaptativo por Movimento: remove o flicker mas mostra alguns artefatos em detalhes em movimento": "Motion Adaptive: removes flicker and shows some artefacts in moving details",
    "Se possível, configure a fonte para saída progressiva. Caso contrário, recomenda-se o Adaptativo por Movimento.": "If possible, configure the source for progressive output. Otherwise, using Motion Adaptive is recommended.",
    "Adaptativo por Movimento": "Motion Adaptive",
    "Modo Desenvolvedor": "Developer Mode",
    "Habilita o menu de desenvolvedor com várias ferramentas de debug": "Enables the developer menu which contains various debugging tools",
    "Salvar Filtros por Slot": "Save Filtering Per Slot",
    "Quando ativo, slots salvos recuperam suas próprias preferências de filtro.": "When enabled, saved slots recover their own filter preferences.",
    "Quando desativo, slots salvos mantêm os filtros atuais.": "When disabled, saved slots maintain current filter settings.",
    "Sistema": "System",
    "Habilitar OTA": "Enable OTA",
    "Reiniciar": "Restart",
    "Restaurar Padrões": "Reset Defaults",
    "Cópia [para o mesmo aparelho]": "Backup [intended for same device]",
    "Cópia / Restauração dos arquivos de configuração": "Backup / Restore of configuration files",
    "A cópia é válida apenas no aparelho atual": "Backup is valid for current device only",
    "Baixar": "Download",
    "Restaurar": "Restore",
    "Ponto de Acesso": "Access Point",
    "Estação": "Station",
    "Selecionar Rede": "Select SSID",
    "Conectar à Rede": "Connect to SSID",
    "Conectar": "Connect",
    "Origem de vídeo": "Video source",
    "Componente": "Component",
    "CANCELAR": "CANCEL",
    "ALERTA": "ALERT",
    "Escolha um ícone": "Choose an icon",
    "Saída": "Output",
    "senha": "password",
    "Nome do slot": "Slot name",
    "Falha ao apagar o preset": "Failed to delete the preset",
    "Erro ao apagar o preset": "Error deleting the preset",
    "Erro ao salvar o preset": "Error saving the preset",
    "Atualização disponível": "Update available",
    "Arquivo de cópia inválido": "Invalid backup file",
    "Reiniciando o GBSControl.\nAguarde o wifi reconectar e clique OK": "Restarting GBSControl.\nWait for wifi to reconnect and click OK",
    "Trocando para o modo Ponto de Acesso. Conecte-se ao SSID gbscontrol e clique OK": "Switching to Access Point mode. Connect to the gbscontrol SSID and click OK",
};
let currentLang = "pt";
const isEn = () => currentLang === "en";
const t = (pt) => (isEn() && I18N_EN[pt]) || pt;
const i18nOriginals = new WeakMap();
const i18nAttrOriginals = new WeakMap();
const normalizeI18nKey = (s) => s.replace(/\s+/g, " ").trim();
const translateTextNodes = () => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
        nodes.push(walker.currentNode);
    }
    nodes.forEach((node) => {
        const parent = node.parentElement;
        if (!parent ||
            parent.closest("script, style, textarea, .gbs-icon, [gbs-lang-keep]")) {
            return;
        }
        if (!i18nOriginals.has(node)) {
            i18nOriginals.set(node, node.nodeValue || "");
        }
        const original = i18nOriginals.get(node);
        const translated = isEn() ? I18N_EN[normalizeI18nKey(original)] : undefined;
        if (translated) {
            const lead = original.match(/^\s*/)[0];
            const trail = original.match(/\s*$/)[0];
            node.nodeValue = lead + translated + trail;
        }
        else if (node.nodeValue !== original) {
            node.nodeValue = original;
        }
    });
    nodelistToArray(document.querySelectorAll("[placeholder]")).forEach((el) => {
        if (!i18nAttrOriginals.has(el)) {
            i18nAttrOriginals.set(el, el.getAttribute("placeholder") || "");
        }
        const original = i18nAttrOriginals.get(el);
        el.setAttribute("placeholder", (isEn() && I18N_EN[original]) || original);
    });
};
const applyLanguage = (lang) => {
    currentLang = lang;
    document.documentElement.setAttribute("lang", lang === "en" ? "en" : "pt-BR");
    try {
        localStorage.setItem("gbs-lang", lang);
    }
    catch (e) { }
    translateTextNodes();
    nodelistToArray(document.querySelectorAll(".gbs-lang-btn")).forEach((b) => {
        if (b.getAttribute("gbs-lang-value") === lang) {
            b.setAttribute("active", "");
        }
        else {
            b.removeAttribute("active");
        }
    });
    if (GBSControl.structs) {
        updateSlotNames();
    }
};
const initLanguageSelector = () => {
    let stored = null;
    try {
        stored = localStorage.getItem("gbs-lang");
    }
    catch (e) { }
    const initial = stored === "en" || stored === "pt"
        ? stored
        : (navigator.language || "pt").toLowerCase().indexOf("pt") === 0
            ? "pt"
            : "en";
    nodelistToArray(document.querySelectorAll(".gbs-lang-btn")).forEach((button) => {
        button.addEventListener("click", () => {
            applyLanguage(button.getAttribute("gbs-lang-value"));
        });
    });
    applyLanguage(initial);
};
const initOledPresetDisplayButtons = () => {
    const buttons = nodelistToArray(document.querySelectorAll(".gbs-oled-preset-display-btn"));
    const markActive = (value) => {
        buttons.forEach((b) => {
            if (b.getAttribute("gbs-oled-preset-display-value") === value) {
                b.setAttribute("active", "");
            }
            else {
                b.removeAttribute("active");
            }
        });
    };
    buttons.forEach((button) => {
        const value = button.getAttribute("gbs-oled-preset-display-value");
        button.addEventListener("click", () => {
            markActive(value);
            fetch(`/gbs/oled-preset-display-set?value=${value}&${+new Date()}`).catch(() => { });
        });
    });
    fetch(`/gbs/oled-preset-display?${+new Date()}`)
        .then((r) => r.json())
        .then((value) => markActive(String(value)))
        .catch(() => { });
};
const getSlotsHTML = () => {
    // prettier-ignore
    return [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.', '_', '~', '(', ')', '!', '*', ':', ','
    ].map((chr, idx) => {
        return `<button
    class="gbs-button gbs-button__slot"
    gbs-slot-id="${idx}"
    gbs-message="${chr}"
    gbs-message-type="setSlot"
    gbs-click="normal"
    gbs-element-ref="slot-${chr}"
    gbs-role="slot"
    gbs-name="slot-${idx}"
  ><svg class="gbs-slot-art"><use gbs-icon-use href="#gbs-slot-icon-0"></use></svg></button>`;
    }).join('');
};
const setSlot = (slot) => {
    fetch(`/slot/set?slot=${slot}&${+new Date()}`);
};
// Slot buttons are generated once (fixed gbs-slot-id per storage index, see
// getSlotsHTML()) and never recreated, so re-sorting means actually moving
// the existing DOM nodes (appendChild on an attached element relocates it
// instead of cloning it) rather than just a CSS "order" - a CSS-only
// reorder wouldn't touch document order, and the "only show the first
// Vazio" trick in style.css ([gbs-name="Empty"] ~ [gbs-name="Empty"]) relies
// on document order to hide the other ~70 unused slots.
const sortSlotButtonsAlphabetically = () => {
    const container = GBSControl.ui.slotContainer;
    if (!container) {
        return;
    }
    const buttons = nodelistToArray(container.querySelectorAll('[gbs-role="slot"]'));
    buttons.sort((a, b) => {
        const nameA = a.getAttribute("gbs-name") || "";
        const nameB = b.getAttribute("gbs-name") || "";
        const emptyA = nameA === "Empty";
        const emptyB = nameB === "Empty";
        if (emptyA !== emptyB) {
            // keep the (single, visible) "Vazio" placeholder last, not wherever
            // "Empty" happens to sort alphabetically
            return emptyA ? 1 : -1;
        }
        return nameA.localeCompare(nameB, "pt-BR", { sensitivity: "base" });
    });
    const fragment = document.createDocumentFragment();
    buttons.forEach((button) => fragment.appendChild(button));
    container.appendChild(fragment);
};
const updateSlotNames = () => {
    let savedCount = 0;
    for (let i = 0; i < GBSControl.maxSlots; i++) {
        const slotName = (GBSControl.structs.slots[i].name || "").trim();
        if (slotName && slotName !== "Empty") {
            savedCount++;
        }
        const el = document.querySelector(`[gbs-slot-id="${i}"]`);
        if (!el) {
            continue;
        }
        el.setAttribute("gbs-name", GBSControl.structs.slots[i].name);
        const iconId = GBSControl.slotIcons[i] || 0;
        nodelistToArray(el.querySelectorAll("[gbs-icon-use]")).forEach((use) => {
            use.setAttribute("href", `#gbs-slot-icon-${iconId}`);
        });
        el.setAttribute("gbs-conn", t(CONNECTOR_LABELS[GBSControl.slotConnectors[i]] || ""));
    }
    const counter = document.querySelector("[gbs-slot-count]");
    if (counter) {
        counter.textContent = `${savedCount}/${GBSControl.maxSlots}`;
    }
    sortSlotButtonsAlphabetically();
    applySlotPagination();
    showActiveSlotPage();
    populateStartupPresetOptions();
};
let startupPresetValue = null;
const applyStartupPresetSelectValue = () => {
    const select = document.querySelector("[gbs-startup-preset-select]");
    if (select && startupPresetValue !== null) {
        select.value = String(startupPresetValue);
    }
};
const populateStartupPresetOptions = () => {
    const select = document.querySelector("[gbs-startup-preset-select]");
    if (!select || !GBSControl.structs) {
        return;
    }
    while (select.options.length > 1) {
        select.remove(1);
    }
    const namedSlots = [];
    for (let i = 0; i < GBSControl.maxSlots; i++) {
        const slot = GBSControl.structs.slots[i];
        const name = slot && slot.name ? slot.name.trim() : "";
        if (!name || name === "Empty") {
            continue;
        }
        namedSlots.push({ index: i, name });
    }
    namedSlots.sort((a, b) => a.name.localeCompare(b.name, "pt-BR", { sensitivity: "base" }));
    for (const { index: i, name } of namedSlots) {
        const option = document.createElement("option");
        option.value = String(i + 1);
        option.textContent = name;
        select.appendChild(option);
    }
    applyStartupPresetSelectValue();
};
const initStartupPresetSelect = () => {
    const select = document.querySelector("[gbs-startup-preset-select]");
    if (!select) {
        return;
    }
    select.addEventListener("change", () => {
        fetch(`/gbs/startup-preset-set?value=${select.value}&${+new Date()}`).catch(() => { });
    });
    fetch(`/gbs/startup-preset?${+new Date()}`)
        .then((r) => r.json())
        .then((value) => {
        startupPresetValue = value;
        applyStartupPresetSelectValue();
    })
        .catch(() => { });
};
const fetchSlotNames = () => {
    // The ESP8266 web server only handles a handful of concurrent
    // connections, and there's usually already an open websocket - firing 3
    // parallel fetches here made the 3rd (slot_conn.bin) fail silently often
    // enough that the connector label basically never showed up. Fetch it
    // sequentially, after the other two (which were already reliable as a
    // pair), instead of adding a 3rd parallel request.
    return Promise.all([
        fetch(`/bin/slots.bin?${+new Date()}`).then((response) => response.arrayBuffer()),
        fetch(`/bin/slot_icons.bin?${+new Date()}`)
            .then((response) => response.arrayBuffer())
            .catch(() => null),
    ]).then(([arrayBuffer, iconsBuffer]) => {
        if (arrayBuffer.byteLength !==
            StructParser.getSize(Structs, "slots") * GBSControl.maxSlots) {
            return false;
        }
        GBSControl.structs = {
            slots: StructParser.parseStructArray(arrayBuffer, Structs, "slots"),
        };
        GBSControl.slotIcons =
            iconsBuffer && iconsBuffer.byteLength === GBSControl.maxSlots
                ? new Uint8Array(iconsBuffer)
                : new Uint8Array(GBSControl.maxSlots);
        const fetchConn = () => fetch(`/bin/slot_conn.bin?${+new Date()}`)
            .then((response) => response.arrayBuffer())
            .catch(() => null);
        // One retry: this device only has a handful of TCP connections to go
        // around (there's usually a websocket open too), so a single fetch
        // failing here and there is expected - not worth surfacing to the user
        // over just trying once more.
        return fetchConn()
            .then((connBuffer) => (connBuffer ? connBuffer : fetchConn()))
            .then((connBuffer) => {
            GBSControl.slotConnectors =
                connBuffer && connBuffer.byteLength === GBSControl.maxSlots
                    ? new Uint8Array(connBuffer)
                    : new Uint8Array(GBSControl.maxSlots);
            return true;
        });
    });
};
const fetchSlotNamesErrorRetry = () => {
    setTimeout(fetchSlotNamesAndInit, 1000);
};
const fetchSlotNamesAndInit = () => {
    fetchSlotNames()
        .then((success) => {
        if (!success) {
            fetchSlotNamesErrorRetry();
            return;
        }
        initUIElements();
        checkForUpdate();
        wifiGetStatus().then(() => {
            initUI();
            updateSlotNames();
            createWebSocket();
            createIntervalChecks();
            setTimeout(hideLoading, 1000);
        });
    }, fetchSlotNamesErrorRetry)
        .catch(fetchSlotNamesErrorRetry);
};
/** Promises */
const serial = (funcs) => funcs.reduce((promise, func) => promise.then((result) => func().then(Array.prototype.concat.bind(result))), Promise.resolve([]));
/** helpers */
const toggleHelp = () => {
    let help = GBSStorage.read("help") || false;
    GBSStorage.write("help", !help);
    updateHelp(!help);
};
const toggleDeveloperMode = () => {
    const developerMode = GBSStorage.read("developerMode") || false;
    GBSStorage.write("developerMode", !developerMode);
    updateDeveloperMode(!developerMode);
};
const toggleCustomSlotFilters = () => {
    const customSlotFilters = GBSStorage.read("customSlotFilters");
    GBSStorage.write("customSlotFilters", !customSlotFilters);
    updateCustomSlotFilters(!customSlotFilters);
};
const updateHelp = (help) => {
    if (help) {
        document.body.classList.remove("gbs-help-hide");
    }
    else {
        document.body.classList.add("gbs-help-hide");
    }
};
const updateDeveloperMode = (developerMode) => {
    const el = document.querySelector('[gbs-section="developer"]');
    if (developerMode) {
        el.removeAttribute("hidden");
        GBSControl.ui.developerSwitch.setAttribute("active", "");
        document.body.classList.remove("gbs-output-hide");
    }
    else {
        el.setAttribute("hidden", "");
        GBSControl.ui.developerSwitch.removeAttribute("active");
        document.body.classList.add("gbs-output-hide");
    }
    GBSControl.ui.developerSwitch.querySelector(".gbs-icon").innerText = developerMode ? "toggle_on" : "toggle_off";
};
const updateCustomSlotFilters = (customFilters = GBSStorage.read("customSlotFilters") === true) => {
    if (customFilters) {
        GBSControl.ui.customSlotFilters.setAttribute("active", "");
    }
    else {
        GBSControl.ui.customSlotFilters.removeAttribute("active");
    }
    GBSControl.ui.customSlotFilters.querySelector(".gbs-icon").innerText = customFilters ? "toggle_on" : "toggle_off";
};
const GBSStorage = {
    lsObject: {},
    write(key, value) {
        GBSStorage.lsObject = GBSStorage.lsObject || {};
        GBSStorage.lsObject[key] = value;
        localStorage.setItem("GBSControlSlotNames", JSON.stringify(GBSStorage.lsObject));
    },
    read(key) {
        GBSStorage.lsObject = JSON.parse(localStorage.getItem("GBSControlSlotNames") || "{}");
        return GBSStorage.lsObject[key];
    },
};
const nodelistToArray = (nodelist) => {
    return Array.prototype.slice.call(nodelist);
};
const toggleButtonActive = (id) => (button, _index, _array) => {
    button.removeAttribute("active");
    if (button.getAttribute("gbs-element-ref") === id) {
        button.setAttribute("active", "");
    }
};
const displayWifiWarning = (mode) => {
    GBSControl.ui.webSocketConnectionWarning.style.display = mode
        ? "block"
        : "none";
};
const updateTerminal = () => {
    if (GBSControl.queuedText.length > 0) {
        requestAnimationFrame(() => {
            GBSControl.ui.terminal.value += GBSControl.queuedText;
            GBSControl.ui.terminal.scrollTop = GBSControl.ui.terminal.scrollHeight;
            GBSControl.queuedText = "";
        });
    }
};
const updateViewPort = () => {
    document.documentElement.style.setProperty("--viewport-height", window.innerHeight + "px");
};
const hideLoading = () => {
    GBSControl.ui.loader.setAttribute("style", "display:none");
};
const checkFetchResponseStatus = (response) => {
    if (!response.ok) {
        throw new Error(`HTTP ${response.status} - ${response.statusText}`);
    }
    return response;
};
const readLocalFile = (file) => {
    const reader = new FileReader();
    reader.addEventListener("load", (event) => {
        doRestore(reader.result);
    });
    reader.readAsArrayBuffer(file);
};
/** backup / restore */
const doBackup = () => {
    let backupFiles;
    let done = 0;
    let total = 0;
    fetch("/spiffs/dir")
        .then((r) => r.json())
        .then((files) => {
        backupFiles = files;
        total = files.length;
        const funcs = files.map((path) => () => {
            return fetch(`/spiffs/download?file=${path}&${+new Date()}`).then((response) => {
                GBSControl.ui.progressBackup.setAttribute("gbs-progress", `${done}/${total}`);
                done++;
                return checkFetchResponseStatus(response) && response.arrayBuffer();
            });
        });
        return serial(funcs);
    })
        .then((files) => {
        const headerDescriptor = files.reduce((acc, f, index) => {
            acc[backupFiles[index]] = f.byteLength;
            return acc;
        }, {});
        const backupFilesJSON = JSON.stringify(headerDescriptor);
        const backupFilesJSONSize = backupFilesJSON.length;
        const mainHeader = [
            (backupFilesJSONSize >> 24) & 255,
            (backupFilesJSONSize >> 16) & 255,
            (backupFilesJSONSize >> 8) & 255,
            (backupFilesJSONSize >> 0) & 255,
        ];
        const outputArray = [
            ...mainHeader,
            ...backupFilesJSON.split("").map((c) => c.charCodeAt(0)),
            ...files.reduce((acc, f, index) => {
                acc = acc.concat(Array.from(new Uint8Array(f)));
                return acc;
            }, []),
        ];
        downloadBlob(new Blob([new Uint8Array(outputArray)]), `gbs-control.backup-${+new Date()}.bin`);
        GBSControl.ui.progressBackup.setAttribute("gbs-progress", ``);
    });
};
const doRestore = (file) => {
    const { backupInput } = GBSControl.ui;
    const fileBuffer = new Uint8Array(file);
    const headerCheck = fileBuffer.slice(4, 6);
    if (headerCheck[0] !== 0x7b || headerCheck[1] !== 0x22) {
        backupInput.setAttribute("disabled", "");
        gbsAlert(t("Arquivo de cópia inválido"))
            .then(() => {
            backupInput.removeAttribute("disabled");
        }, () => {
            backupInput.removeAttribute("disabled");
        })
            .catch(() => {
            backupInput.removeAttribute("disabled");
        });
        return;
    }
    const b0 = fileBuffer[0], b1 = fileBuffer[1], b2 = fileBuffer[2], b3 = fileBuffer[3];
    const headerSize = (b0 << 24) + (b1 << 16) + (b2 << 8) + b3;
    const headerString = Array.from(fileBuffer.slice(4, headerSize + 4))
        .map((c) => String.fromCharCode(c))
        .join("");
    const headerObject = JSON.parse(headerString);
    const files = Object.keys(headerObject);
    let pos = headerSize + 4;
    let total = files.length;
    let done = 0;
    const funcs = files.map((fileName) => () => {
        const fileContents = fileBuffer.slice(pos, pos + headerObject[fileName]);
        const formData = new FormData();
        formData.append("file", new Blob([fileContents], { type: "application/octet-stream" }), fileName.substr(1));
        return fetch("/spiffs/upload", {
            method: "POST",
            body: formData,
        }).then((response) => {
            GBSControl.ui.progressRestore.setAttribute("gbs-progress", `${done}/${total}`);
            done++;
            pos += headerObject[fileName];
            return response;
        });
    });
    serial(funcs).then(() => {
        GBSControl.ui.progressRestore.setAttribute("gbs-progress", ``);
        loadUser("a").then(() => {
            gbsAlert(t("Reiniciando o GBSControl.\nAguarde o wifi reconectar e clique OK"))
                .then(() => {
                window.location.reload();
            })
                .catch(() => { });
        });
    });
};
const downloadBlob = (blob, name = "file.txt") => {
    // Convert your blob into a Blob URL (a special url that points to an object in the browser's memory)
    const blobUrl = URL.createObjectURL(blob);
    // Create a link element
    const link = document.createElement("a");
    // Set link's href to point to the Blob URL
    link.href = blobUrl;
    link.download = name;
    // Append link to the body
    document.body.appendChild(link);
    // Dispatch click event on the link
    // This is necessary as link.click() does not work on the latest firefox
    link.dispatchEvent(new MouseEvent("click", {
        bubbles: true,
        cancelable: true,
        view: window,
    }));
    // Remove link from body
    document.body.removeChild(link);
};
/** WIFI management */
const wifiGetStatus = () => {
    return fetch(`/wifi/status?${+new Date()}`)
        .then((r) => r.json())
        .then((wifiStatus) => {
        GBSControl.wifi = wifiStatus;
        if (GBSControl.wifi.mode === "ap") {
            GBSControl.ui.wifiApButton.setAttribute("active", "");
            GBSControl.ui.wifiApButton.classList.add("gbs-button__secondary");
            GBSControl.ui.wifiStaButton.removeAttribute("active", "");
            GBSControl.ui.wifiStaButton.classList.remove("gbs-button__secondary");
            GBSControl.ui.wifiStaSSID.textContent = "STA | Scan Network";
        }
        else {
            GBSControl.ui.wifiApButton.removeAttribute("active", "");
            GBSControl.ui.wifiApButton.classList.remove("gbs-button__secondary");
            GBSControl.ui.wifiStaButton.setAttribute("active", "");
            GBSControl.ui.wifiStaButton.classList.add("gbs-button__secondary");
            GBSControl.ui.wifiStaSSID.textContent = `${GBSControl.wifi.ssid}`;
        }
    });
};
const wifiConnect = () => {
    const ssid = GBSControl.ui.wifiSSDInput.value;
    const password = GBSControl.ui.wifiPasswordInput.value;
    if (!password.length) {
        GBSControl.ui.wifiPasswordInput.classList.add("gbs-wifi__input--error");
        return;
    }
    const formData = new FormData();
    formData.append("n", ssid);
    formData.append("p", password);
    fetch("/wifi/connect", {
        method: "POST",
        body: formData,
    }).then(() => {
        gbsAlert(isEn()
            ? `GBSControl will restart and connect to ${ssid}. Wait a few seconds and click OK`
            : `O GBSControl vai reiniciar e conectar em ${ssid}. Aguarde alguns segundos e clique OK`)
            .then(() => {
            window.location.href = "http://gbscontrol.local/";
        })
            .catch(() => { });
    });
};
// Escapes text pulled from network-controlled data (e.g. a scanned WiFi
// SSID) before it is interpolated into an HTML string, since that data can
// contain markup and must not be inserted via innerHTML unescaped.
const escapeHtml = (s) => String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
const wifiScanSSID = () => {
    GBSControl.ui.wifiStaButton.setAttribute("disabled", "");
    GBSControl.ui.wifiListTable.innerHTML = "";
    if (!GBSControl.scanSSIDDone) {
        fetch(`/wifi/list?${+new Date()}`).then(() => {
            GBSControl.scanSSIDDone = true;
            setTimeout(wifiScanSSID, 3000);
        });
        return;
    }
    fetch(`/wifi/list?${+new Date()}`)
        .then((e) => e.text())
        .then((result) => {
        GBSControl.scanSSIDDone = false;
        return result.length
            ? result
                .split("\n")
                .map((line) => line.split(","))
                .map(([strength, encripted, ssid]) => {
                return { strength, encripted, ssid };
            })
            : [];
    })
        .then((ssids) => {
        return ssids.reduce((acc, ssid) => {
            const safeSsid = escapeHtml(ssid.ssid);
            return `${acc}<tr gbs-ssid="${safeSsid}">
        <td class="gbs-icon" style="opacity:${parseInt(ssid.strength, 10) / 100}">wifi</td>
        <td>${safeSsid}</td>
        <td class="gbs-icon">${ssid.encripted ? "lock" : "lock_open"}</td>
      </tr>`;
        }, "");
    })
        .then((html) => {
        GBSControl.ui.wifiStaButton.removeAttribute("disabled");
        if (html.length) {
            GBSControl.ui.wifiListTable.innerHTML = html;
            GBSControl.ui.wifiList.removeAttribute("hidden");
            GBSControl.ui.wifiConnect.setAttribute("hidden", "");
        }
    });
};
const wifiSelectSSID = (event) => {
    GBSControl.ui
        .wifiSSDInput.value = event.target.parentElement.getAttribute("gbs-ssid");
    GBSControl.ui.wifiPasswordInput.classList.remove("gbs-wifi__input--error");
    GBSControl.ui.wifiList.setAttribute("hidden", "");
    GBSControl.ui.wifiConnect.removeAttribute("hidden");
};
const wifiSetAPMode = () => {
    if (GBSControl.wifi.mode === "ap") {
        return;
    }
    const formData = new FormData();
    formData.append("n", "dummy");
    fetch("/wifi/connect", {
        method: "POST",
        body: formData,
    }).then(() => {
        gbsAlert(t("Trocando para o modo Ponto de Acesso. Conecte-se ao SSID gbscontrol e clique OK"))
            .then(() => {
            window.location.href = "http://192.168.4.1";
        })
            .catch(() => { });
    });
};
/** button click management */
const controlClick = (control) => () => {
    const controlKey = control.getAttribute("gbs-control-key");
    const target = GBSControl.controlKeysMobile[GBSControl.controlKeysMobileMode];
    switch (target.type) {
        case "loadDoc":
            loadDoc(target[controlKey]);
            break;
        case "loadUser":
            loadUser(target[controlKey]);
            break;
    }
};
const controlMouseDown = (control) => () => {
    clearInterval(control["__interval"]);
    const click = controlClick(control);
    click();
    control["__interval"] = setInterval(click, 300);
};
const controlMouseUp = (control) => () => {
    clearInterval(control["__interval"]);
};
/** inits */
const initMenuButtons = () => {
    const menuButtons = nodelistToArray(document.querySelector(".gbs-menu").querySelectorAll("button"));
    const sections = nodelistToArray(document.querySelectorAll("section"));
    const scroll = document.querySelector(".gbs-scroll");
    menuButtons.forEach((button) => button.addEventListener("click", () => {
        const section = button.getAttribute("gbs-section");
        sections.forEach((section) => section.setAttribute("hidden", ""));
        document
            .querySelector(`section[name="${section}"]`)
            .removeAttribute("hidden");
        menuButtons.forEach((btn) => btn.removeAttribute("active"));
        button.setAttribute("active", "");
        scroll.scrollTo(0, 1);
    }));
};
const initGBSButtons = () => {
    const actions = {
        user: loadUser,
        action: loadDoc,
        setSlot,
    };
    const buttons = nodelistToArray(document.querySelectorAll("[gbs-click]"));
    buttons.forEach((button) => {
        const clickMode = button.getAttribute("gbs-click");
        const message = button.getAttribute("gbs-message");
        const messageType = button.getAttribute("gbs-message-type");
        const action = actions[messageType];
        if (clickMode === "normal") {
            button.addEventListener("click", () => {
                action(message);
            });
        }
        if (clickMode === "repeat") {
            const callback = () => {
                action(message);
            };
            button.addEventListener(!("ontouchstart" in window) ? "mousedown" : "touchstart", () => {
                callback();
                clearInterval(button["__interval"]);
                button["__interval"] = setInterval(callback, 300);
            });
            button.addEventListener(!("ontouchstart" in window) ? "mouseup" : "touchend", () => {
                clearInterval(button["__interval"]);
            });
        }
    });
};
const initClearButton = () => {
    GBSControl.ui.outputClear.addEventListener("click", () => {
        GBSControl.ui.terminal.value = "";
    });
};
const initControlMobileKeys = () => {
    const controls = document.querySelectorAll("[gbs-control-target]");
    const controlsKeys = document.querySelectorAll("[gbs-control-key]");
    controls.forEach((control) => {
        control.addEventListener("click", () => {
            GBSControl.controlKeysMobileMode = control.getAttribute("gbs-control-target");
            controls.forEach((crtl) => {
                crtl.removeAttribute("active");
            });
            control.setAttribute("active", "");
        });
    });
    controlsKeys.forEach((control) => {
        control.addEventListener(!("ontouchstart" in window) ? "mousedown" : "touchstart", controlMouseDown(control));
        control.addEventListener(!("ontouchstart" in window) ? "mouseup" : "touchend", controlMouseUp(control));
    });
};
const initLegendHelpers = () => {
    nodelistToArray(document.querySelectorAll(".gbs-fieldset__legend--help")).forEach((e) => {
        e.addEventListener("click", toggleHelp);
    });
};
const initUnloadListener = () => {
    window.addEventListener("unload", () => {
        clearInterval(GBSControl.wsCheckTimer);
        if (GBSControl.ws) {
            if (GBSControl.ws.readyState == 0 || GBSControl.ws.readyState == 1) {
                GBSControl.ws.close();
            }
        }
    });
};
// Checks the device's own reported version against the latest GitHub
// release, and shows a small link in the header if a newer one exists.
// Actually downloading/flashing a new firmware happens in the GBSC
// Updater desktop app, not here - this is just a heads-up.
const GITHUB_REPO = "maniaco007/Projeto-GBSC---BR-by-Maniaco";
// Parses "v1.0.10" / "1.0.10" into [1, 0, 10] for a numeric comparison -
// a plain string compare would put "1.0.10" before "1.0.9".
const parseVersion = (v) => (v.match(/\d+/g) || ["0"]).map((n) => parseInt(n, 10));
const isNewerVersion = (remote, local) => {
    const r = parseVersion(remote);
    const l = parseVersion(local);
    for (let i = 0; i < Math.max(r.length, l.length); i++) {
        const rv = r[i] || 0;
        const lv = l[i] || 0;
        if (rv !== lv) {
            return rv > lv;
        }
    }
    return false;
};
// Best-effort and silent: no internet, GitHub unreachable, API rate
// limit, older firmware without /gbs/version - any of those just skip
// the banner instead of interrupting normal use of the device.
const checkForUpdate = () => {
    const banner = GBSControl.ui.updateBanner;
    if (!banner) {
        return;
    }
    fetch(`/gbs/version?${+new Date()}`)
        .then((r) => r.json())
        .then((deviceInfo) => fetch(`https://api.github.com/repos/${GITHUB_REPO}/releases/latest`)
        .then((r) => r.json())
        .then((release) => {
        const newer = release.tag_name &&
            release.html_url &&
            isNewerVersion(release.tag_name, deviceInfo.version);
        if (newer) {
            banner.textContent = `${t("Atualização disponível")}: ${release.tag_name}`;
            banner.setAttribute("href", release.html_url);
            banner.removeAttribute("hidden");
        }
        // Tell the device too, so it can show a small notice on the
        // OLED status bar even when nobody's looking at the webui.
        fetch(`/gbs/update-available?value=${newer ? 1 : 0}`).catch(() => { });
    }))
        .catch(() => { });
};
const initSlotButtons = () => {
    GBSControl.ui.slotContainer.innerHTML = getSlotsHTML();
    GBSControl.ui.slotButtonList = nodelistToArray(document.querySelectorAll('[gbs-role="slot"]'));
};
const initUIElements = () => {
    GBSControl.ui = {
        terminal: document.getElementById("outputTextArea"),
        webSocketConnectionWarning: document.getElementById("websocketWarning"),
        presetButtonList: nodelistToArray(document.querySelectorAll("[gbs-role='preset']")),
        slotButtonList: nodelistToArray(document.querySelectorAll('[gbs-role="slot"]')),
        toggleList: document.querySelectorAll("[gbs-toggle]"),
        toggleSwichList: document.querySelectorAll("[gbs-toggle-switch]"),
        updateBanner: document.querySelector("[gbs-update-banner]"),
        wifiList: document.querySelector("[gbs-wifi-list]"),
        wifiListTable: document.querySelector(".gbs-wifi__list"),
        wifiConnect: document.querySelector(".gsb-wifi__connect"),
        wifiConnectButton: document.querySelector("[gbs-wifi-connect-button]"),
        wifiSSDInput: document.querySelector('[gbs-input="ssid"]'),
        wifiPasswordInput: document.querySelector('[gbs-input="password"]'),
        wifiApButton: document.querySelector("[gbs-wifi-ap]"),
        wifiStaButton: document.querySelector("[gbs-wifi-station]"),
        wifiStaSSID: document.querySelector("[gbs-wifi-station-ssid]"),
        loader: document.querySelector(".gbs-loader"),
        progressBackup: document.querySelector("[gbs-progress-backup]"),
        progressRestore: document.querySelector("[gbs-progress-restore]"),
        outputClear: document.querySelector("[gbs-output-clear]"),
        slotContainer: document.querySelector("[gbs-slot-html]"),
        backupButton: document.querySelector(".gbs-backup-button"),
        backupInput: document.querySelector(".gbs-backup-input"),
        developerSwitch: document.querySelector("[gbs-dev-switch]"),
        customSlotFilters: document.querySelector("[gbs-slot-custom-filters]"),
        alert: document.querySelector('section[name="alert"]'),
        alertOk: document.querySelector("[gbs-alert-ok]"),
        alertContent: document.querySelector("[gbs-alert-content]"),
        prompt: document.querySelector('section[name="prompt"]'),
        promptOk: document.querySelector("[gbs-prompt-ok]"),
        promptCancel: document.querySelector("[gbs-prompt-cancel]"),
        promptContent: document.querySelector("[gbs-prompt-content]"),
        promptInput: document.querySelector('[gbs-input="prompt-input"]'),
        iconPicker: document.querySelector('section[name="iconpicker"]'),
        iconPickerGrid: document.querySelector("[gbs-icon-picker-grid]"),
        iconPickerCancel: document.querySelector("[gbs-icon-picker-cancel]"),
        iconPickerOk: document.querySelector("[gbs-icon-picker-ok]"),
    };
};
const initGeneralListeners = () => {
    window.addEventListener("resize", () => {
        updateViewPort();
    });
    GBSControl.ui.backupInput.addEventListener("change", (event) => {
        const fileList = event.target["files"];
        readLocalFile(fileList[0]);
        GBSControl.ui.backupInput.value = "";
    });
    GBSControl.ui.backupButton.addEventListener("click", doBackup);
    GBSControl.ui.wifiListTable.addEventListener("click", wifiSelectSSID);
    GBSControl.ui.wifiConnectButton.addEventListener("click", wifiConnect);
    GBSControl.ui.wifiApButton.addEventListener("click", wifiSetAPMode);
    GBSControl.ui.wifiStaButton.addEventListener("click", wifiScanSSID);
    GBSControl.ui.developerSwitch.addEventListener("click", toggleDeveloperMode);
    GBSControl.ui.customSlotFilters.addEventListener("click", toggleCustomSlotFilters);
    GBSControl.ui.alertOk.addEventListener("click", () => {
        GBSControl.ui.alert.setAttribute("hidden", "");
        gbsAlertPromise.resolve();
    });
    GBSControl.ui.promptOk.addEventListener("click", () => {
        GBSControl.ui.prompt.setAttribute("hidden", "");
        const value = GBSControl.ui.promptInput.value;
        if (value !== undefined && value.length > 0) {
            gbsPromptPromise.resolve({ name: value, connector: selectedConnector });
        }
        else {
            gbsPromptPromise.reject();
        }
    });
    GBSControl.ui.promptCancel.addEventListener("click", () => {
        GBSControl.ui.prompt.setAttribute("hidden", "");
        gbsPromptPromise.reject();
    });
    GBSControl.ui.promptInput.addEventListener("keydown", (event) => {
        if (event.keyCode === 13) {
            GBSControl.ui.prompt.setAttribute("hidden", "");
            const value = GBSControl.ui.promptInput.value;
            if (value !== undefined && value.length > 0) {
                gbsPromptPromise.resolve({ name: value, connector: selectedConnector });
            }
            else {
                gbsPromptPromise.reject();
            }
        }
        if (event.keyCode === 27) {
            gbsPromptPromise.reject();
        }
    });
};
const initDeveloperMode = () => {
    const devMode = GBSStorage.read("developerMode");
    if (devMode === undefined) {
        GBSStorage.write("developerMode", false);
        updateDeveloperMode(false);
    }
    else {
        updateDeveloperMode(devMode);
    }
};
const initHelp = () => {
    let help = GBSStorage.read("help");
    if (help === undefined) {
        help = false;
        GBSStorage.write("help", help);
    }
    updateHelp(help);
};
const gbsAlertPromise = {
    resolve: null,
    reject: null,
};
const alertKeyListener = (event) => {
    if (event.keyCode === 13) {
        gbsAlertPromise.resolve();
    }
    if (event.keyCode === 27) {
        gbsAlertPromise.reject();
    }
};
const gbsAlert = (text) => {
    GBSControl.ui.alertContent.textContent = text;
    GBSControl.ui.alert.removeAttribute("hidden");
    document.addEventListener("keyup", alertKeyListener);
    return new Promise((resolve, reject) => {
        gbsAlertPromise.resolve = (e) => {
            document.removeEventListener("keyup", alertKeyListener);
            GBSControl.ui.alert.setAttribute("hidden", "");
            return resolve(e);
        };
        gbsAlertPromise.reject = () => {
            document.removeEventListener("keyup", alertKeyListener);
            GBSControl.ui.alert.setAttribute("hidden", "");
            return reject();
        };
    });
};
const gbsPromptPromise = {
    resolve: null,
    reject: null,
};
let selectedConnector = 1; // SCART by default
const applyConnectorSelection = () => {
    const items = nodelistToArray(document.querySelectorAll("[gbs-connector-value]"));
    items.forEach((item) => {
        const value = parseInt(item.getAttribute("gbs-connector-value"), 10);
        if (value === selectedConnector) {
            item.setAttribute("active", "");
        }
        else {
            item.removeAttribute("active");
        }
    });
};
const initConnectorPicker = () => {
    const items = nodelistToArray(document.querySelectorAll("[gbs-connector-value]"));
    items.forEach((item) => {
        item.addEventListener("click", () => {
            selectedConnector = parseInt(item.getAttribute("gbs-connector-value"), 10);
            applyConnectorSelection();
        });
    });
};
const gbsPrompt = (text, defaultValue = "", defaultConnector = 1) => {
    GBSControl.ui.promptContent.textContent = text;
    GBSControl.ui.prompt.removeAttribute("hidden");
    GBSControl.ui.promptInput.value = defaultValue;
    selectedConnector = defaultConnector || 1;
    applyConnectorSelection();
    return new Promise((resolve, reject) => {
        gbsPromptPromise.resolve = resolve;
        gbsPromptPromise.reject = reject;
        GBSControl.ui.promptInput.focus();
    });
};
const SLOT_ICON_COUNT = 56;
// 0 = not set (older preset, saved before this existed)
const CONNECTOR_LABELS = {
    1: "SCART",
    2: "VGA",
    3: "Componente",
    4: "RGBS",
};
const SLOT_ICON_LABELS = [
    "Genérico",
    "Nintendo NES",
    "Famicom",
    "Super Nintendo",
    "Super Nintendo (Alt)",
    "Super Nintendo (logo)",
    "Nintendo 64",
    "Nintendo 64 (logo)",
    "GameCube",
    "GameCube (logo)",
    "Nintendo Wii",
    "Nintendo Wii (logo)",
    "Game Boy Advance",
    "Game Boy Micro",
    "Sega Mega Drive",
    "Sega Genesis",
    "Mega Drive (logo)",
    "Mega Drive / Genesis (linha)",
    "Sega Saturn",
    "Sega Saturn (logo)",
    "Sega Saturn (linha)",
    "Sega Saturn (linha 2)",
    "Dreamcast",
    "Dreamcast (logo)",
    "Dreamcast (linha)",
    "Sega CD (logo)",
    "Sega CD (linha)",
    "Sega Master System",
    "NEC / PC Engine (logo)",
    "PC Engine / TurboGrafx (linha)",
    "Neo Geo",
    "Neo Geo CD (logo)",
    "PS1",
    "PS1 (logo)",
    "PS1 Slim (logo)",
    "PS1 (Azul)",
    "PS1 (Dual Shock)",
    "PS2",
    "PS2 (logo)",
    "PS3",
    "PSP",
    "Xbox Classic",
    "Xbox (logo)",
    "Xbox 360",
    "Atari 2600 (Joystick)",
    "Atari (logo)",
    "Atari (Fuji)",
    "Atari 2600 (console)",
    "Philips Odyssey",
    "Philips CD-i",
    "Panasonic 3DO",
    "Gravis GamePad",
    "MAME / Arcade",
    "Console Retrô 1",
    "Console Retrô 2",
    "Console Retrô 3",
];
const gbsIconPromptPromise = {
    resolve: null,
    reject: null,
};
let selectedIconId = 0;
const gbsIconPrompt = (currentIconId = 0) => {
    GBSControl.ui.iconPicker.removeAttribute("hidden");
    selectedIconId = currentIconId;
    const items = nodelistToArray(GBSControl.ui.iconPickerGrid.querySelectorAll("[gbs-icon-picker-id]"));
    items.forEach((item) => {
        const id = parseInt(item.getAttribute("gbs-icon-picker-id"), 10);
        if (id === currentIconId) {
            item.setAttribute("active", "");
        }
        else {
            item.removeAttribute("active");
        }
    });
    return new Promise((resolve, reject) => {
        gbsIconPromptPromise.resolve = resolve;
        gbsIconPromptPromise.reject = reject;
    });
};
const initIconPicker = () => {
    const items = [];
    for (let i = 0; i < SLOT_ICON_COUNT; i++) {
        const item = document.createElement("button");
        item.className = "gbs-button gbs-icon-picker__item";
        item.setAttribute("gbs-icon-picker-id", String(i));
        item.innerHTML = `<svg><use href="#gbs-slot-icon-${i}"></use></svg>`;
        // Just select/highlight the icon here - saving only happens on OK, so a
        // stray tap doesn't immediately commit (and trigger a preset save).
        item.addEventListener("click", () => {
            selectedIconId = i;
            items.forEach((el) => el.removeAttribute("active"));
            item.setAttribute("active", "");
        });
        items.push(item);
        GBSControl.ui.iconPickerGrid.appendChild(item);
    }
    GBSControl.ui.iconPickerCancel.addEventListener("click", () => {
        GBSControl.ui.iconPicker.setAttribute("hidden", "");
        if (gbsIconPromptPromise.reject) {
            gbsIconPromptPromise.reject();
        }
    });
    GBSControl.ui.iconPickerOk.addEventListener("click", () => {
        GBSControl.ui.iconPicker.setAttribute("hidden", "");
        if (gbsIconPromptPromise.resolve) {
            gbsIconPromptPromise.resolve(selectedIconId);
        }
    });
};
const initUI = () => {
    updateCustomSlotFilters();
    initGeneralListeners();
    updateViewPort();
    initSlotButtons();
    initLegendHelpers();
    initMenuButtons();
    initGBSButtons();
    initClearButton();
    initControlMobileKeys();
    initUnloadListener();
    initDeveloperMode();
    initHelp();
    initIconPicker();
    initConnectorPicker();
    initOledPresetDisplayButtons();
    initStartupPresetSelect();
    initSlotPager();
    initThemeSelector();
    initLanguageSelector();
};
const main = () => {
    const ip = location.hostname;
    GBSControl.serverIP = ip;
    GBSControl.webSocketServerUrl = `ws://${ip}:81/`;
    document
        .querySelector(".gbs-loader img")
        .setAttribute("src", document.head
        .querySelector('[rel="apple-touch-icon"]')
        .getAttribute("href"));
    fetchSlotNamesAndInit();
};
main();
