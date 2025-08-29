default round_number = 5
default maxAP = 9
default availableAP = 3

transform orb(angle=0):
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    angle angle
    radius 125

transform glow:
    parallel:
        linear 1.0 alpha 0.5
        linear 1.0 alpha 1.0
        repeat

label start:
    show screen battle_ui
    pause

screen battle_ui:
    frame:
        xysize (250, 250)
        background Solid("#505050")
        align (0.5, 0.5)

    text "Round":
        xalign 0.5
        yalign 0.45
        size 36 color "#FFFFFF"

    text str(round_number):
        xalign 0.5
        yalign 0.55
        size 90 color "#FFFFFF"

    for i in range(maxAP):
        $ deg = 360.0 * i / maxAP - 90.0
        if i < availableAP:
            add Solid("#FFD700", xysize=(50,50)) at (orb(angle=deg), glow)
        else:
            add Solid("#DAA520", xysize=(50,50)) at orb(angle=deg)
