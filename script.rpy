# Optimized Round UI for Ren'Py - Simplified ATL Implementation

# Game variables
default current_round = 59
default max_ap = 9
default available_ap = 3

# Optimized ATL transforms
transform round_breathe:
    zoom 1.0
    ease 3.0 zoom 1.02
    ease 3.0 zoom 1.0
    repeat

transform orb_glow:
    alpha 1.0
    additive 0.0
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

# Optimized orb positioning transform that takes angle as parameter
transform orb_position(angle_deg):
    # Convert to Ren'Py's coordinate system and place orb
    anchor (0.5, 0.5)
    pos (125, 125)  # Center of the 250x250 container
    angle angle_deg
    radius 125

# Simple circle creation using Solid with Transform
define round_bg = Transform(Solid("#505050"), size=(250, 250), corner1=(125, 125))
define round_inner = Transform(Solid("#808080"), size=(240, 240), corner1=(120, 120))
define orb_active_img = Transform(Solid("#FFD700"), size=(50, 50), corner1=(25, 25))
define orb_inactive_img = Transform(Solid("#666666"), size=(50, 50), corner1=(25, 25))

# Utility function for angle calculation
init python:
    def get_orb_angle(index, total):
        """Calculate angle for orb positioning (starting from top)"""
        return (index * 360.0 / total - 90) % 360

# Main optimized UI screen
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Background circles with shared breathe animation
        add round_bg at round_breathe
        add round_inner at round_breathe

        # Round number text
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

        # Optimized AP orbs using polar positioning
        for i in range(max_ap):
            $ angle = get_orb_angle(i, max_ap)

            if i < available_ap:
                add orb_active_img at Transform(orb_position(angle), orb_glow):
                    anchor (0.5, 0.5)
            else:
                add orb_inactive_img at Transform(orb_position(angle), orb_inactive):
                    anchor (0.5, 0.5)

# Simplified management functions
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

# Demo label
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

# Alternative: Even more optimized version using composite circles
# This version eliminates individual transforms for better performance

screen round_ui_ultra_optimized():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        # Single composite background
        add Composite(
            (250, 250),
            (0, 0), Transform(Solid("#505050"), size=(250, 250), corner1=(125, 125)),
            (5, 5), Transform(Solid("#808080"), size=(240, 240), corner1=(120, 120))
        ) at round_breathe

        # Text overlay
        text "Round\n[current_round]":
            xalign 0.5
            yalign 0.5
            size 28
            color "#FFFFFF"
            text_align 0.5
            outlines [(2, "#000000", 0, 0)]
            line_spacing -20

        # Single composite for all orbs (most optimized approach)
        python:
            import math
            orb_composite_list = [(250, 250)]  # Size tuple

            for i in range(max_ap):
                angle_rad = (i / max_ap) * 2 * math.pi - math.pi / 2
                x = int(125 + 125 * math.cos(angle_rad) - 25)
                y = int(125 + 125 * math.sin(angle_rad) - 25)

                if i < available_ap:
                    orb_img = Transform(Solid("#FFD700"), size=(50, 50), corner1=(25, 25))
                    orb_composite_list.extend([(x, y), orb_img])
                else:
                    orb_img = Transform(Solid("#666666"), size=(50, 50), corner1=(25, 25))
                    orb_composite_list.extend([(x, y), orb_img])

        add Composite(*orb_composite_list) at orb_glow
