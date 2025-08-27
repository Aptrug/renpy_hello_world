# Unified Combat System for RenPy - Proper Syntax
# Uses correct RenPy alpha/transparency methods

# Preload all images
image boss = "images/combat_system/boss.webp"
image kanami = "images/combat_system/kanami.webp"
image kenshin = "images/combat_system/kenshin.webp"
image magic = "images/combat_system/magic.webp"
image rance = "images/combat_system/rance.webp"
image reset = "images/combat_system/reset.webp"
image sachiko = "images/combat_system/sachiko.webp"
image suzume = "images/combat_system/suzume.webp"

# Unified transforms
transform boss_breathe:
    yoffset 30 zoom 0.7
    linear 3.0 yoffset 25 zoom 0.72
    linear 3.0 yoffset 30 zoom 0.7
    repeat

transform ally_hover:
    zoom 1.0
    linear 0.25 zoom 1.08

transform ally_idle:
    linear 0.25 zoom 1.0

transform selected_glow:
    matrixcolor BrightnessMatrix(0.3)
    linear 0.8 matrixcolor BrightnessMatrix(0.1)
    linear 0.8 matrixcolor BrightnessMatrix(0.3)
    repeat

transform gentle_float:
    yoffset 0
    linear 4.0 yoffset -8
    linear 4.0 yoffset 0
    repeat

transform damage_flash:
    matrixcolor TintMatrix("#FF4444")
    linear 0.15 matrixcolor TintMatrix("#FFFFFF")
    linear 0.15 matrixcolor TintMatrix("#FF4444")
    linear 0.15 matrixcolor IdentityMatrix()

# Game state variables
default selected_ally = None
default boss_health = 100

# Main unified battle screen
screen battle_ui():
    # Background layers for depth
    add Solid("#4D5D53")

    # Semi-transparent overlays using alpha in add statements
    add Solid("#000000"):
        alpha 0.15
        ysize 120
        yalign 0.0

    add Solid("#000000"):
        alpha 0.1
        ysize 80
        yalign 1.0

    # Boss area with health indicator
    vbox:
        xalign 0.5
        yalign 0.05
        spacing 15

        # Health bar frame - using hexadecimal alpha
        frame:
            background Solid("#00000099")  # 60% opacity black
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

        # Boss with shadow
        add Solid("#000000"):
            alpha 0.25
            xalign 0.5
            yalign 1.0
            yoffset 38
            zoom 0.7

        if boss_health <= 30:
            add "boss":
                at boss_breathe
                matrixcolor TintMatrix("#FF9999")
        elif boss_health <= 60:
            add "boss":
                at boss_breathe
                matrixcolor TintMatrix("#FFCC99")
        else:
            add "boss":
                at boss_breathe

    # Battle field surface
    add Solid("#2A3A30"):
        alpha 0.2
        xalign 0.5
        yalign 0.72
        xsize config.screen_width - 40
        ysize 180

    # Selected ally info
    if selected_ally is not None:
        frame:
            background Solid("#000000B3")  # 70% opacity black
            padding (15, 8)
            xalign 0.5
            yalign 0.75

            text "Selected: [selected_ally_names[selected_ally]]" size 16 color "#FFFFFF" xalign 0.5

    # Allies section
    hbox:
        xalign 0.5
        yalign 0.82
        spacing 18

        for i, ally_name in enumerate(["kanami", "kenshin", "magic", "rance", "reset", "sachiko", "suzume"]):
            vbox:
                spacing -5

                # Shadow for each ally
                add Solid("#000000"):
                    alpha 0.2
                    xalign 0.5
                    size (60, 12)

                imagebutton:
                    idle ally_name
                    hover ally_name
                    at gentle_float

                    if selected_ally == i:
                        at selected_glow

                    hover_transform ally_hover
                    unhover_transform ally_idle

                    action SetVariable("selected_ally", i)

# Battle actions screen
screen battle_actions():
    if selected_ally is not None:
        frame:
            xalign 0.5
            yalign 0.95
            background Solid("#000000CC")  # 80% opacity black
            padding (20, 10)

            hbox:
                spacing 15
                textbutton "Attack":
                    action [
                        SetVariable("boss_health", max(0, boss_health - renpy.random.randint(15, 25))),
                        SetVariable("selected_ally", None)
                    ]
                textbutton "Defend":
                    action SetVariable("selected_ally", None)
                textbutton "Special":
                    action [
                        SetVariable("boss_health", max(0, boss_health - renpy.random.randint(25, 40))),
                        SetVariable("selected_ally", None)
                    ]
                textbutton "Cancel":
                    action SetVariable("selected_ally", None)

# Main battle screen
screen battle_main():
    use battle_ui
    use battle_actions

# Ally names for display
define selected_ally_names = ["Kanami", "Kenshin", "Magic", "Rance", "Reset", "Sachiko", "Suzume"]

# Example usage
label battle_start:
    $ boss_health = 100
    $ selected_ally = None

    call screen battle_main
