# Round UI for Ren'Py Game - Optimized ATL Implementation
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

# Creator-Defined Displayable for circles with optional radial gradient
init python:
    def lerp_color(c1, c2, t):
        return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))

    class Circle(renpy.Displayable):
        def __init__(self, radius, center_color, edge_color=None, border_color=None, border_width=0, **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.radius = radius
            self.size = radius * 2
            self.center_color = renpy.easy.color(center_color)
            self.edge_color = renpy.easy.color(edge_color) if edge_color else None
            self.border_color = renpy.easy.color(border_color) if border_color else None
            self.border_width = border_width

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)
            canvas = render.canvas()
            center = (self.radius, self.radius)

            if self.edge_color:
                # Radial gradient from center (light) to edge (dark)
                for r in range(self.radius, 0, -1):
                    t = 1 - (r / float(self.radius))  # t=0 at edge, t=1 at center
                    col = lerp_color(self.edge_color, self.center_color, t)
                    canvas.circle(col + (255,), center, r)  # Add alpha 255 for opaque
            else:
                # Solid fill
                canvas.circle(self.center_color + (255,), center, self.radius)

            # Draw border if specified
            if self.border_color and self.border_width > 0:
                canvas.circle(self.border_color + (255,), center, self.radius, self.border_width)

            return render

# Create circular displayables
define round_bg = Circle(125, center_color=(128, 128, 128), edge_color=(80, 80, 80))
define orb_active = Circle(25, center_color=(255, 215, 0), edge_color=(218, 165, 32), border_color=(184, 134, 11), border_width=2)
define orb_inactive_img = Circle(25, center_color=(102, 102, 102), edge_color=(60, 60, 60), border_color=(50, 50, 50), border_width=2)

# Python function for positioning
init python:
    import math

    def get_orb_positions(num_orbs, radius=125, center_x=125, center_y=125, orb_radius=25):
        """Calculate circular positions for orbs around center"""
        positions = []
        for i in range(num_orbs):
            angle = (i / float(num_orbs)) * 2 * math.pi - math.pi / 2
            x = center_x + radius * math.cos(angle) - orb_radius
            y = center_y + radius * math.sin(angle) - orb_radius
            positions.append((int(x), int(y)))
        return positions

# Main UI Screen
screen round_ui():
    # Container positioned at screen center
    fixed:
        xalign 0.5
        yalign 0.5  # Adjusted to true center for better alignment
        xsize 250
        ysize 250

        # Main round circle background with breathing animation
        add round_bg at round_breathe:
            xpos 0
            ypos 0

        # Round number display
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -10  # Tightened spacing for better visual match to HTML

            text "Round":
                size 36
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#00000080", 0, 0)]  # Softer shadow for text

            text "[current_round]":
                size 90
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#00000080", 0, 0)]

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
