# Epic Battle Transitions for Ren'Py (1920x1080)
# Place this code in your script.rpy file or create a separate transitions.rpy file

init python:
    import math
    import random

    # Helper function for creating dynamic transforms
    def spiral_transform(t):
        """Creates a spiral transformation for FF-style transitions"""
        angle = t * 720  # Two full rotations
        scale_factor = 1.0 - (t * 0.8)
        return Transform(
            rotate=angle,
            zoom=scale_factor,
            alpha=1.0 - (t * t)  # Quadratic fade
        )

    def shatter_piece_transform(piece_id, t):
        """Individual glass shard transformation"""
        # Each piece flies in a different direction
        random.seed(piece_id)  # Consistent randomization
        angle = random.uniform(0, 360)
        distance = t * random.uniform(200, 800)
        rotation = t * random.uniform(-180, 180)

        x_offset = math.cos(math.radians(angle)) * distance
        y_offset = math.sin(math.radians(angle)) * distance

        return Transform(
            xoffset=x_offset,
            yoffset=y_offset,
            rotate=rotation,
            alpha=1.0 - (t * 1.5)
        )

# 1. FINAL FANTASY STYLE SPIRAL TRANSITION
transform ff_spiral_out:
    # Start normal, then spiral and shrink
    linear 0.0 rotate 0 zoom 1.0 alpha 1.0
    linear 1.5 rotate 720 zoom 0.2 alpha 0.0

transform ff_spiral_in:
    # Start spiraled and small, expand to normal
    linear 0.0 rotate -720 zoom 0.2 alpha 0.0
    linear 1.5 rotate 0 zoom 1.0 alpha 1.0

# Create the transition
define ff_spiral = ComposeTransition(
    ff_spiral_out, Pause(0.1), ff_spiral_in,
    time_warp=None
)

# 2. GLASS SHATTER TRANSITION
image shatter_overlay:
    # Create a cracked glass overlay effect
    "cracked_screen.png"  # You'll need a transparent PNG with crack lines
    alpha 0.0
    linear 0.3 alpha 1.0
    linear 0.2 alpha 0.0

transform glass_shatter_out:
    # Screen cracks then shatters
    linear 0.0 alpha 1.0
    linear 0.3 alpha 1.0  # Brief pause as cracks appear
    parallel:
        linear 0.5 alpha 0.0
    parallel:
        # Multiple shatter pieces effect
        block:
            choice:
                linear 0.5 xoffset 200 yoffset -150 rotate 45
            choice:
                linear 0.5 xoffset -180 yoffset 200 rotate -60
            choice:
                linear 0.5 xoffset 150 yoffset 180 rotate 30
            choice:
                linear 0.5 xoffset -200 yoffset -100 rotate -45

transform glass_shatter_in:
    # Pieces reassemble
    alpha 0.0 rotate 0 xoffset 0 yoffset 0
    linear 0.5 alpha 1.0

define glass_shatter = ComposeTransition(
    glass_shatter_out, Pause(0.1), glass_shatter_in,
    time_warp=None
)

# 3. RADIAL WIPE TRANSITION (Iris effect)
transform radial_out:
    # Create circular mask effect shrinking to center
    size (1920, 1080)
    crop (0, 0, 1920, 1080)
    linear 1.0 crop (960, 540, 0, 0)  # Shrink to center point

transform radial_in:
    # Expand from center
    crop (960, 540, 0, 0)
    linear 1.0 crop (0, 0, 1920, 1080)

define radial_wipe = ComposeTransition(
    radial_out, Pause(0.05), radial_in,
    time_warp=None
)

# 4. LIGHTNING FLASH TRANSITION
image lightning_flash:
    # White flash overlay
    Solid("#ffffff")
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.8
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.0

transform lightning_shake:
    # Screen shake effect
    linear 0.0 xoffset 0 yoffset 0
    linear 0.02 xoffset 5 yoffset -3
    linear 0.02 xoffset -4 yoffset 2
    linear 0.02 xoffset 3 yoffset -4
    linear 0.02 xoffset -2 yoffset 3
    linear 0.02 xoffset 0 yoffset 0
    linear 0.3 xoffset 0 yoffset 0  # Settle

transform lightning_out:
    alpha 1.0
    parallel:
        lightning_shake
    parallel:
        linear 0.3 alpha 0.0

transform lightning_in:
    alpha 0.0
    parallel:
        lightning_shake
    parallel:
        linear 0.3 alpha 1.0

define lightning_flash_transition = MultipleTransition([
    False, Pause(0.1),
    "lightning_flash", Pause(0.3),
    False, Pause(0.1),
    True, lightning_in
])

# 5. PIXEL DISSOLVE TRANSITION
transform pixel_dissolve_out:
    # Pixelated breakdown effect
    alpha 1.0
    parallel:
        # Gradual pixelation (simulated with blur and scaling)
        linear 0.5 blur 0
        linear 0.5 blur 10
    parallel:
        # Random alpha flicker
        block:
            linear 0.1 alpha 1.0
            linear 0.1 alpha 0.7
            linear 0.1 alpha 1.0
            linear 0.1 alpha 0.5
            linear 0.1 alpha 0.8
            linear 0.5 alpha 0.0

transform pixel_dissolve_in:
    alpha 0.0 blur 10
    parallel:
        linear 0.5 blur 0
    parallel:
        linear 0.5 alpha 1.0

define pixel_dissolve = ComposeTransition(
    pixel_dissolve_out, Pause(0.1), pixel_dissolve_in,
    time_warp=None
)

# BONUS: CLASSIC BATTLE SWIPE (Horizontal)
transform battle_swipe_out:
    crop (0, 0, 1920, 1080)
    linear 0.8 crop (1920, 0, 0, 1080)  # Wipe left to right

transform battle_swipe_in:
    crop (0, 0, 0, 1080)
    linear 0.8 crop (0, 0, 1920, 1080)

define battle_swipe = ComposeTransition(
    battle_swipe_out, Pause(0.05), battle_swipe_in,
    time_warp=None
)

# USAGE EXAMPLES IN YOUR SCRIPT:

# Example usage in your game script:
# ADDITIONAL NOTES:
# 1. For glass_shatter, create a "gui/overlay.png" with crack lines
# 2. These work best at 1920x1080 resolution as specified
# 3. You can adjust timing by changing the linear duration values
# 4. Add sound effects with renpy.sound.play() for maximum impact
# 5. Some effects may need additional images in your images folder

# ADVANCED CUSTOMIZATION:
# You can modify the duration, rotation angles, and movement distances
# Example: Change linear 1.5 to linear 2.0 for slower transitions
# Or modify rotate 720 to rotate 1080 for more spirals

# For even more epic effects, combine with screen shake:
transform epic_shake:
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 xoffset 0
    repeat 3

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
