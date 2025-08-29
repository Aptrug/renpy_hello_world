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

transform orb_inactive:
    alpha 0.4
    zoom 0.9

# Python helper for orb positions
init python:
    import math

    def get_orb_positions(num_orbs, radius=125, center_x=125, center_y=125):
        positions = []
        for i in range(num_orbs):
            angle = (i / float(num_orbs)) * 2 * math.pi - math.pi / 2
            x = center_x + radius * math.cos(angle) - 25
            y = center_y + radius * math.sin(angle) - 25
            positions.append((int(x), int(y)))
        return positions

# Circle graphics using Solid + Composite (no Python drawing)
define round_bg = Composite(
    (250, 250),
    (0, 0), Solid("#505050"),
    (3, 3), Solid("#808080", xysize=(244, 244))
)

define orb_active = Composite(
    (50, 50),
    (0, 0), Solid("#DAA520"),
    (5, 5), Solid("#FFD700", xysize=(40, 40))
)

define orb_inactive_img = Composite(
    (50, 50),
    (0, 0), Solid("#3C3C3C"),
    (5, 5), Solid("#666666", xysize=(40, 40))
)

# Main UI screen
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Breathing round background
        add round_bg at round_breathe:
            xpos 0
            ypos 0

        # Round number in the center
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

        # Orbs arranged in a circle
        $ orb_positions = get_orb_positions(max_ap)
        for i, (x, y) in enumerate(orb_positions):
            if i < available_ap:
                add orb_active at orb_glow:
                    xpos x
                    ypos y
            else:
                add orb_inactive_img at orb_inactive:
                    xpos x
                    ypos y

# Demo/Test label
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
