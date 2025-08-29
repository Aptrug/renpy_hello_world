# This code works, but the question is, can the logic be simplified though?

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

define ROUND_RADIUS = 70
define ORB_RADIUS = 15
define ORB_DISTANCE = ROUND_RADIUS  # distance from center to orb center

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

transform round_breathe:
    ease 3.0 zoom 1.02
    ease 3.0 zoom 1.0
    repeat

transform orb_inactive:
    alpha 0.4
    zoom 0.9

# ========================
# Python: Circle + Orb Positions
# ========================
init python:
    import math

    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super().__init__(**kwargs)
            self.radius = radius
            self.color = color
            self.border_color = border_color
            self.border_width = border_width

        def render(self, width, height, st, at):
            render = renpy.Render(self.radius*2, self.radius*2)
            canvas = render.canvas()
            canvas.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                canvas.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return render

    def get_orb_positions(num_orbs, orb_radius=ORB_RADIUS, distance=ORB_DISTANCE, center=ROUND_RADIUS):
        return [
            (
                int(center + distance * math.cos(2*math.pi*i/num_orbs - math.pi/2) - orb_radius),
                int(center + distance * math.sin(2*math.pi*i/num_orbs - math.pi/2) - orb_radius)
            )
            for i in range(num_orbs)
        ]

    def get_orb_display(i, available_ap):
        return (orb_active, orb_glow) if i < available_ap else (orb_inactive_img, orb_inactive)

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# ========================
# Main UI Screen
# ========================
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.75
        xsize ROUND_RADIUS*2
        ysize ROUND_RADIUS*2

        # Round circle background with breathing animation
        add round_bg at round_breathe xpos 0 ypos 0

        # Round number in the center
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -5

            text "Round":
                size 22
                color "#FFFFFF"
                xalign 0.45
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 56
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

        # Orbs arranged around the circle
        $ orb_positions = get_orb_positions(max_ap)
        for i, (x, y) in enumerate(orb_positions):
            $ orb_img, orb_tr = get_orb_display(i, available_ap)
            add orb_img at orb_tr xpos x ypos y

# ========================
# Demo Label
# ========================
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
