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

# Creator-defined displayable for drawing circular orbs
init python:
    import math

    class CircularOrb(renpy.Displayable):
        def __init__(self, radius=25, color=(255, 215, 0), border_color=(184, 134, 11), active=True, **kwargs):
            super(CircularOrb, self).__init__(**kwargs)
            self.radius = radius
            self.color = color
            self.border_color = border_color
            self.active = active
            self.size = radius * 2

        def render(self, width, height, st, at):
            # Create a render object
            render = renpy.Render(self.size, self.size)

            # Get the canvas for drawing
            canvas = render.canvas()

            # Draw the main circle
            if self.active:
                canvas.circle(self.color, (self.radius, self.radius), self.radius - 2)
                # Add highlight for 3D effect
                highlight_color = tuple(min(255, c + 50) for c in self.color[:3])
                canvas.circle(highlight_color, (self.radius - 8, self.radius - 8), 8)
            else:
                # Inactive orb - darker color
                inactive_color = (120, 120, 120)
                canvas.circle(inactive_color, (self.radius, self.radius), self.radius - 2)

            # Draw border
            canvas.circle(self.border_color, (self.radius, self.radius), self.radius - 2, 2)

            return render

    def calculate_orb_positions(max_orbs, radius=125, center_x=375, center_y=200):
        """Calculate positions for orbs in a circle around the center"""
        positions = []
        for i in range(max_orbs):
            angle = (i / max_orbs) * 2 * math.pi - math.pi / 2  # Start at top
            x = center_x + radius * math.cos(angle) - 25  # -25 to center the 50px orb
            y = center_y + radius * math.sin(angle) - 25
            positions.append((int(x), int(y)))
        return positions

# Simple image definitions for the round background
image round_bg = Solid("#808080")

# Screen definition for the round UI
screen round_ui():
    # Main container positioned at center of screen
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 750
        ysize 400

        # Background round circle using Transform with proper size and shape
        add Transform(round_bg, size=(250, 250)) at round_circle_transform:
            xpos 250  # Center in the fixed container
            ypos 75

        # Round text display
        vbox:
            xpos 375  # Center the text over the circle
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
                add CircularOrb(active=True) at orb_glow:
                    xpos x
                    ypos y
            else:
                # Inactive orb
                add CircularOrb(active=False) at orb_inactive:
                    xpos x
                    ypos y

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

# Alternative simpler implementation using basic shapes
# If you prefer not to use creator-defined displayables, uncomment this:

# image orb_active = Transform(Solid("#FFD700"), size=(50, 50))
# image orb_inactive = Transform(Solid("#787878"), size=(50, 50))

# screen round_ui_simple():
#     fixed:
#         xalign 0.5
#         yalign 0.4
#         xsize 750
#         ysize 400
#
#         # Background circle
#         add Transform(Solid("#808080"), size=(250, 250)) at round_circle_transform:
#             xpos 250
#             ypos 75
#
#         # Round text
#         vbox:
#             xpos 375
#             ypos 115
#             xanchor 0.5
#             spacing 0
#
#             text "Round" size 36 color "#FFFFFF" text_align 0.5 outlines [(2, "#000000", 0, 0)]
#             text str(current_round) size 90 color "#FFFFFF" text_align 0.5 outlines [(2, "#000000", 0, 0)]
#
#         # Orbs
#         $ orb_positions = calculate_orb_positions(max_ap, radius=125, center_x=375, center_y=200)
#         for i, (x, y) in enumerate(orb_positions):
#             if i < available_ap:
#                 add "orb_active" at orb_glow:
#                     xpos x
#                     ypos y
#             else:
#                 add "orb_inactive" at orb_inactive:
#                     xpos x
#                     ypos y
