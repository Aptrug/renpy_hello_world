init python:
    # Example variables (could be updated during gameplay)
    default round_number = 5
    default maxAP = 9
    default availableAP = 3

# Define an ATL transform that places a child at a given angle around center.
transform orb(angle=0):
    anchor (0.5, 0.5)       # center of orb image is pivot
    pos (0.5, 0.5)          # start at screen center
    angle angle            # polar angle in degrees (0 = up)
    radius 125             # distance (pixels) from center

# A “glow” transform to animate active orbs (optional).
transform glow:
    parallel:
        linear 1.0 alpha 0.5
        linear 1.0 alpha 1.0
        repeat

label start:
    # Show the battle UI and pause to view.
    show screen battle_ui
    pause

screen battle_ui:
    # Background circle (using frame or an image of a circle).
    frame:
        xysize (250, 250)
        background Solid("#505050")
        background Frame("gui/frame.png", 0, 0)  # example frame (replace with your style)
        align (0.5, 0.5)

    # Centered text: "Round" and the round number.
    text "Round" at truecenter:
        xalign 0.5
        yalign 0.45
        size 36 color "#FFFFFF"
    text str(round_number) at truecenter:
        xalign 0.5
        yalign 0.55
        size 90 color "#FFFFFF"

    # Loop to create orbs around the circle.
    for i in range(maxAP):
        # Compute angle: start at -90° so i=0 is top (0 deg = up by default).
        $ deg = 360.0 * i / maxAP - 90.0
        # Choose image and transform based on active/inactive.
        if i < availableAP:
            # Active orb: use glow animation and/or a highlighted image.
            add Solid("#FFD700", xysize=(50,50)) at orb(angle=deg) xalign 0.5 yalign 0.5 rotate 0:
                zoom 1.0
                at glow  # apply glowing animation
        else:
            # Inactive orb: use plain orb image (no glow).
            add Solid("#DAA520", xysize=(50,50)) at orb(angle=deg) xalign 0.5 yalign 0.5 rotate 0
