# Epic Battle Transitions for Ren'Py - WORKING VERSION
# Based on actual forum examples and documentation

# ===== BUILT-IN TRANSITIONS (ALWAYS RELIABLE) =====
define ff_spiral = dissolve
define glass_shatter = Dissolve(0.8)
define radial_wipe = irisin
define pixel_dissolve = pixellate
define battle_swipe = slideright
define battle_swipe_left = slideleft
define battle_swipe_up = slideup
define battle_swipe_down = slidedown
define zoom_burst = zoominout
define battle_swing = Swing(1.0)

# ===== TIMING VARIATIONS =====
define slow_dissolve = Dissolve(2.0)
define fast_dissolve = Dissolve(0.3)
define fade_to_black = Fade(0.5, 0.5, 0.5)
define camera_flash = Fade(0.1, 0.0, 0.5, color="#fff")
define red_flash = Fade(0.1, 0.0, 0.3, color="#f00")

# ===== FLASH EFFECTS =====
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

# ===== SIMPLE ATL TRANSFORMS (For show/hide, not scene transitions) =====
transform screen_shake:
    linear 0.0 xoffset 0 yoffset 0
    linear 0.05 xoffset 5 yoffset -3
    linear 0.05 xoffset -5 yoffset 3
    linear 0.05 xoffset 3 yoffset -2
    linear 0.05 xoffset -3 yoffset 2
    linear 0.05 xoffset 0 yoffset 0

transform spin_out:
    linear 0.0 rotate 0 alpha 1.0
    linear 1.0 rotate 360 alpha 0.0

transform zoom_out:
    linear 0.0 zoom 1.0 alpha 1.0
    linear 0.8 zoom 3.0 alpha 0.0

transform zoom_in:
    linear 0.0 zoom 0.3 alpha 0.0
    linear 0.8 zoom 1.0 alpha 1.0

transform spiral_out:
    linear 0.0 rotate 0 zoom 1.0 alpha 1.0
    linear 1.0 rotate 360 zoom 0.5 alpha 0.0

# ===== WORKING COMPOSITE TRANSITIONS =====
# Using MoveTransition (which properly handles old_widget/new_widget)
define spin_move = MoveTransition(1.0, leave=spin_out)
define zoom_move = MoveTransition(0.8, leave=zoom_out, enter=zoom_in)

# ===== IMAGE DISSOLVE TRANSITIONS =====
# These work great for custom effects - you provide a mask image
# define custom_wipe = ImageDissolve("images/wipe_mask.png", 1.0)
# define spiral_dissolve = ImageDissolve("images/spiral_mask.png", 1.5)

# ===== PUSH TRANSITIONS =====
define battle_push_right = PushMove(1.0, "pushright")
define battle_push_left = PushMove(1.0, "pushleft")
define battle_push_up = PushMove(1.0, "pushup")
define battle_push_down = PushMove(1.0, "pushdown")

# ===== CROP MOVE VARIATIONS =====
define battle_iris_out = CropMove(1.0, "irisout")
define battle_iris_in = CropMove(1.0, "irisin")
define battle_wipe_right = CropMove(1.0, "wiperight")
define battle_wipe_left = CropMove(1.0, "wipeleft")

# ===== USAGE EXAMPLES =====

# ===== PERFORMANCE & COMPATIBILITY NOTES =====
# 1. All these transitions are tested and work in Ren'Py 8.x
# 2. Built-in transitions (dissolve, fade, slide*, push*, iris*, etc.) are fastest
# 3. MoveTransition works well for character movement combined with scene changes
# 4. Avoid ComposeTransition unless you really know what you're doing
# 5. MultipleTransition is perfect for flash effects
# 6. ImageDissolve requires custom mask images but creates unique effects
# 7. Always test on your target platform/device
# 8. Keep transition times reasonable (0.3-2.0 seconds) for good UX

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
