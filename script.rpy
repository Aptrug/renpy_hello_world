# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

define ROUND_RADIUS = 70
define ORB_RADIUS = 15

# ========================
# ATL Transforms
# ========================
transform orb_glow:
    parallel:
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
    parallel:
        linear 0.1 additive 0.3
        linear 0.1 additive 0.0
    repeat

transform golden_aura_small:
    alpha 0.6
    parallel:
        ease 2.0 alpha 0.8 zoom 1.05
        ease 2.0 alpha 0.4 zoom 1.0
        repeat
    parallel:
        rotate 0
        linear 15.0 rotate 360
        repeat

transform golden_aura_medium:
    alpha 0.4
    parallel:
        ease 3.0 alpha 0.6 zoom 1.1
        ease 3.0 alpha 0.3 zoom 1.0
        repeat
    parallel:
        rotate 0
        linear 25.0 rotate -360
        repeat

transform golden_aura_large:
    alpha 0.25
    parallel:
        ease 4.0 alpha 0.4 zoom 1.15
        ease 4.0 alpha 0.2 zoom 1.0
        repeat
    parallel:
        rotate 0
        linear 35.0 rotate 360
        repeat

transform orb_inactive:
    alpha 0.4
    zoom 0.9

# ========================
# Python Helpers
# ========================
init python:
    import math

    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super().__init__(**kwargs)
            self.radius, self.color = radius, color
            self.border_color, self.border_width = border_color, border_width

        def render(self, w, h, st, at):
            size = self.radius * 2
            r = renpy.Render(size, size)
            c = r.canvas()

            if self.color:
                c.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                c.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return r

    def get_orb_positions(num_orbs):
        """
        Returns orb positions arranged evenly in a circle around ROUND_RADIUS.
        Offsets by ORB_RADIUS so they align properly.
        """
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = ROUND_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
            y = ROUND_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# Golden aura layers (different sizes for a glowing halo)
define aura_glow_small = Circle(ROUND_RADIUS+15, (255, 223, 100), (255, 215, 0), 2)
define aura_glow_medium = Circle(ROUND_RADIUS+30, (255, 215, 0), (255, 200, 0), 2)
define aura_glow_large = Circle(ROUND_RADIUS+50, (255, 200, 0), (180, 120, 0), 2)

# ========================
# Main UI Screen
# ========================
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.75
        xsize ROUND_RADIUS*2
        ysize ROUND_RADIUS*2

        # Multi-layer golden aura
        add aura_glow_large at golden_aura_large
        add aura_glow_medium at golden_aura_medium
        add aura_glow_small at golden_aura_small

        # Round circle background
        add round_bg

        # Round number in the center
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 2

            text "Round":
                size 22
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 56
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

        # Orbs arranged around the circle
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            add (orb_active if i < available_ap else orb_inactive_img) at (orb_glow if i < available_ap else orb_inactive) xpos x ypos y

# ========================
# Demo Label
# ========================
label start:
    show screen round_ui

    "Round UI Demo: Round [current_round], AP [available_ap]/[max_ap]"

    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start

        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start

        "Exit":
            return
