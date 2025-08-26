screen battle_ui():
    # Boss image (centered top)
    add "boss.png" xpos 0.5 ypos 0.1 anchor (0.5, 0.0)

    # Allies row (bottom)
    hbox:
        xpos 0.5
        ypos 0.9
        anchor (0.5, 1.0)
        spacing 20

        add "ally1.png"
        add "ally2.png"
        add "ally3.png"
        add "ally4.png"
        add "ally5.png"
        add "ally6.png"
        add "ally7.png"
