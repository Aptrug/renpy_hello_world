# transitions.rpy
init python:
    import random

# 1. FINAL FANTASY STYLE SPIRAL TRANSITION
transform ff_spiral_out:
    linear 1.5 rotate 720 zoom 0.2 alpha 0.0

transform ff_spiral_in:
    linear 1.5 rotate -720 zoom 1.0 alpha 1.0

define ff_spiral_transition = Transition(ff_spiral_out)

# 2. GLASS SHATTER TRANSITION
image shatter_overlay:
    "gui/overlay.png"  # Transparent PNG with cracks
    alpha 0.0

transform glass_shatter_out:
    alpha 1.0
    linear 0.3 alpha 1.0
    linear 0.5 alpha 0.0 xoffset 200 yoffset -150 rotate 45

transform glass_shatter_in:
    alpha 0.0
    linear 0.5 alpha 1.0 xoffset 0 yoffset 0 rotate 0

define glass_shatter_transition = Transition(glass_shatter_out)

# 3. RADIAL WIPE TRANSITION (Iris effect)
transform radial_out:
    zoom 1.0 alpha 1.0
    linear 1.0 zoom 0.0 alpha 0.0

transform radial_in:
    zoom 0.0 alpha 0.0
    linear 1.0 zoom 1.0 alpha 1.0

define radial_wipe_transition = Transition(radial_out)

# 4. LIGHTNING FLASH TRANSITION
image lightning_flash:
    Solid("#ffffff")
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.8
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.0

transform lightning_shake:
    linear 0.02 xoffset 5 yoffset -3
    linear 0.02 xoffset -4 yoffset 2
    linear 0.02 xoffset 3 yoffset -4
    linear 0.02 xoffset -2 yoffset 3
    linear 0.02 xoffset 0 yoffset 0

define lightning_flash_transition = Transition(lightning_flash)

# 5. PIXEL DISSOLVE TRANSITION
transform pixel_dissolve_out:
    alpha 1.0
    linear 0.5 alpha 0.0

transform pixel_dissolve_in:
    alpha 0.0
    linear 0.5 alpha 1.0

define pixel_dissolve_transition = Transition(pixel_dissolve_out)

# BONUS: CLASSIC BATTLE SWIPE (Horizontal)
transform battle_swipe_out:
    xalign 0.0
    linear 0.8 xalign 1.0

transform battle_swipe_in:
    xalign 1.0
    linear 0.8 xalign 0.0

define battle_swipe_transition = Transition(battle_swipe_out)

# USAGE EXAMPLES

screen battle_ui():
    # Boss image (centered top)
    add "images/combat_system/boss.webp" xpos 0.5 ypos 0.1 anchor (0.5, 0.0)

    # Allies row (bottom)
    hbox:
        xpos 0.5
        ypos 0.9
        anchor (0.5, 1.0)
        spacing 20

        add "images/combat_system/kanami.webp"
        add "images/combat_system/kenshin.webp"
        add "images/combat_system/magic.webp"
        add "images/combat_system/rance.webp"
        add "images/combat_system/reset.webp"
        add "images/combat_system/sachiko.webp"
        add "images/combat_system/suzume.webp"
