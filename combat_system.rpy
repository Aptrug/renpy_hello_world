# Unified Combat System for RenPy - Mobile & Desktop Compatible
# Optimized effects that work smoothly on all devices

# Preload all images
image boss = "images/combat_system/boss.webp"
image kanami = "images/combat_system/kanami.webp"
image kenshin = "images/combat_system/kenshin.webp"
image magic = "images/combat_system/magic.webp"
image rance = "images/combat_system/rance.webp"
image reset = "images/combat_system/reset.webp"
image sachiko = "images/combat_system/sachiko.webp"
image suzume = "images/combat_system/suzume.webp"

# Unified transforms - lightweight but effective
transform boss_breathe:
    yoffset 30 zoom 0.7
    linear 3.0 yoffset 25 zoom 0.72
    linear 3.0 yoffset 30 zoom 0.7
    repeat

transform ally_hover:
    zoom 1.0 matrixcolor BrightnessMatrix(0.0)
    linear 0.25 zoom 1.08 matrixcolor BrightnessMatrix(0.2)

transform ally_idle:
    linear 0.25 zoom 1.0 matrixcolor BrightnessMatrix(0.0)

transform selected_glow:
    matrixcolor BrightnessMatrix(0.3) * TintMatrix("#88DDFF")
    linear 0.8 matrixcolor BrightnessMatrix(0.1) * TintMatrix("#88DDFF")
    linear 0.8 matrixcolor BrightnessMatrix(0.3) * TintMatrix("#88DDFF")
    repeat

transform gentle_float:
    yoffset 0
    linear 4.0 yoffset -8
    linear 4.0 yoffset 0
    repeat

# Game state variables
default selected_ally = None
default boss_health = 100

# Main unified battle screen
screen battle_ui():
    # Multi-layer background for depth without heavy effects
    add Solid("#3A4A40")
    add Solid("#4D5D53") alpha 0.85

    # Subtle depth shadows (lightweight)
    add Solid("#000000") alpha 0.15:
        xsize config.screen_width
        ysize 120
        yalign 0.0
        blur 8

    add Solid("#000000") alpha 0.1:
        xsize config.screen_width
        ysize 80
        yalign 1.0
        blur 8

    # Boss area with health indicator
    vbox:
        xalign 0.5
        yalign 0.05
        spacing 15

        # Health bar
        frame:
            background Solid("#000000") alpha 0.6
            padding (15, 8)
            xalign 0.5

            vbox:
                spacing 5
                text "Boss Health" size 18 color "#FFFFFF" xalign 0.5
                bar:
                    value boss_health
                    range 100
                    xsize 250
                    ysize 15
                    left_bar Solid("#FF6B6B")
                    right_bar Solid("#333333")

        # Boss with shadow and breathing
        frame:
            background None
            padding (0, 0)
            xalign 0.5

            # Simple shadow
            add Solid("#000000") alpha 0.25:
                xalign 0.5
                yalign 1.0
                yoffset 8
                zoom 0.7
                blur 12

            add "boss":
                xalign 0.5
                yalign 0.0
                at boss_breathe
                # Visual feedback based on health
                if boss_health <= 30:
                    matrixcolor TintMatrix("#FF9999")
                elif boss_health <= 60:
                    matrixcolor TintMatrix("#FFCC99")

    # Battle field surface illusion
    add Solid("#2A3A30") alpha 0.2:
        xalign 0.5
        yalign 0.72
        xsize config.screen_width - 40
        ysize 180
        blur 2

    # Allies section with touch-friendly spacing
    vbox:
        xalign 0.5
        yalign 0.82
        spacing 10

        # Optional ally info display
        if selected_ally is not None:
            frame:
                background Solid("#000000") alpha 0.7
                padding (15, 8)
                xalign 0.5

                text "Selected: [selected_ally_names[selected_ally]]" size 16 color "#FFFFFF" xalign 0.5

        # Main ally selection row
        hbox:
            xalign 0.5
            spacing 18  # Touch-friendly spacing

            for i, ally_name in enumerate(["kanami", "kenshin", "magic", "rance", "reset", "sachiko", "suzume"]):
                frame:
                    background None
                    padding (0, 0)

                    # Subtle shadow for each ally
                    add Solid("#000000") alpha 0.2:
                        xalign 0.5
                        yalign 1.0
                        yoffset 5
                        size (60, 12)
                        blur 8

                    imagebutton:
                        idle ally_name
                        hover ally_name

                        # Floating animation
                        at gentle_float

                        # Selection highlighting
                        if selected_ally == i:
                            at selected_glow

                        hover_transform ally_hover
                        unhover_transform ally_idle

                        action [
                                SetVariable("selected_ally", i),
                                # Add your battle action here
                                ]

                        # Touch/click feedback
                        hover_sound "audio/ui_hover.ogg" # Optional
                        activate_sound "audio/ui_select.ogg" # Optional

# Ally names for UI display
define selected_ally_names = ["Kanami", "Kenshin", "Magic", "Rance", "Reset", "Sachiko", "Suzume"]

# Battle actions - example implementation
screen battle_actions():
    if selected_ally is not None:
        frame:
            xalign 0.5
            yalign 0.95
            background Solid("#000000") alpha 0.8
            padding (20, 10)

            hbox:
                spacing 15
                textbutton "Attack" action Call("battle_attack")
                textbutton "Defend" action Call("battle_defend")
                textbutton "Special" action Call("battle_special")
                textbutton "Cancel" action SetVariable("selected_ally", None)

# Main battle screen combining UI and actions
screen battle_main():
    use battle_ui
    use battle_actions

# Damage feedback transform for hit reactions
transform damage_flash:
    matrixcolor TintMatrix("#FF4444")
    linear 0.15 matrixcolor TintMatrix("#FFFFFF")
    linear 0.15 matrixcolor TintMatrix("#FF4444")
    linear 0.15 matrixcolor IdentityMatrix()

# Victory/defeat animations
transform victory_bounce:
    yoffset 0
    linear 0.3 yoffset -20
    linear 0.3 yoffset 0
    linear 0.2 yoffset -10
    linear 0.2 yoffset 0

# Example battle logic labels
label battle_attack:
    $ damage = renpy.random.randint(15, 25)
    $ boss_health = max(0, boss_health - damage)

    "You deal [damage] damage!"

    # Visual feedback
    show boss at damage_flash

    if boss_health <= 0:
        jump battle_victory
    else:
        jump battle_enemy_turn

label battle_defend:
    "You take a defensive stance!"
    jump battle_enemy_turn

label battle_special:
    $ sp_damage = renpy.random.randint(25, 40)
    $ boss_health = max(0, boss_health - sp_damage)

    "Special attack for [sp_damage] damage!"

    show boss at damage_flash

    if boss_health <= 0:
        jump battle_victory
    else:
        jump battle_enemy_turn

label battle_enemy_turn:
    "Boss attacks!"
    # Add your enemy logic here
    jump battle_player_turn

label battle_player_turn:
    $ selected_ally = None  # Reset selection
    call screen battle_main

label battle_victory:
    show boss at victory_bounce
    "Victory! The boss has been defeated!"
    return

# Example usage in your main script
label start_battle:
    scene black
    "The battle begins!"

    $ boss_health = 100
    $ selected_ally = None

    jump battle_player_turn
