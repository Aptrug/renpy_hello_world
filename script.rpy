# This code works, but instead of round_breathe I want the round to emit Golden aura around it instead

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

define ROUND_RADIUS = 70
define ORB_RADIUS = 15
define AURA_PADDING = 50
define AURA_BLUR = 20
define AURA_BORDER_WIDTH = 7

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

transform aura_glow:
    ease 3.0 zoom 1.05 alpha 0.4
    ease 3.0 zoom 1.0 alpha 0.6
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
        def __init__(self, radius, color, border_color=None, border_width=2, padding=0, **kwargs):
            super().__init__(**kwargs)
            self.radius, self.color = radius, color
            self.border_color, self.border_width = border_color, border_width
            self.padding = padding

        def render(self, w, h, st, at):
            size = 2 * (self.radius + self.padding)
            r = renpy.Render(size, size)
            c = r.canvas()

            center = self.radius + self.padding
            if self.color:
                c.circle(self.color, (center, center), self.radius)
            if self.border_color:
                c.circle(self.border_color, (center, center), self.radius, self.border_width)
            return r

    def get_orb_positions(num_orbs, center_x, center_y, orbit_radius):
        """
        Returns orb top-left positions arranged evenly in a circle around the center.
        """
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            orb_center_x = center_x + orbit_radius * math.cos(angle)
            orb_center_y = center_y + orbit_radius * math.sin(angle)
            x = orb_center_x - ORB_RADIUS
            y = orb_center_y - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define glow_source = Circle(ROUND_RADIUS, None, "#ffffff", AURA_BORDER_WIDTH, padding=AURA_PADDING)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# ========================
# Main UI Screen
# ========================
screen round_ui():
    add Solid("#000000")  # Gray color in hex
    fixed:
        xalign 0.5
        yalign 0.75
        xsize 2 * (ROUND_RADIUS + AURA_PADDING)
        ysize 2 * (ROUND_RADIUS + AURA_PADDING)

        # Golden aura
        add glow_source:
            align (0.5, 0.5)
            matrixcolor TintMatrix("#ffd700")
            blur AURA_BLUR
            additive 1.0
            at aura_glow

        # Round circle background (static)
        add round_bg align (0.5, 0.5)

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
        $ center = ROUND_RADIUS + AURA_PADDING
        for i, (x, y) in enumerate(get_orb_positions(max_ap, center, center, ROUND_RADIUS)):
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
