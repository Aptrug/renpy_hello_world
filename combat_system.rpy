# Epic Battle Transitions for Ren'Py - SIMPLIFIED & OPTIMIZED
# Focus on working transitions with clean, simple code

# ===== BUILT-IN TRANSITIONS (RECOMMENDED) =====
# These are optimized, reliable, and always work

define ff_spiral = dissolve                    # Simple dissolve
define glass_shatter = Dissolve(0.8)          # Timed dissolve
define radial_wipe = irisin                    # Circular iris
define pixel_dissolve = pixellate              # Pixel effect
define battle_swipe = slideright               # Horizontal slide
define battle_swipe_left = slideleft           # Left slide
define battle_swipe_up = slideup               # Up slide
define battle_swipe_down = slidedown           # Down slide
define zoom_burst = zoominout                  # Zoom effect
define battle_swing = Swing(1.0)               # 3D flip

# ===== CUSTOM SIMPLE TRANSITIONS =====
# Using basic Dissolve and Fade classes for reliability

define slow_dissolve = Dissolve(2.0)
define fast_dissolve = Dissolve(0.3)
define fade_to_black = Fade(0.5, 0.5, 0.5)
define camera_flash = Fade(0.1, 0.0, 0.5, color="#fff")
define red_flash = Fade(0.1, 0.0, 0.3, color="#f00")

# ===== WORKING ATL TRANSITIONS =====
# Simplified versions that actually work

# Simple spiral zoom effect
transform simple_spiral:
    linear 0.0 rotate 0 zoom 1.0 alpha 1.0
    linear 1.0 rotate 360 zoom 0.5 alpha 0.0

# Screen shake effect (standalone)
transform screen_shake:
    linear 0.0 xoffset 0 yoffset 0
    linear 0.05 xoffset 5 yoffset -3
    linear 0.05 xoffset -5 yoffset 3
    linear 0.05 xoffset 3 yoffset -2
    linear 0.05 xoffset -3 yoffset 2
    linear 0.05 xoffset 0 yoffset 0

# Zoom out effect
transform zoom_out:
    linear 0.0 zoom 1.0 alpha 1.0
    linear 0.8 zoom 3.0 alpha 0.0

# Zoom in effect
transform zoom_in:
    linear 0.0 zoom 0.3 alpha 0.0
    linear 0.8 zoom 1.0 alpha 1.0

# Spin out effect
transform spin_out:
    linear 0.0 rotate 0 alpha 1.0
    linear 1.0 rotate 360 alpha 0.0

# ===== LIGHTNING FLASH =====
image white_flash:
    Solid("#ffffff")
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.7
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.0

define lightning_flash = MultipleTransition([
    False, Pause(0.1),
    "white_flash", Pause(0.25),
    True
])

# ===== WORKING CUSTOM ATL TRANSITION =====
# Based on official documentation example
transform working_spin(duration=1.0):
    delay duration
    xcenter 0.5
    ycenter 0.5
    rotate 0
    linear duration rotate 360 alpha 0.5
    linear 0.0 rotate 0 alpha 1.0

# ===== COMPOSITE TRANSITIONS =====
# Using ComposeTransition correctly (simple version)
define spin_dissolve = ComposeTransition(dissolve, before=spin_out, after=None)
define zoom_dissolve = ComposeTransition(dissolve, before=zoom_out, after=zoom_in)

# ===== USAGE EXAMPLES =====
label battle_transitions:

# ===== PERFORMANCE NOTES =====
# 1. Built-in transitions (dissolve, fade, etc.) are fastest
# 2. Simple ATL transforms work better than complex ones
# 3. Avoid nested parallel blocks in ATL
# 4. Test on slower devices if targeting mobile
# 5. Use shorter durations (0.5-1.5s) for better UX
# 6. MultipleTransition is good for flash effects
# 7. ComposeTransition can be expensive - use sparingly

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
