# I'm making a combat system for my renpy game (hero party vs boss)
# I've just started working on it, so it's pretty unimpressive right now
# Portability & efficiency is priority (I want to target mobile users too)

# I want to make the images feel... more alive, like they're real or 3D
# Any ways to do that?
# PS. research what effects card games use to make cards more alive
# Open to all kind of improvements

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
        yalign 0.1
        zoom 0.65

    # Allies row, bottom center
    hbox:
        xalign 0.5
        yalign 0.95
        spacing 20

        add "kanami" at pulse_glow
        add "kenshin" at ally_hover
        add "magic" at gentle_float
        add "rance" at ally_selected_effect
        add "reset" at ally_idle
        add "sachiko" at ally_hover_effect
        add "suzume" at ally_selected_effect

# Bunch of effects, some used, some not
transform idle_float:
    yoffset 0
    linear 2.0 yoffset -5
    linear 2.0 yoffset 0
    repeat

transform pulse_glow:
    alpha 0.5
    linear 1.0 alpha 0.8
    linear 1.0 alpha 0.5
    repeat

transform slow_pulse:
    alpha 0.9
    linear 1.5 alpha 1.0
    linear 1.5 alpha 0.9
    repeat

transform hit_shake:
    linear 0.1 xoffset 10
    linear 0.1 xoffset -10
    linear 0.1 xoffset 0

transform ally_selected_effect:
    matrixcolor BrightnessMatrix(0.3)
    linear 0.8 matrixcolor BrightnessMatrix(0.1)
    linear 0.8 matrixcolor BrightnessMatrix(0.3)
    repeat

transform boss_breathe:
    yoffset 30 zoom 0.7
    linear 3.0 yoffset 25 zoom 0.72
    linear 3.0 yoffset 30 zoom 0.7
    repeat

transform ally_hover_effect:
    zoom 1.08
    matrixcolor BrightnessMatrix(0.2)

transform ally_hover:
    zoom 1.0
    linear 0.25 zoom 1.08

transform gentle_float:
    yoffset 0
    linear 4.0 yoffset -8
    linear 4.0 yoffset 0
    repeat

transform ally_idle:
    linear 0.25 zoom 1.0
