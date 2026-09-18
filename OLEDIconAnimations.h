#ifndef OLED_ICON_ANIMATIONS_H_
#define OLED_ICON_ANIMATIONS_H_
#include <Arduino.h>

// Per-console icon animation used by the OLED screensaver while a custom
// preset is active (see presetScreenSaverHandler() in
// OLEDMenuImplementation.cpp). iconId matches the webui's slot icon id
// (public/src/index.html.tpl, symbols named "gbs-slot-icon-<id>"), so the
// same icon chosen in the "Escolha um icone" picker at save time drives
// both the webui icon and this animation.
struct IconAnimation
{
    uint8_t iconId;
    uint8_t frameCount;
    uint8_t width;
    uint8_t height;
    // frameCount pointers to PROGMEM XBM-packed byte arrays (1 bit per
    // pixel, row-major, LSB first per byte -- same packing as
    // scripts/make_boot_logo.py's to_xbm_bytes()).
    const uint8_t *const *frames;
};

// GENERATED (see OLEDIconAnimations.cpp) from scripts/make_icon_animation.py
// + assets_in/icons/animations_manifest.json. Do not hand-edit the .cpp;
// edit the manifest and rerun the script instead.
extern const IconAnimation ICON_ANIMATIONS[];
extern const uint8_t ICON_ANIMATIONS_COUNT;

// Looks up the animation table entry for a slot icon id. Returns nullptr if
// no animation has been made for that icon yet, so callers should fall back
// to a generic visual.
const IconAnimation *findIconAnimation(uint8_t iconId);

#endif
