# Epic Battle Transitions for Ren'Py - CORRECT ATL SYNTAX
# Based on working forum examples and documentation

# 1. PROPER ATL TRANSITION SYNTAX (using 'contains:')
transform battle_spiral(new_widget, old_widget):
    delay 2.0

    contains:
        old_widget
        alpha 1.0 rotate 0 zoom 1.0
        linear 1.0 alpha 0.0 rotate 360 zoom 0.3

    contains:
        new_widget
        alpha 0.0 rotate -360 zoom 0.3
        linear 1.0 alpha 1.0 rotate 0 zoom 1.0

transform shatter_transition(new_widget, old_widget):
    delay 1.0

    contains:
        old_widget
        alpha 1.0 rotate 0 xoffset 0 yoffset 0
        parallel:
            linear 0.3 alpha 1.0
            linear 0.7 alpha 0.0
        parallel:
            linear 1.0 rotate 25 xoffset 100 yoffset -50

    contains:
        new_widget
        alpha 0.0
        linear 1.0 alpha 1.0

transform zoom_burst_transition(new_widget, old_widget):
    delay 1.0

    contains:
        old_widget
        zoom 1.0 alpha 1.0
        linear 0.5 zoom 3.0 alpha 0.0

    contains:
        new_widget
        zoom 0.1 alpha 0.0
        linear 0.5 zoom 1.0 alpha 1.0

transform spin_transition(new_widget, old_widget):
    delay 1.0

    contains:
        old_widget
        rotate 0.0 alpha 1.0
        linear 0.5 rotate 360.0 alpha 0.0

    contains:
        new_widget
        rotate -360.0 alpha 0.0
        linear 0.5 rotate 0.0 alpha 1.0

# 2. BUILT-IN TRANSITIONS (Recommended - these always work)
define ff_spiral = dissolve
define glass_shatter = Dissolve(0.8)
define radial_wipe = irisin
define pixel_dissolve = pixellate
define battle_swipe = slideright
define zoom_burst = zoominout
define battle_swing = Swing(1.0)

# 3. LIGHTNING FLASH TRANSITION
image white_flash:
    Solid("#ffffff")
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.8
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.0

define lightning_flash = MultipleTransition([
    False, Pause(0.1),
    "white_flash", Pause(0.3),
    True
])

# 4. SCREEN SHAKE TRANSFORM
transform epic_shake:
    xoffset 0 yoffset 0
    linear 0.05 xoffset 10 yoffset 0
    linear 0.05 xoffset -10 yoffset 0
    linear 0.05 xoffset 8 yoffset 5
    linear 0.05 xoffset -8 yoffset -5
    linear 0.05 xoffset 5 yoffset 0
    linear 0.05 xoffset -5 yoffset 0
    linear 0.05 xoffset 0 yoffset 0

# 5. MORE BUILT-IN OPTIONS
define slow_dissolve = Dissolve(2.0)
define fast_dissolve = Dissolve(0.3)
define fade_to_black = Fade(0.5, 0.5, 0.5)
define camera_flash = Fade(0.1, 0.0, 0.5, color="#fff")

# NOTES:
# 1. ATL transitions use 'contains:' blocks, not direct colons
# 2. Parameters are (new_widget, old_widget) - no asterisk or defaults needed
# 3. Built-in transitions are more reliable and performant
# 4. Always set 'delay' property in ATL transitions
# 5. Test thoroughly on your target platform

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
