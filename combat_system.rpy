screen battle_ui():
    # Boss image (centered top)
    add "images/combat_system/boss.webp" xpos 0.5 ypos 0.1 anchor (0.5, 0.0)

    # Allies row (bottom)
    hbox:
        xpos 0.5
        ypos 0.9
        anchor (0.5, 1.0)
        spacing 20

    add "images/combat_system/kanami.webp"
    add "images/combat_system/kenshin.webp"
    add "images/combat_system/magic.webp"
    add "images/combat_system/rance.webp"
    add "images/combat_system/reset.webp"
    add "images/combat_system/sachiko.webp"
    add "images/combat_system/suzume.webp"
