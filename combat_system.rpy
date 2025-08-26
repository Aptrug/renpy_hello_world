# Epic Battle Transitions for Ren'Py - Fixed and Simplified
# Place this in your script.rpy file or create a separate transitions.rpy file

# 1. FINAL FANTASY STYLE SPIRAL TRANSITION
transform ff_spiral_out:
    rotate 0 zoom 1.0 alpha 1.0
    linear 1.5 rotate 720 zoom 0.2 alpha 0.0

transform ff_spiral_in:
    rotate -720 zoom 0.2 alpha 0.0
    linear 1.5 rotate 0 zoom 1.0 alpha 1.0

define ff_spiral = ComposeTransition(
    ff_spiral_out, Pause(0.1), ff_spiral_in
)

# 2. GLASS SHATTER TRANSITION
# Note: You'll need to create a cracked glass overlay image
image shatter_overlay:
    "images/crack_overlay.png"  # Create this image with crack lines
    alpha 0.0
    linear 0.3 alpha 1.0
    linear 0.2 alpha 0.0

transform glass_shatter_out:
    alpha 1.0
    parallel:
        linear 0.3 alpha 1.0
        linear 0.5 alpha 0.0
    parallel:
        choice:
            linear 0.5 xoffset 200 yoffset -150 rotate 45
        choice:
            linear 0.5 xoffset -180 yoffset 200 rotate -60
        choice:
            linear 0.5 xoffset 150 yoffset 180 rotate 30

transform glass_shatter_in:
    alpha 0.0 rotate 0 xoffset 0 yoffset 0
    linear 0.5 alpha 1.0

define glass_shatter = ComposeTransition(
    glass_shatter_out, Pause(0.1), glass_shatter_in
)

# 3. RADIAL WIPE TRANSITION (Iris effect)
# Using ImageDissolve with a radial mask would be better, but here's a simple version
transform radial_out:
    zoom 1.0 alpha 1.0
    linear 1.0 zoom 0.0 alpha 0.0

transform radial_in:
    zoom 0.0 alpha 0.0
    linear 1.0 zoom 1.0 alpha 1.0

define radial_wipe = ComposeTransition(
    radial_out, Pause(0.05), radial_in
)

# 4. LIGHTNING FLASH TRANSITION
image lightning_flash:
    Solid("#ffffff")
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.8
    linear 0.05 alpha 1.0
    linear 0.1 alpha 0.0

transform lightning_shake:
    xoffset 0 yoffset 0
    linear 0.02 xoffset 5 yoffset -3
    linear 0.02 xoffset -4 yoffset 2
    linear 0.02 xoffset 3 yoffset -4
    linear 0.02 xoffset -2 yoffset 3
    linear 0.02 xoffset 0 yoffset 0
    linear 0.3 xoffset 0 yoffset 0

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

define lightning_flash_transition = ComposeTransition(
    lightning_out, Pause(0.1), lightning_in
)

# 5. PIXEL DISSOLVE TRANSITION
# Note: Real pixelation requires custom shaders. This simulates with blur.
transform pixel_dissolve_out:
    alpha 1.0 blur 0
    parallel:
        linear 1.0 blur 10
    parallel:
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
    pixel_dissolve_out, Pause(0.1), pixel_dissolve_in
)

# 6. CLASSIC BATTLE SWIPE (using proper crop)
# Create a mask image for better results
image battle_swipe_mask:
    "images/swipe_mask.png"  # Black to white gradient from left to right

# Alternative simple version using movement
transform battle_swipe_out:
    xoffset 0
    linear 0.8 xoffset -1920

transform battle_swipe_in:
    xoffset 1920
    linear 0.8 xoffset 0

define battle_swipe = ComposeTransition(
    battle_swipe_out, Pause(0.05), battle_swipe_in
)

# 7. ZOOM BURST TRANSITION
transform zoom_burst_out:
    zoom 1.0 alpha 1.0
    linear 0.5 zoom 3.0 alpha 0.0

transform zoom_burst_in:
    zoom 0.1 alpha 0.0
    linear 0.5 zoom 1.0 alpha 1.0

define zoom_burst = ComposeTransition(
    zoom_burst_out, Pause(0.05), zoom_burst_in
)

# 8. SCREEN SHAKE HELPER
transform epic_shake:
    xoffset 0
    linear 0.05 xoffset 10
    linear 0.05 xoffset -10
    linear 0.05 xoffset 8
    linear 0.05 xoffset -8
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 xoffset 0

# NOTES:
# 1. Some transitions need custom images:
#    - "images/crack_overlay.png" for glass shatter
#    - "images/swipe_mask.png" for better swipe effect
# 2. Test all transitions at your target resolution
# 3. Add sound effects with "play sound" for better impact
# 4. Adjust timing by changing linear duration values
# 5. For true pixel effects, you'd need custom shaders

# ADVANCED TIPS:
# - Combine transitions with camera movement for more drama
# - Use with statement variations: "with Dissolve(1.0)"
# - Add particle effects using displayables
# - Consider performance on slower devices

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
