# Define variables for the UI state
default current_round = 59
default max_ap = 9
default available_ap = 3

# Define the screen for the round and AP indicator
screen round_ap_indicator():
    # Main container
    fixed:
        # Background circle - using your round_bg.png or fallback styling
        if renpy.loadable("round_bg.png"):
            add "round_bg.png" xalign 0.5 yalign 0.5
        else:
            # Fallback: create a circular background using Frame
            frame:
                background "#505050"
                xsize 250
                ysize 250
                xalign 0.5
                yalign 0.5

        # Round text in the center
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 0

            text "Round":
                size 36
                color "#FFFFFF"
                text_align 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 90
                color "#FFFFFF"
                text_align 0.5
                outlines [(2, "#000000", 0, 0)]

        # Orbs positioned in a circle
        for i in range(max_ap):
            $ angle = (i / max_ap) * 2 * 3.14159 - 3.14159 / 2
            $ x_pos = 125 + 125 * renpy.math.cos(angle) - 16  # 16 = half of 32px orb
            $ y_pos = 125 + 125 * renpy.math.sin(angle) - 16

            if i < available_ap:
                add "orb_active.png" xpos int(x_pos) ypos int(y_pos)
            else:
                add "orb_inactive.png" xpos int(x_pos) ypos int(y_pos)
