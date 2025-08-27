screen battle_ui():
    # Full black background
    add Solid("#000")

    # Boss image (top 70% of screen with top margin)
    add "images/combat_system/boss.webp" at boss_resize

    # Allies row (bottom center)
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

# Simplified transform for boss
transform boss_resize:
    xalign 0.5
    yalign 0.0
    yoffset 30   # top margin
    zoom 0.7     # 70% height
