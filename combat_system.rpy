# Epic Battle Transitions for Ren'Py - CORRECTED VERSION
# Based on official Ren'Py 8.4+ documentation

# 1. FINAL FANTASY STYLE SPIRAL TRANSITION
transform ff_spiral_out:
    rotate 0 zoom 1.0 alpha 1.0
    linear 1.5 rotate 720 zoom 0.2 alpha 0.0

transform ff_spiral_in:
    rotate -720 zoom 0.2 alpha 0.0
    linear 1.5 rotate 0 zoom 1.0 alpha 1.0

# Using simple dissolve with transforms - ComposeTransition is complex
define ff_spiral = dissolve

# Alternative: Use ATL transitions (the correct way)
transform ff_spiral_transition(duration=2.0, *, new_widget=None, old_widget=None):
    delay duration

    # Handle old widget (spinning out)
    old_widget:
        alpha 1.0 rotate 0 zoom 1.0
        linear (duration/2) alpha 0.0 rotate 360 zoom 0.3

    # Handle new widget (spinning in)
    new_widget:
        alpha 0.0 rotate -360 zoom 0.3
        linear (duration/2) alpha 1.0 rotate 0 zoom 1.0

# 2. GLASS SHATTER EFFECT (Simplified)
transform shatter_out:
    alpha 1.0 rotate 0
    parallel:
        linear 0.3 alpha 1.0
        linear 0.5 alpha 0.0
    parallel:
        linear 0.8 rotate 15 xoffset 50 yoffset -30

define glass_shatter = Dissolve(0.8)  # Simple dissolve for now

# 3. RADIAL IRIS TRANSITION (Using built-in)
define radial_wipe = irisin

# 4. LIGHTNING FLASH TRANSITION
image white_flash:
    Solid("#ffffff")
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.8
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.0

transform lightning_shake:
    xoffset 0 yoffset 0
    block:
        linear 0.02 xoffset 5 yoffset -3
        linear 0.02 xoffset -4 yoffset 2
        linear 0.02 xoffset 3 yoffset -4
        linear 0.02 xoffset -2 yoffset 3
        linear 0.02 xoffset 0 yoffset 0

# Lightning transition using MultipleTransition (correct syntax)
define lightning_flash_transition = MultipleTransition([
    False, Pause(0.1),
    "white_flash", Pause(0.3),
    True
])

# 5. PIXEL DISSOLVE (Using built-in)
define pixel_dissolve = pixellate

# 6. BATTLE SWIPE TRANSITIONS (Using built-ins)
define battle_swipe = slideright
define battle_swipe_left = slideleft
define battle_swipe_up = slideup
define battle_swipe_down = slidedown

# 7. ZOOM BURST TRANSITION
define zoom_burst = zoominout

# 8. SCREEN SHAKE (Standalone effect)
transform epic_shake:
    xoffset 0 yoffset 0
    linear 0.05 xoffset 10 yoffset 0
    linear 0.05 xoffset -10 yoffset 0
    linear 0.05 xoffset 8 yoffset 5
    linear 0.05 xoffset -8 yoffset -5
    linear 0.05 xoffset 5 yoffset 0
    linear 0.05 xoffset -5 yoffset 0
    linear 0.05 xoffset 0 yoffset 0

# 9. CUSTOM SWING TRANSITION (Using built-in Swing class)
define battle_swing = Swing(1.0)

# 10. ADVANCED ATL TRANSITION EXAMPLE (Correct syntax)
transform custom_spin(duration=1.0, *, new_widget=None, old_widget=None):
    # Required: Set transition duration
    delay duration

    # Position everything at screen center
    xcenter 0.5
    ycenter 0.5

    # Animate old widget (spinning out)
    old_widget:
        events False  # Don't let it receive clicks
        rotate 0.0 alpha 1.0
        easeout (duration/2) rotate 360.0 alpha 0.0

    # Animate new widget (spinning in)
    new_widget:
        events True   # Let it receive clicks
        rotate -360.0 alpha 0.0
        easein (duration/2) rotate 0.0 alpha 1.0


# NOTES:
# 1. ATL transitions need new_widget/old_widget parameters and delay property
# 2. ComposeTransition is complex - use simpler alternatives when possible
# 3. Many effects can use Ren'Py's built-in transitions
# 4. MultipleTransition takes a list: [scene1, trans1, scene2, trans2, ...]
# 5. Built-in transitions: dissolve, fade, pixellate, move, ease, zoom*,
#    *punch, blinds, squares, wipe*, slide*, iris*, push*
# 6. Add sound effects: play sound "battle_start.ogg" before transitions

# PERFORMANCE TIPS:
# - Use built-in transitions when possible (they're optimized)
# - Avoid complex ComposeTransitions on slower devices
# - Test all transitions at your target resolution
# - Keep transition times under 2 seconds for good UX

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
