# Epic Battle Transitions for Ren'Py - OPTIMIZED & SIMPLIFIED
# High-performance transitions using only built-in Ren'Py features

# ===== GEOMETRIC PATTERN TRANSITIONS =====
# Simple geometric effects using built-in classes

define spiralwipe = Swing(0.8, vertical=False)          # Rotating spiral effect
define diamondwipe = CropMove(0.8, "irisin")            # Diamond iris
define starwipe = CropMove(1.0, "irisin")               # Star-like iris
define hexwipe = CropMove(0.9, "wiperight")             # Hex-like wipe
define trianglewipe = CropMove(0.7, "wipedown")         # Triangle wipe

# ===== RETRO/PIXEL ART INSPIRED =====
# Classic arcade and retro game styles

define scanlinewipe = CropMove(0.8, "wipedown")         # Scanline sweep
define glitchwipe = CropMove(0.6, "slideright")         # Glitchy slide
define pixelburst = Pixellate(0.8, 4)                   # Chunky pixels
define pixeldissolve = Pixellate(1.2, 6)                # Heavy pixelation
define staticwipe = Dissolve(0.5)                       # Static-like dissolve

# ===== ORGANIC/NATURAL PATTERNS =====
# Nature-inspired smooth transitions

define ripplewipe = CropMove(1.2, "irisin")             # Water ripple
define flamewipe = CropMove(0.9, "wipeup")              # Fire lick
define lightningwipe = CropMove(0.4, "wiperight")       # Lightning bolt
define inkblotwipe = CropMove(1.0, "irisin")            # Ink spread
define leafwipe = CropMove(1.3, "slidedown")            # Falling leaves

# ===== MECHANICAL/TECH INSPIRED =====
# Industrial and technological effects

define gearwipe = Swing(1.0, vertical=True)             # Gear rotation
define shutterwipe = CropMove(0.6, "irisin")            # Camera shutter
define circuitwipe = CropMove(0.8, "wiperight")         # Circuit trace
define conveyorwipe = CropMove(0.9, "slideright")       # Conveyor belt
define angleblinds = CropMove(0.8, "wipedown")          # Angled blinds

# ===== SIMPLE GEOMETRIC WIPES =====
# Clean geometric patterns

define crosswipe = CropMove(0.7, "irisin")              # Cross expand
define cornerpeel = CropMove(1.0, "slideawayright")     # Corner peel
define mosaicwipe = Pixellate(1.0, 3)                   # Mosaic blocks
define radialwipe = CropMove(0.8, "irisin")             # Radial sweep
define ringswipe = CropMove(1.1, "irisin")              # Concentric rings

# ===== MINIMAL MODERN EFFECTS =====
# Contemporary smooth transitions

define elasticwipe = Dissolve(0.8)                      # Elastic feel
define foldwipe = CropMove(0.6, "wipedown")             # Paper fold
define slidefade = ComposeTransition(Dissolve(0.5), before=slideawayleft, after=slideright)
define scalerotatewipe = Swing(0.9, vertical=False)     # Scale + rotate
define colorshift = Fade(0.3, 0.1, 0.3, color="#ff00ff") # Color transition

# ===== DIRECTIONAL VARIATIONS =====
# Additional directional options

define spiralleft = Swing(0.8, vertical=False, reverse=True)
define spiralup = Swing(0.8, vertical=True)
define spiraldown = Swing(0.8, vertical=True, reverse=True)

define quickwipe = CropMove(0.3, "wiperight")           # Fast wipe
define slowwipe = CropMove(1.8, "wiperight")            # Slow wipe

# ===== FLASH & COLOR EFFECTS =====
# Color-coded transitions for different moods

define flash_green = Fade(0.05, 0.02, 0.3, color="#0f0")     # Nature/poison
define flash_purple = Fade(0.05, 0.02, 0.3, color="#f0f")    # Magic/psychic
define flash_orange = Fade(0.05, 0.02, 0.3, color="#f80")    # Fire/energy
define flash_cyan = Fade(0.05, 0.02, 0.3, color="#0ff")      # Ice/tech

# ===== SPEED VARIATIONS =====
# Fast, normal, and slow versions of key transitions

define fast_dissolve = Dissolve(0.2)                    # Quick fade
define slow_dissolve = Dissolve(2.0)                    # Dramatic fade
define fast_pixel = Pixellate(0.4, 3)                   # Quick pixels
define slow_pixel = Pixellate(1.8, 8)                   # Slow heavy pixels
define fast_swing = Swing(0.4)                          # Quick spin
define slow_swing = Swing(1.6)                          # Slow dramatic spin

# ===== COMBO TRANSITIONS =====
# Combinations of existing effects

define zoomfade = ComposeTransition(Dissolve(0.6), before=zoomout, after=zoomin)
define spinslide = ComposeTransition(slideright, before=Swing(0.5), after=None)
define pixelslide = ComposeTransition(slidedown, before=Pixellate(0.4, 4), after=None)

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
define flash_gray = Fade(0.1, 0.05, 0.2, color="#888")

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
