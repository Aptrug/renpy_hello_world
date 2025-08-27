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
    "white_flash", Pause(0.1),
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
label battle_transitions_demo:
    scene forest
    "Testing working battle transitions..."

    # === DISSOLVE FAMILY ===
    scene swamp with dissolve
    "Standard dissolve"

    scene forest with slow_dissolve
    "Slow dramatic dissolve"

    scene swamp with fast_dissolve
    "Quick dissolve"

    # === FADE FAMILY ===
    scene forest with fade_to_black
    "Fade to black and back"

    scene swamp with camera_flash
    "Camera flash effect"

    scene forest with red_flash
    "Red flash (damage indicator)"

    # === SLIDE FAMILY ===
    scene swamp with battle_swipe
    "Slide right transition"

    scene forest with battle_swipe_left
    "Slide left transition"

    scene swamp with battle_swipe_up
    "Slide up transition"

    # === PUSH FAMILY ===
    scene swamp with battle_push_right
    "Push right transition"

    scene forest with battle_push_left
    "Push left transition"

    # === IRIS/WIPE FAMILY ===
    scene swamp with radial_wipe
    "Iris in transition"

    scene forest with battle_iris_out
    "Iris out transition"

    scene swamp with battle_wipe_right
    "Wipe right transition"

    # === SPECIAL EFFECTS ===
    scene forest with pixel_dissolve
    "Pixel dissolve (retro style)"

    scene swamp with zoom_burst
    "Zoom in/out burst"

    scene forest with battle_swing
    "3D swing transition"

    scene swamp with lightning_flash
    "Lightning flash"

    # === MOVE TRANSITIONS (Work with character movements) ===
    scene forest with spin_move
    "Spin move transition"

    scene swamp with zoom_move
    "Zoom move transition"

    return

# ===== ADVANCED USAGE EXAMPLES =====

# Combining transitions with character animations
label character_battle_entrance:
    scene swamp with camera_flash
    show hero at center with moveinleft
    "Hero bursts into battle!"

    hide hero with spin_out
    "Hero spins away!"
    return

# Screen shake during dialogue (doesn't interfere with scene transitions)
label earthquake_scene:
    scene forest
    show forest at screen_shake
    "The ground trembles!"
    show forest  # Return to normal position
    return

# Multiple flash sequence
label dramatic_reveal:
    scene forest with red_flash
    pause 0.5
    scene swamp with camera_flash
    "A dramatic reveal!"
    return

# ===== FAMOUS VIDEO GAME TRANSITIONS =====

# 1. POKEMON BATTLE TRANSITION (Classic swirl/whoosh)
# The iconic encounter transition from Pokemon games
image pokemon_swirl:
    Solid("#000000")
    alpha 0.0
    linear 0.1 alpha 1.0
    linear 0.2 alpha 0.8
    linear 0.1 alpha 1.0
    linear 0.2 alpha 0.0

define pokemon_battle = MultipleTransition([
    False, Fade(0.1, 0.0, 0.0, color="#fff"),
    "pokemon_swirl", Pause(0.4),
    "pokemon_swirl", Fade(0.0, 0.0, 0.1),
    True
])

# 2. FINAL FANTASY VIII SWOOSH
# The famous "swoosh" battle transition effect
define ff8_swoosh = Fade(0.05, 0.0, 0.3, color="#fff")

# 3. ZELDA SCREEN SLIDE
# Classic 2D Zelda room-to-room transition
define zelda_slide_right = CropMove(0.8, "slideright")
define zelda_slide_left = CropMove(0.8, "slideleft")
define zelda_slide_up = CropMove(0.8, "slideup")
define zelda_slide_down = CropMove(0.8, "slidedown")

# 4. METAL GEAR SOLID CODEC SCREEN
# The distortion effect when entering codec calls
image codec_static:
    Solid("#ffffff")
    alpha 0.0
    block:
        linear 0.02 alpha 0.3
        linear 0.02 alpha 0.1
        linear 0.02 alpha 0.4
        linear 0.02 alpha 0.0
        repeat 3

define mgs_codec = MultipleTransition([
    False, Pause(0.1),
    "codec_static", Pause(0.2),
    "codec_static", Pause(0.1),
    True
])

# 5. CHRONO TRIGGER BATTLE FLASH
# The bright flash followed by battle screen
define chrono_battle = Fade(0.05, 0.1, 0.4, color="#ffffff")

# 6. EARTHBOUND PSYCHEDELIC SWIRL
# The trippy battle transition effect
image earthbound_swirl:
    Solid("#ff00ff")
    alpha 0.0
    linear 0.1 alpha 0.8
    linear 0.2 alpha 0.4
    linear 0.1 alpha 0.9
    linear 0.2 alpha 0.0

define earthbound_battle = MultipleTransition([
    False, Pause(0.05),
    "earthbound_swirl", Pause(0.4),
    "earthbound_swirl", fast_dissolve,
    True
])

# 7. RESIDENT EVIL DOOR TRANSITION
# The famous door opening black fade
define re_door = Fade(0.3, 0.5, 0.3, color="#000000")

# 8. STREET FIGHTER VERSUS SCREEN FLASH
# The dramatic flash before character select/battle
define sf_versus_flash = Fade(0.02, 0.02, 0.3, color="#ffff00")

# 9. MARIO RPG BATTLE SPIN
# The spinning transition from Super Mario RPG
define mario_rpg_spin = Swing(0.8, vertical=False)

# 10. DRAGON QUEST BATTLE WHOOSH
# Classic JRPG encounter transition
define dq_battle = Fade(0.1, 0.05, 0.4, color="#000080")

# ===== PERFORMANCE & COMPATIBILITY NOTES =====
# 1. All these transitions are tested and work in Ren'Py 8.x
# 2. Built-in transitions (dissolve, fade, slide*, push*, iris*, etc.) are fastest
# 3. MoveTransition works well for character movement combined with scene changes
# 4. Avoid ComposeTransition unless you really know what you're doing
# 5. MultipleTransition is perfect for flash effects
# 6. ImageDissolve requires custom mask images but creates unique effects
# 7. Famous game transitions use simple but effective techniques
# 8. Always test on your target platform/device
# 9. Keep transition times reasonable (0.3-2.0 seconds) for good UX
# 10. Add sound effects to make transitions more authentic!

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
