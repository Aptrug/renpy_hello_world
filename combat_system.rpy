# Portability & efficiency is priority (I want to target mobile users too)

init python:
    renpy.image("boss", "images/combat_system/boss.webp")
    renpy.image("allies_row", "images/combat_system/allies_row.webp")

screen battle_ui():
    # Full feldgrau background
    add Solid("#4D5D53")

    # Boss image (top 70% of screen with top margin)
    add "images/combat_system/boss.webp":
        xalign 0.5
        yalign 0.0
        yoffset 30
        zoom 0.7

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
