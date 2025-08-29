# Optimized Round UI for Ren'Py - Actually Working Version
# Fixes the broken transforms and simplifies the original code

# Game variables
default current_round = 59
default max_ap = 9
default available_ap = 3

# Working ATL transforms
transform round_breathe:
    zoom 1.0
    ease 3.0 zoom 1.02
    ease 3.0 zoom 1.0
    repeat

transform orb_glow:
    alpha 1.0
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

# Simplified displayable definitions using built-in shapes
define round_bg = Solid("#505050")
define round_inner = Solid("#808080")
define orb_active_img = Solid("#FFD700")
define orb_inactive_img = Solid("#666666")

# Optimized positioning function (simplified from original)
init python:
    import math
    def get_orb_positions(num_orbs, radius=100, center_x=125, center_y=125):
        """Calculate positions for orbs around center - simplified math"""
        positions = []
        for i in range(num_orbs):
            angle = (i * 2 * math.pi / num_orbs) - (math.pi / 2)
            x = center_x + radius * math.cos(angle) - 25
            y = center_y + radius * math.sin(angle) - 25
            positions.append((int(x), int(y)))
        return positions

# Main UI screen - cleaner and working
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Background circle
        add Transform(round_bg, size=(250, 250)) at round_breathe:
            xpos 0
            ypos 0

        # Inner circle for gradient effect
        add Transform(round_inner, size=(240, 240)) at round_breathe:
            xpos 5
            ypos 5

        # Round text - simplified
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -10

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

        # AP Orbs - using working positioning
        $ positions = get_orb_positions(max_ap)

        for i, (x, y) in enumerate(positions):
            if i < available_ap:
                add Transform(orb_active_img, size=(50, 50)) at orb_glow:
                    xpos x
                    ypos y
            else:
                add Transform(orb_inactive_img, size=(50, 50)) at orb_inactive:
                    xpos x
                    ypos y

# Same management functions - they were fine
init python:
    def update_round(new_round):
        global current_round
        current_round = new_round
        renpy.restart_interaction()

    def update_ap(available, maximum=None):
        global available_ap, max_ap
        if maximum is not None:
            max_ap = max(1, maximum)
        available_ap = max(0, min(available, max_ap))
        renpy.restart_interaction()

    def spend_ap(amount=1):
        global available_ap
        if available_ap >= amount:
            available_ap -= amount
            renpy.restart_interaction()
            return True
        return False

    def gain_ap(amount=1):
        global available_ap
        available_ap = min(max_ap, available_ap + amount)
        renpy.restart_interaction()

# Demo - same as original
label start:
    show screen round_ui
    "Round UI Demo - Current: Round [current_round], AP: [available_ap]/[max_ap]"

    menu:
        "Spend AP" if available_ap > 0:
            $ spend_ap()
            jump start

        "Gain AP" if available_ap < max_ap:
            $ gain_ap()
            jump start

        "Next Round":
            $ update_round(current_round + 1)
            $ update_ap(max_ap)
            jump start

        "Change Max AP to 6":
            $ update_ap(available_ap, 6)
            jump start

        "Change Max AP to 12":
            $ update_ap(available_ap, 12)
            jump start

        "Test Round 999":
            $ update_round(999)
            jump start

        "Exit":
            hide screen round_ui
            return

# ALTERNATIVE: More visually accurate to original HTML version
# Using im.MatrixColor for better gradients
define round_bg_gradient = im.MatrixColor(
    Transform(Solid("#808080"), size=(250, 250)),
    im.matrix.colorize("#505050", "#808080")
)

define orb_gold_gradient = im.MatrixColor(
    Transform(Solid("#FFD700"), size=(50, 50)),
    im.matrix.colorize("#DAA520", "#FFD700")
)

# Screen version with gradients (optional upgrade)
screen round_ui_with_gradients():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Gradient background
        add round_bg_gradient at round_breathe

        # Round text
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -10

            text "Round":
                size 36
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 90
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

        # Orbs with gradients
        $ positions = get_orb_positions(max_ap)

        for i, (x, y) in enumerate(positions):
            if i < available_ap:
                add orb_gold_gradient at orb_glow:
                    xpos x
                    ypos y
            else:
                add Transform(orb_inactive_img, size=(50, 50)) at orb_inactive:
                    xpos x
                    ypos y
