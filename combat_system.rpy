# Epic Battle Transitions for Ren'Py - CORRECTED ATL SYNTAX
# Based on official Ren'Py documentation examples

# 1. SIMPLE TRANSFORM EXAMPLES (No new_widget/old_widget)
transform ff_spiral_out:
    rotate 0 zoom 1.0 alpha 1.0
    linear 1.5 rotate 720 zoom 0.2 alpha 0.0

transform ff_spiral_in:
    rotate -720 zoom 0.2 alpha 0.0
    linear 1.5 rotate 0 zoom 1.0 alpha 1.0

# 2. PROPER ATL TRANSITION (Based on official documentation example)
transform spin_transition(duration=1.0, *, new_widget=None, old_widget=None):
    # Set how long this transform will take to complete
    delay duration

    # Center it
    xcenter .5
    ycenter .5

    # Spin the old displayable
    old_widget:
        events False
        rotate 0.
        easeout (duration / 2) rotate 360.0

    # Spin the new displayable
    new_widget:
        events True
        easein (duration / 2) rotate 720.0

# 3. BATTLE SPIRAL TRANSITION
transform battle_spiral(duration=2.0, *, new_widget=None, old_widget=None):
    delay duration
    xcenter 0.5
    ycenter 0.5

    old_widget:
        events False
        alpha 1.0 rotate 0 zoom 1.0
        linear (duration/2) alpha 0.0 rotate 360 zoom 0.3

    new_widget:
        events True
        alpha 0.0 rotate -360 zoom 0.3
        linear (duration/2) alpha 1.0 rotate 0 zoom 1.0

# 4. SHATTER TRANSITION
transform shatter_transition(duration=1.0, *, new_widget=None, old_widget=None):
    delay duration

    old_widget:
        events False
        alpha 1.0 rotate 0 xoffset 0 yoffset 0
        parallel:
            linear 0.3 alpha 1.0
            linear 0.7 alpha 0.0
        parallel:
            linear duration rotate 25 xoffset 100 yoffset -50

    new_widget:
        events True
        alpha 0.0
        linear duration alpha 1.0

# 5. ZOOM BURST TRANSITION
transform zoom_burst_transition(duration=1.0, *, new_widget=None, old_widget=None):
    delay duration
    xcenter 0.5
    ycenter 0.5

    old_widget:
        events False
        zoom 1.0 alpha 1.0
        linear (duration/2) zoom 3.0 alpha 0.0

    new_widget:
        events True
        zoom 0.1 alpha 0.0
        linear (duration/2) zoom 1.0 alpha 1.0

# 6. USING BUILT-IN TRANSITIONS (Recommended for most cases)
define ff_spiral = dissolve
define glass_shatter = Dissolve(0.8)
define radial_wipe = irisin
define pixel_dissolve = pixellate
define battle_swipe = slideright
define zoom_burst = zoominout
define battle_swing = Swing(1.0)

# 7. LIGHTNING FLASH (MultipleTransition)
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

# 8. SCREEN SHAKE TRANSFORM
transform epic_shake:
    xoffset 0 yoffset 0
    linear 0.05 xoffset 10 yoffset 0
    linear 0.05 xoffset -10 yoffset 0
    linear 0.05 xoffset 8 yoffset 5
    linear 0.05 xoffset -8 yoffset -5
    linear 0.05 xoffset 5 yoffset 0
    linear 0.05 xoffset -5 yoffset 0
    linear 0.05 xoffset 0 yoffset 0

# 9. CUSTOM DISSOLVE WITH TIMING
define slow_dissolve = Dissolve(2.0)
define fast_dissolve = Dissolve(0.3)

# NOTES:
# 1. ATL transitions must have old_widget/new_widget parameters and colon after them
# 2. Use 'events False' on old_widget, 'events True' on new_widget
# 3. Built-in transitions are faster and more reliable
# 4. Test all custom transitions thoroughly
# 5. Keep transition times under 2 seconds for good UX

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
