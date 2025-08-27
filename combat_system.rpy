# Epic Battle Transitions for Ren'Py - OPTIMIZED & SIMPLIFIED
# High-performance transitions using only built-in Ren'Py features

# ===== CORE BATTLE TRANSITIONS =====
# Fast, reliable transitions using optimized built-ins

define battle_dissolve = dissolve              # Classic fade
define battle_fast = Dissolve(0.3)             # Quick transition
define battle_slow = Dissolve(1.5)             # Dramatic buildup
define battle_iris = irisin                    # Circular zoom
define battle_pixel = pixellate                # Retro effect
define battle_zoom = zoominout                 # Scale effect
define battle_spin = Swing(0.8)                # 3D rotation

# ===== DIRECTIONAL TRANSITIONS =====
# Movement-based transitions for different battle entrances

define battle_right = slideright               # Slide from right
define battle_left = slideleft                 # Slide from left
define battle_up = slideup                     # Slide from top
define battle_down = slidedown                 # Slide from bottom
define battle_push = PushMove(0.8, "pushright") # Push effect

# ===== FLASH EFFECTS =====
# Color-coded flashes for different battle types

define flash_white = Fade(0.05, 0.02, 0.3, color="#fff")    # Lightning/holy
define flash_red = Fade(0.05, 0.02, 0.3, color="#f00")      # Fire/damage
define flash_blue = Fade(0.05, 0.02, 0.3, color="#00f")     # Ice/magic
define flash_yellow = Fade(0.05, 0.02, 0.3, color="#ff0")   # Electric
define flash_black = Fade(0.2, 0.3, 0.2, color="#000")      # Dark/mystery
define colorshift = Fade(0.3, 0.1, 0.3, color="#ff00ff")

# # ===== FAMOUS GAME STYLES =====
# # Simplified versions of iconic game transitions
#
# define pokemon_style = flash_white             # Pokemon encounter
# define ff_style = flash_white                  # Final Fantasy
# define zelda_style = battle_right              # Zelda room change
# define mario_style = battle_spin               # Mario RPG
# define retro_style = battle_pixel              # Classic JRPG

# ===== SCREEN EFFECTS =====
# Simple transforms for show/hide animations

transform shake:
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 xoffset 3
    linear 0.05 xoffset -3
    linear 0.05 xoffset 0

transform zoom_out:
    linear 0.8 zoom 3.0 alpha 0.0

transform spin_away:
    linear 1.0 rotate 360 alpha 0.0

# # ===== USAGE EXAMPLES =====
# label optimized_battle_demo:
#     scene bg forest
#     "Optimized battle transitions - choose your style!"
#
#     # Core transitions
#     scene bg battle with battle_dissolve
#     "Classic dissolve"
#
#     scene bg forest with battle_fast
#     "Quick battle start"
#
#     scene bg battle with battle_iris
#     "Iris zoom effect"
#
#     scene bg forest with battle_pixel
#     "Retro pixel style"
#
#     # Directional effects
#     scene bg battle with battle_right
#     "Side entrance"
#
#     scene bg forest with battle_push
#     "Push transition"
#
#     # Flash effects
#     scene bg battle with flash_red
#     "Fire battle!"
#
#     scene bg forest with flash_blue
#     "Ice magic!"
#
#     scene bg battle with flash_yellow
#     "Lightning strike!"
#
#     # Famous game styles
#     scene bg forest with pokemon_style
#     "Pokemon encounter!"
#
#     scene bg battle with mario_style
#     "Mario RPG spin!"
#
#     scene bg forest with retro_style
#     "Classic JRPG pixel!"
#
#     return
#
# # ===== ADVANCED USAGE =====
# # Combining effects for maximum impact
#
# label advanced_battle_effects:
#     # Sound + transition combo
#     play sound "battle_start.ogg"
#     scene bg battle with flash_white
#     "Epic battle begins!"
#
#     # Character movement with transition
#     scene bg forest with battle_left
#     show hero at center with moveinright
#     "Hero charges in!"
#
#     # Screen shake during dialogue
#     show bg battle at shake
#     "The ground trembles!"
#     show bg battle  # Reset position
#
#     # Quick sequence
#     scene bg forest with battle_fast
#     scene bg battle with flash_red
#     scene bg forest with battle_dissolve
#     "Combo attack sequence!"
#
#     return

# ===== PERFORMANCE NOTES =====
# 1. All transitions use Ren'Py built-ins (fastest performance)
# 2. No custom images required (no loading delays)
# 3. Simple timing (0.3-1.5s for good UX)
# 4. Color-based effects (lightweight)
# 5. Reusable definitions (memory efficient)
# 6. Compatible with all Ren'Py versions 8.x+
# 7. Mobile-friendly (tested on slower devices)

# ===== CUSTOMIZATION TIPS =====
# - Adjust timings: Dissolve(0.5) -> Dissolve(1.0) for slower
# - Change colors: color="#fff" -> color="#f0f" for different mood
# - Combine with sound: play sound before transitions
# - Use with character animations: show/hide with movein*
# - Test on target platform for optimal timing

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
