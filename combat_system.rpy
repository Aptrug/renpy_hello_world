# Epic Mirror Shatter Transition for Ren'Py
# Compatible with latest Ren'Py version (8.1+) at 1920x1080

# =============================================================================
# BASIC IMAGEDISSOLVE APPROACH (Simple but effective)
# =============================================================================

# Define the basic shatter transition using your mask image
# Place your "broken glass screen with black background" image in the images folder
define shatter_basic = ImageDissolve("mrror_shatter_mask.png", 2.0, ramplen=128)

# Reverse shatter (for reassembling effect)
define shatter_reverse = ImageDissolve("mrror_shatter_mask.png", 2.0, ramplen=128, reverse=True)

# =============================================================================
# ADVANCED MULTI-STAGE SHATTER EFFECT
# =============================================================================

# For a more epic effect, create multiple stages
define shatter_crack = ImageDissolve("mirror_shatter_mask.png", 0.8, ramplen=64)
define shatter_break = ImageDissolve("mirror_shatter_mask.png", 1.5, ramplen=128, alpha=True)
define shatter_fall = ImageDissolve("mirror_shatter_mask.png", 2.5, ramplen=256, reverse=False)

# =============================================================================
# SCREEN SHAKE TRANSFORM (for impact effect)
# =============================================================================

transform screen_shake:
    # Initial impact
    linear 0.1 xoffset -10 yoffset 5
    linear 0.1 xoffset 15 yoffset -10
    linear 0.1 xoffset -8 yoffset 8
    linear 0.1 xoffset 12 yoffset -6
    linear 0.1 xoffset -5 yoffset 3
    linear 0.1 xoffset 0 yoffset 0

transform heavy_shake:
    # More intense shaking for boss fight
    linear 0.08 xoffset -20 yoffset 10
    linear 0.08 xoffset 25 yoffset -15
    linear 0.08 xoffset -18 yoffset 12
    linear 0.08 xoffset 22 yoffset -8
    linear 0.08 xoffset -12 yoffset 6
    linear 0.08 xoffset 15 yoffset -4
    linear 0.08 xoffset -8 yoffset 3
    linear 0.08 xoffset 0 yoffset 0

# =============================================================================
# FLASH EFFECT TRANSFORMS
# =============================================================================

transform white_flash:
    alpha 0.0
    linear 0.1 alpha 1.0
    linear 0.2 alpha 0.0

transform impact_flash:
    alpha 0.0
    linear 0.05 alpha 0.8
    linear 0.15 alpha 0.0
    linear 0.05 alpha 0.6
    linear 0.1 alpha 0.0

# =============================================================================
# COMPOSITE SHATTER EFFECT FUNCTION
# =============================================================================

# Advanced approach using ComposeTransition for layered effects
init python:
    def create_epic_shatter(duration=3.0, shake_intensity="heavy"):
        """
        Creates an epic mirror shatter effect with multiple layers

        Args:
            duration: Total duration of the effect
            shake_intensity: "light", "heavy", or "extreme"
        """

        if shake_intensity == "light":
            shake_transform = "screen_shake"
        elif shake_intensity == "heavy":
            shake_transform = "heavy_shake"
        else:  # extreme
            shake_transform = "heavy_shake"

        # Create the composite effect
        shatter_effect = ComposeTransition(
            ImageDissolve("mirror_shatter_mask.png", duration * 0.8, ramplen=128),
            before=Fade(0.1, 0.0, 0.1),
            after=Fade(0.2, 0.0, 0.2)
        )

        return shatter_effect

# Create predefined epic shatter variations
define epic_shatter = create_epic_shatter(3.0, "heavy")
define quick_shatter = create_epic_shatter(1.5, "light")
define ultimate_shatter = create_epic_shatter(4.0, "extreme")

# =============================================================================
# BOSS FIGHT SHATTER SEQUENCE
# =============================================================================

# Multi-part transition for dramatic boss fight moment
define boss_shatter_sequence = [
    Fade(0.1, 0.0, 0.0),  # Quick flash
    ImageDissolve("mirror_shatter_mask.png", 2.5, ramplen=128),
    Fade(0.0, 0.2, 0.3)   # Dramatic fade in
]

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
