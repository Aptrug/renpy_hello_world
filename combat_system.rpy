# Renpy latest version, 1920x1080

screen battle_ui():
    # Full black background
    add Solid("#000")  # solid black fills everything

    # Boss image (top 70% of screen)
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

# Transform to resize boss to ~70% of screen height with margin
transform boss_resize:
    xpos 0.5
    yalign 0.0
    xanchor 0.5
    yanchor 0.0
    zoom 0.7  # roughly 70% of screen height
