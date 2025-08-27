# I'm making a combat system for my renpy game (hero party vs boss)
# I've just started working on it, so it's pretty unimpressive right now
# Portability & efficiency is priority (I want to target mobile users too)

# I want to make the images feel... more alive, like they're real
# Any ways to do that?
# PS. research what effects card games use to make cards more alive

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
    add "boss" at idle_float:
        xalign 0.5
        yalign 0.0
        yoffset 30
        zoom 0.7

    # Allies row, bottom center
    hbox:
        xalign 0.5
        yalign 0.8
        spacing 20

        add "kanami" at idle_float
        add "kenshin"
        add "magic"
        add "rance" at slow_pulse
        add "reset"
        add "sachiko"
        add "suzume"

transform idle_float:
    yoffset 0
    linear 2.0 yoffset -5
    linear 2.0 yoffset 0
    repeat

transform slow_pulse:
    alpha 0.9
    linear 1.5 alpha 1.0
    linear 1.5 alpha 0.9
    repeat
