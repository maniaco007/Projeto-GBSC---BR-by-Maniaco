#ifndef _SLOT_H_
#define _SLOT_H_
// SLOTS
#define SLOTS_FILE "/slots.bin" // the file where to store slots metadata
#define SLOTS_TOTAL 72          // max number of slots
#define EMPTY_SLOT_NAME "Empty                   "
// Per-slot console icon, kept in its own file (1 byte per slot) instead of
// growing SlotMeta, so existing slots.bin dumps on already-flashed devices
// keep working unmodified. 0 = no icon / generic.
#define SLOT_ICONS_FILE "/slot_icons.bin"
// Per-slot linked input ("Link Perfil<->Entrada", idea ported from OSSC),
// same 1-byte-per-slot approach as SLOT_ICONS_FILE. 0 = no link, 1 =
// RGB/RGBS, 2 = Componente (same encoding as uopt->inputSourceLock).
#define SLOT_INPUT_FILE "/slot_input.bin"
// Per-slot video source connector label, same 1-byte-per-slot approach.
// 0 = not set (older preset, saved before this existed - shown as nothing),
// 1 = SCART, 2 = VGA, 3 = Componente, 4 = RGBS.
#define SLOT_CONNECTOR_FILE "/slot_conn.bin"
typedef struct
{
    char name[25];
    uint8_t presetID;
    uint8_t scanlines;
    uint8_t scanlinesStrength;
    uint8_t slot;
    uint8_t wantVdsLineFilter;
    uint8_t wantStepResponse;
    uint8_t wantPeaking;
} SlotMeta;

typedef struct
{
    SlotMeta slot[SLOTS_TOTAL]; // the max avaliable slots that can be encoded in a the charset[A-Za-z0-9-._~()!*:,;]
} SlotMetaArray;
#endif