# Define variables for dynamic updates
default round_number = 59
default max_ap = 9
default available_ap = 3

# Screen to display the round and AP indicator
screen round_ui:
    # Center the UI on a 1920x1080 screen
    frame:
        xalign 0.5 yalign 0.5
        background None  # No frame background, we'll use an image

        # Circular background
        add "round_bg.png":
            xalign 0.5 yalign 0.5

        # Round number text
        vbox:
            xalign 0.5 yalign 0.5
            text "Round" style "round_label"
            text "[round_number]" style "round_number"

        # Orbs positioned in a circle
        python:
            import math  # Import math module for trigonometric functions
            radius = 64  # Radius of the orb circle (half of 128px background)
            orb_size = 32  # Size of each orb
            for i in range(max_ap):
                # Calculate angle for each orb (same as JS: evenly spaced, starting at top)
                angle = (i / float(max_ap)) * 2 * 3.14159 - 3.14159 / 2
                # Calculate x, y offsets
                x_offset = radius * math.cos(angle)
                y_offset = radius * math.sin(angle)
                # Adjust to center the orb (since images are anchored at top-left)
                x_pos = 64 + x_offset - orb_size / 2  # 64 is half of background width
                y_pos = 64 + y_offset - orb_size / 2
                # Choose active or inactive orb based on available_ap
                orb_image = "orb_active.png" if i < available_ap else "orb_inactive.png"
                # Add the orb at calculated position
                ui.image(orb_image, xpos=int(x_pos), ypos=int(y_pos))

# Define styles for text
style round_label:
    font "arial.ttf"  # Ensure you have Arial or another font in your game folder
    size 36
    color "#ffffff"
    outlines [(2, "#00000080", 2, 2)]  # Text shadow effect
    xalign 0.5

style round_number:
    font "arial.ttf"
    size 90
    color "#ffffff"
    outlines [(2, "#00000080", 2, 2)]
    xalign 0.5
