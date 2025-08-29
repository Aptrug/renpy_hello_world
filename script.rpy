# Round UI for Ren'Py Game - Clean ATL Implementation
# Place this in your game/ folder as a .rpy file

# Game variables
default current_round = 59
default max_ap = 9
default available_ap = 3

# ATL Transform definitions for animations
transform orb_glow:
    alpha 1.0
    zoom 1.0
    parallel:
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
        repeat
    parallel:
        linear 0.1 additive 0.3
        linear 0.1 additive 0.0
        repeat

transform orb_inactive:
    alpha 0.4
    zoom 0.9

transform round_breathe:
    zoom 1.0
    ease 3.0 zoom 1.02
    ease 3.0 zoom 1.0
    repeat

# Circular image definitions using Creator-Defined Displayables
init python:
    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.radius = radius
            self.size = radius * 2
            self.color = color
            self.border_color = border_color
            self.border_width = border_width

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)
            canvas = render.canvas()

            # Draw filled circle
            canvas.circle(self.color, (self.radius, self.radius), self.radius)

            # Draw border if specified
            if self.border_color:
                canvas.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)

            return render

# Create circular images
define round_bg = Circle(125, (80, 80, 80), (50, 50, 50), 3)
define round_inner = Circle(120, (128, 128, 128))
define orb_active = Circle(25, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(25, (102, 102, 102), (60, 60, 60), 2)

# Python functions for positioning
init python:
    import math

    def get_orb_positions(num_orbs, radius=125, center_x=125, center_y=125):
        """Calculate circular positions for orbs around center"""
        positions = []
        for i in range(num_orbs):
            # Start from top (-π/2) and go clockwise
            angle = (i / num_orbs) * 2 * math.pi - math.pi / 2
            x = center_x + radius * math.cos(angle) - 25  # -25 to center 50px orb
            y = center_y + radius * math.sin(angle) - 25
            positions.append((int(x), int(y)))
        return positions

# Main UI Screen
screen round_ui():
    # Container positioned at screen center
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Main round circle background with breathing animation
        add round_bg at round_breathe:
            xpos 0
            ypos 0

        # Inner circle for depth effect
        add round_inner at round_breathe:
            xpos 5
            ypos 5

        # Round number display
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -5

            text "Round":
                size 28
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 72
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

        # AP Orbs positioned in circle
        $ orb_positions = get_orb_positions(max_ap)

        for i, (x, y) in enumerate(orb_positions):
            if i < available_ap:
                # Active orb with glow
                add orb_active at orb_glow:
                    xpos x
                    ypos y
            else:
                # Inactive orb
                add orb_inactive_img at orb_inactive:
                    xpos x
                    ypos y

# Helper functions for AP/Round management
init python:
    def update_round(new_round):
        """Update current round"""
        global current_round
        current_round = new_round
        renpy.restart_interaction()

    def update_ap(available, maximum=None):
        """Update AP values"""
        global available_ap, max_ap
        if maximum is not None:
            max_ap = max(1, maximum)
        available_ap = max(0, min(available, max_ap))
        renpy.restart_interaction()

    def spend_ap(amount=1):
        """Spend AP if available"""
        global available_ap
        if available_ap >= amount:
            available_ap -= amount
            renpy.restart_interaction()
            return True
        return False

    def gain_ap(amount=1):
        """Gain AP up to maximum"""
        global available_ap
        available_ap = min(max_ap, available_ap + amount)
        renpy.restart_interaction()

# Demo/Test label
label start:
    show screen round_ui

    "Round UI Demo - Current: Round [current_round], AP: [available_ap]/[max_ap]"

    menu:
        "What would you like to test?"

        "Spend AP" if available_ap > 0:
            $ spend_ap()
            "Spent 1 AP! Remaining: [available_ap]/[max_ap]"
            jump start

        "Gain AP" if available_ap < max_ap:
            $ gain_ap()
            "Gained 1 AP! Current: [available_ap]/[max_ap]"
            jump start

        "Next Round":
            $ update_round(current_round + 1)
            $ update_ap(max_ap)  # Refresh AP
            "Round [current_round]! AP restored to [available_ap]/[max_ap]"
            jump start

        "Change Max AP to 6":
            $ update_ap(available_ap, 6)
            "Max AP changed to 6. Current: [available_ap]/[max_ap]"
            jump start

        "Change Max AP to 12":
            $ update_ap(available_ap, 12)
            "Max AP changed to 12. Current: [available_ap]/[max_ap]"
            jump start

        "Test Round 999":
            $ update_round(999)
            "Now showing Round 999!"
            jump start

        "Exit":
            hide screen round_ui
            "Demo complete!"
            return

# Alternative: More visual orbs using Composite for better circles
# Uncomment these definitions if you want prettier orbs:

# define orb_gold = Composite(
#     (50, 50),
#     (0, 0), Transform(Solid("#DAA520"), size=(50, 50)),  # Base
#     (5, 5), Transform(Solid("#FFD700"), size=(40, 40)),  # Highlight
#     (10, 10), Transform(Solid("#FFEF94"), size=(30, 30)) # Inner glow
# )

# define orb_inactive_pretty = Composite(
#     (50, 50),
#     (0, 0), Transform(Solid("#444444"), size=(50, 50)),  # Base
#     (5, 5), Transform(Solid("#666666"), size=(40, 40)),  # Highlight
# )
