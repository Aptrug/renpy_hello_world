# Renpy latest version, 1920x1080

screen battle_ui():
    # Boss image (centered top)
    add "images/combat_system/boss.webp" xalign 0.5 yalign 0.0

    # Allies row (bottom), occupy bottom space evenly
    hbox:
        xalign 0.5
        yalign 1.0
        spacing 20

        add "images/combat_system/kanami.webp"
        add "images/combat_system/kenshin.webp"
        add "images/combat_system/magic.webp"
        add "images/combat_system/rance.webp"
        add "images/combat_system/reset.webp"
        add "images/combat_system/sachiko.webp"
        add "images/combat_system/suzume.webp"
