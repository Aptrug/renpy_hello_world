# Portability & efficiency is priority (I want to target mobile users too)

# Preload all images
image boss = "images/combat_system/boss.webp"
image kanami = "images/combat_system/kanami.webp"
image kenshin = "images/combat_system/kenshin.webp"
image magic = "images/combat_system/magic.webp"
image rance = "images/combat_system/rance.webp"
image reset = "images/combat_system/reset.webp"
image sachiko = "images/combat_system/sachiko.webp"
image suzume = "images/combat_system/suzume.webp"

screen battle_ui():
    # Feldgrau background
    add Solid("#4D5D53")

    # Boss image, centered top, 70% height, top margin 30px
    add "boss":
        xalign 0.5
        yalign 0.0
        yoffset 30
        zoom 0.7

    # Allies row, bottom center
    hbox:
        xalign 0.5
        yalign 1.0
        spacing 20

        add "kanami"
        add "kenshin"
        add "magic"
        add "rance"
        add "reset"
        add "sachiko"
        add "suzume"
