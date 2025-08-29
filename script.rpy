# Game variables
default current_round = 59
default max_ap = 9
default available_ap = 3

# ATL Transforms for animations
transform orb_glow:
    parallel:
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
        linear 0.1 additive 0.3
        linear 0.1 additive 0.0
        repeat

transform round_breathe:
    ease 3.0 zoom 1.02
    ease 3.0 zoom 1.0
    repeat

# Custom displayable to draw a colored circle with optional border
init python:
    import math

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

            # Draw border if given
            if self.border_color:
                canvas.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)

            return render

    def get_orb_positions(num_orbs, radius=125, center_x=125, center_y=125):
        """Compute (x,y) positions for orbs in a circle."""
        positions = []
        for i in range(num_orbs):
            angle = (i / float(num_orbs)) * 2 * math.pi - math.pi / 2
            x = center_x + radius * math.cos(angle) - 25
            y = center_y + radius * math.sin(angle) - 25
            positions.append((int(x), int(y)))
        return positions

# Define circle graphics
define round_bg = Circle(125, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(25, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(25, (102, 102, 102), (60, 60, 60), 2)

# Main UI screen using fixed layout and loop for orbs
screen round_ui():
    fixed:
        # Center the container
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Main round circle background with breathing animation
        add round_bg at round_breathe:
            xpos 0
            ypos 0

        # Round number display (vertical box centered)
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

        # Compute orb positions and display each orb
        $ orb_positions = get_orb_positions(max_ap)

        for i, (x, y) in enumerate(orb_positions):
            if i < available_ap:
                # Active orb with glow transform
                add orb_active at orb_glow:
                    xpos x
                    ypos y
            else:
                # Inactive orb (duller) using inline alpha/zoom
                add orb_inactive_img:
                    xpos x
                    ypos y
                    alpha 0.4
                    zoom 0.9

# Demo/Test label (optional)
label start:
    show screen round_ui

    "Round UI Demo: Round [current_round], AP [available_ap]/[max_ap]"

    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            $ renpy.restart_interaction()
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            $ renpy.restart_interaction()
            jump start

        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            $ renpy.restart_interaction()
            jump start

        "Exit":
            return
