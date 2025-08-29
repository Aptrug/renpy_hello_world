# Round UI for Ren'Py Game - MINIMAL fix to original working code
# Only removes Creator-Defined Displayables, everything else unchanged

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

# Simple displayables instead of Creator-Defined ones
define round_bg = Transform(Solid("#505050"), size=(250, 250))
define round_inner = Transform(Solid("#808080"), size=(240, 240))
define orb_active = Transform(Solid("#FFD700"), size=(50, 50))
define orb_inactive_img = Transform(Solid("#666666"), size=(50, 50))

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
