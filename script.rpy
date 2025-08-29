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
# Python Helpers
# ========================
init python:
    import math

    def CircleImage(radius, color, border_color=None, border_width=2):
        """Draws a filled circle (with optional border) as a render object."""
        d = renpy.Render(radius*2, radius*2)
        c = d.canvas()
        c.circle(color, (radius, radius), radius)
        if border_color:
            c.circle(border_color, (radius, radius), radius, border_width)
        return d

    def get_orb_positions(num_orbs, orb_radius=ORB_RADIUS, distance=ORB_DISTANCE, center=ROUND_RADIUS):
        """Returns a list of (x, y) positions around a circle."""
        step = 2 * math.pi / num_orbs
        return [
            (
                int(center + distance * math.cos(step*i - math.pi/2) - orb_radius),
                int(center + distance * math.sin(step*i - math.pi/2) - orb_radius)
            )
            for i in range(num_orbs)
        ]

    def orb_state(i):
        """Returns (image, transform) depending on whether orb is active."""
        return (orb_active, orb_glow) if i < available_ap else (orb_inactive_img, orb_inactive)

# ========================
# Circle Definitions
# ========================
define round_bg = CircleImage(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = CircleImage(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = CircleImage(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

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
        add round_bg at round_breathe

        # Round number in the center
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -5

            text "Round":
                size 22
                color "#FFFFFF"
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 56
                color "#FFFFFF"
                outlines [(2, "#000000", 0, 0)]

        # Orbs arranged around the circle
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            $ orb_img, orb_tr = orb_state(i)
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
