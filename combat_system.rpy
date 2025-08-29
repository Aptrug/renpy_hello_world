# Define the variables that control the UI
default current_round = 59
default max_ap = 9
default available_ap = 3

# Transform for the glowing effect on active orbs
transform orb_glow:
    alpha 1.0
    zoom 1.0
    parallel:
        ease 0.8 alpha 0.7
        ease 0.8 alpha 1.0
        repeat
    parallel:
        ease 1.2 zoom 1.1
        ease 1.2 zoom 1.0
        repeat

# Transform for inactive orbs
transform orb_inactive:
    alpha 0.6
    zoom 1.0

# Transform for the main round circle (subtle breathing effect)
transform round_circle_transform:
    zoom 1.0
    ease 2.0 zoom 1.02
    ease 2.0 zoom 1.0
    repeat

# Calculate orb positions using Python
init python:
    import math

    def calculate_orb_positions(max_orbs, radius=125, center_x=375, center_y=200):
        """Calculate positions for orbs in a circle around the center"""
        positions = []
        for i in range(max_orbs):
            angle = (i / max_orbs) * 2 * math.pi - math.pi / 2  # Start at top
            x = center_x + radius * math.cos(angle) - 25  # -25 to center the 50px orb
            y = center_y + radius * math.sin(angle) - 25
            positions.append((int(x), int(y)))
        return positions

# Screen definition for the round UI
screen round_ui():
    # Main container positioned at center of screen
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 750
        ysize 400

        # Background round circle
        add Solid("#808080") at round_circle_transform:
            xsize 250
            ysize 250
            xpos 250  # Center in the fixed container
            ypos 75

        # Round text display
        vbox:
            xpos 325  # Center the text over the circle
            ypos 115
            xanchor 0.5
            spacing 0

            text "Round":
                size 36
                color "#FFFFFF"
                text_align 0.5
                outlines [(2, "#000000", 0, 0)]

            text str(current_round):
                size 90
                color "#FFFFFF"
                text_align 0.5
                outlines [(2, "#000000", 0, 0)]

        # Calculate orb positions
        $ orb_positions = calculate_orb_positions(max_ap, radius=125, center_x=375, center_y=200)

        # Display orbs in calculated positions
        for i, (x, y) in enumerate(orb_positions):
            if i < available_ap:
                # Active orb with glow effect
                add "orb_active" at orb_glow:
                    xpos x
                    ypos y
            else:
                # Inactive orb
                add "orb_inactive" at orb_inactive:
                    xpos x
                    ypos y

# Define orb images using LayeredImage for better control
layeredimage orb_active:
    always "orb_base"
    group glow:
        attribute normal default "orb_glow"

layeredimage orb_inactive:
    always "orb_base"

# Create the orb images using Transform and Solid
# You can replace these with actual PNG files if you have them
image orb_base = Transform(Solid("#FFD700"), xsize=50, ysize=50)
image orb_glow = Transform(Solid("#FFD700"), xsize=50, ysize=50)

# Alternative implementation using actual circular shapes (if you prefer)
init python:
    import pygame

    def create_orb_surface(color, size=50, border_color=None, border_width=2):
        """Create a circular orb surface"""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        # Draw the main circle with gradient effect (simplified as solid color)
        pygame.draw.circle(surf, color, (center, center), center - border_width)

        # Draw border if specified
        if border_color:
            pygame.draw.circle(surf, border_color, (center, center), center - border_width, border_width)

        # Add highlight for 3D effect
        highlight_color = tuple(min(255, c + 50) for c in color[:3]) + (color[3] if len(color) > 3 else (255,))
        pygame.draw.circle(surf, highlight_color, (center - 8, center - 8), 8)

        return surf

# Create orb images using pygame surfaces (more authentic look)
image orb_active_surface = Transform(
    im.Data(
        pygame.image.tostring(
            create_orb_surface((255, 215, 0, 255), border_color=(184, 134, 11, 255)),
            "RGBA"
        ),
        (50, 50)
    )
)

image orb_inactive_surface = Transform(
    im.Data(
        pygame.image.tostring(
            create_orb_surface((120, 120, 120, 255), border_color=(80, 80, 80, 255)),
            "RGBA"
        ),
        (50, 50)
    )
)

# Functions to update the UI state
init python:
    def update_round(new_round):
        global current_round
        current_round = new_round
        renpy.restart_interaction()

    def update_ap(new_available, new_max=None):
        global available_ap, max_ap
        available_ap = new_available
        if new_max is not None:
            max_ap = new_max
        renpy.restart_interaction()

    def gain_ap(amount=1):
        global available_ap
        available_ap = min(max_ap, available_ap + amount)
        renpy.restart_interaction()

    def spend_ap(amount=1):
        global available_ap
        available_ap = max(0, available_ap - amount)
        renpy.restart_interaction()
