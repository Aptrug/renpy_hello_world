# ==============================================================================
# ROUND UI SYSTEM - RENPY IMPLEMENTATION
# ==============================================================================
# This file should be placed in your game/ folder as a .rpy file
# Make sure these variable names don't conflict with existing ones in your project

# Variable declarations - use define for constants, default for changing values
# These MUST be declared only once across your entire project
define MAX_AP_DEFAULT = 9
default current_round = 59
default max_ap = MAX_AP_DEFAULT
default available_ap = 3

# ==============================================================================
# ATL TRANSFORM DEFINITIONS
# ==============================================================================

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

# ==============================================================================
# CREATOR-DEFINED DISPLAYABLE FOR CIRCULAR ORBS
# ==============================================================================

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

# ==============================================================================
# SIMPLE IMAGE DEFINITIONS
# ==============================================================================

# Background for the round display - using a simple solid color
define round_bg_color = Solid("#505050")

# ==============================================================================
# SCREEN DEFINITION
# ==============================================================================

screen round_ui():
    # Main container positioned at center of screen
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 750
        ysize 400

        # Background round circle with gradient-like effect using multiple circles
        add Transform(round_bg_color, size=(250, 250)) at round_circle_transform:
            xpos 250
            ypos 75

        # Inner circle for depth
        add Transform(Solid("#808080"), size=(240, 240)) at round_circle_transform:
            xpos 255
            ypos 80

        # Round text display
        vbox:
            xpos 375
            ypos 115
            xanchor 0.5
            spacing -10

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

        # Calculate orb positions based on current max_ap
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

# ==============================================================================
# UI MANAGEMENT FUNCTIONS
# ==============================================================================

init python:
    def update_round(new_round):
        """Update the current round number"""
        global current_round
        current_round = new_round
        renpy.restart_interaction()

    def update_ap(new_available, new_max=None):
        """Update AP values. If new_max is provided, also update max AP"""
        global available_ap, max_ap
        available_ap = max(0, new_available)
        if new_max is not None:
            max_ap = max(1, new_max)
            available_ap = min(available_ap, max_ap)
        renpy.restart_interaction()

    def gain_ap(amount=1):
        """Increase available AP by the specified amount"""
        global available_ap
        available_ap = min(max_ap, available_ap + amount)
        renpy.restart_interaction()

    def spend_ap(amount=1):
        """Decrease available AP by the specified amount"""
        global available_ap
        if available_ap >= amount:
            available_ap = max(0, available_ap - amount)
            renpy.restart_interaction()
            return True
        return False

    def refresh_ap():
        """Restore AP to maximum (typically used at start of new round)"""
        global available_ap
        available_ap = max_ap
        renpy.restart_interaction()

# ==============================================================================
# DEMONSTRATION LABEL
# ==============================================================================

label start:
    # Show the round UI screen
    show screen round_ui

    "Welcome to the Round UI demo!"
    "Current status: Round [current_round], AP: [available_ap]/[max_ap]"

    menu demo_loop:
        "What would you like to do?"

        "Spend 1 AP" if available_ap > 0:
            $ success = spend_ap(1)
            if success:
                "AP spent! You now have [available_ap]/[max_ap] AP remaining."
            jump demo_loop

        "Spend 1 AP" if available_ap == 0:
            "You don't have any AP to spend!"
            jump demo_loop

        "Gain 1 AP" if available_ap < max_ap:
            $ gain_ap(1)
            "AP gained! You now have [available_ap]/[max_ap] AP."
            jump demo_loop

        "Gain 1 AP" if available_ap >= max_ap:
            "Your AP is already at maximum!"
            jump demo_loop

        "Next Round":
            $ update_round(current_round + 1)
            $ refresh_ap()
            "Welcome to round [current_round]! AP refreshed to [available_ap]/[max_ap]."
            jump demo_loop

        "Change AP Settings":
            menu ap_settings:
                "What AP setting would you like to change?"

                "Set Max AP to 6":
                    $ update_ap(available_ap, 6)
                    "Max AP changed to 6. Current AP: [available_ap]/[max_ap]"
                    jump demo_loop

                "Set Max AP to 12":
                    $ update_ap(available_ap, 12)
                    "Max AP changed to 12. Current AP: [available_ap]/[max_ap]"
                    jump demo_loop

                "Reset to Default (9)":
                    $ update_ap(available_ap, MAX_AP_DEFAULT)
                    "Reset to default settings. AP: [available_ap]/[max_ap]"
                    jump demo_loop

                "Back":
                    jump demo_loop

        "Test Different Rounds":
            menu round_settings:
                "Which round would you like to test?"

                "Round 1":
                    $ update_round(1)
                    jump demo_loop

                "Round 99":
                    $ update_round(99)
                    jump demo_loop

                "Round 999":
                    $ update_round(999)
                    jump demo_loop

                "Back":
                    jump demo_loop

        "Hide UI":
            hide screen round_ui
            "UI hidden. You can show it again from the next menu."

            menu:
                "Show UI again":
                    show screen round_ui
                    "UI is back!"
                    jump demo_loop

        "Exit Demo":
            hide screen round_ui
            "Thanks for trying the Round UI demo!"
            return

# ==============================================================================
# ALTERNATIVE SIMPLE IMPLEMENTATION
# ==============================================================================
# Uncomment the following if you prefer a simpler approach without creator-defined displayables

# define orb_active_img = Transform(Solid("#FFD700"), size=(50, 50))
# define orb_inactive_img = Transform(Solid("#787878"), size=(50, 50))

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
#             spacing -10
#
#             text "Round" size 36 color "#FFFFFF" text_align 0.5 outlines [(2, "#000000", 0, 0)]
#             text str(current_round) size 90 color "#FFFFFF" text_align 0.5 outlines [(2, "#000000", 0, 0)]
#
#         # Orbs
#         $ orb_positions = calculate_orb_positions(max_ap, radius=125, center_x=375, center_y=200)
#         for i, (x, y) in enumerate(orb_positions):
#             if i < available_ap:
#                 add orb_active_img at orb_glow:
#                     xpos x
#                     ypos y
#             else:
#                 add orb_inactive_img at orb_inactive:
#                     xpos x
#                     ypos y
