# Enhanced Rance 10 Battle System for Ren'Py - PROPERLY CODED

# Preload all images
image boss = "images/combat_system/boss.webp"
image kenshin = "images/combat_system/kenshin.webp"
image magic = "images/combat_system/magic.webp"
image rance = "images/combat_system/rance.webp"
image reset = "images/combat_system/reset.webp"
image suzume = "images/combat_system/suzume.webp"

# Battle state variables
default persistent.qmenu_bak = 0
default battle_round = 1
default enemy_hp = 2448177
default enemy_max_hp = 2448177
default ally_hp = 3307542
default ally_max_hp = 3307542
default current_ap = 4
default max_ap = 6

default char_cooldowns = {
    "kenshin": 0,
    "magic": 0,
    "rance": 0,
    "reset": 0,
    "suzume": 0
}

default char_stats = {
    "kenshin": {"name": "Kenshin", "hp": 132245, "attacks": ["Power Strike", "Quick Slash"]},
    "magic": {"name": "Magic Girl", "hp": 126236, "attacks": ["Fireball", "Heal"]},
    "rance": {"name": "Rance", "hp": 167787, "attacks": ["Brutal Strike", "Special Move"]},
    "reset": {"name": "Reset", "hp": 543638, "attacks": ["Holy Light", "Absorb Curse"]},
    "suzume": {"name": "Suzume", "hp": 165734, "attacks": ["Sword Dance", "Shield Bash"]}
}

init python:
    if persistent.qmenu_bak == 2:
        persistent.quickmenu = True
        persistent.qmenu_bak = 0

    def use_character_attack(char_name, attack_type):
        global current_ap, char_cooldowns, enemy_hp

        if char_cooldowns[char_name] > 0 or current_ap <= 0:
            return False

        char_cooldowns[char_name] = 3
        damage = renpy.random.randint(30000, 80000)
        ap_cost = 2 if attack_type == "upper" else 1

        if current_ap >= ap_cost:
            current_ap -= ap_cost
            enemy_hp = max(0, enemy_hp - damage)
            renpy.restart_interaction()
            return True
        return False

    def guard_action():
        global current_ap
        if current_ap >= 1:
            current_ap -= 1
            renpy.restart_interaction()
            return True
        return False

    def advance_turn():
        global battle_round, current_ap, char_cooldowns
        battle_round += 1
        current_ap = min(max_ap, current_ap + 2)

        for char in char_cooldowns:
            if char_cooldowns[char] > 0:
                char_cooldowns[char] -= 1
        renpy.restart_interaction()

screen battle_ui():
    modal True

    add Solid("#2a1810")

    # Boss area
    frame:
        xpos 0
        ypos 0
        xsize config.screen_width
        ysize int(config.screen_height * 0.4)
        background Solid("#8B0000")

        add "boss" at boss_breathe:
            xalign 0.5
            yalign 0.5
            zoom 0.65

    # HP bars
    frame:
        xpos 0
        ypos int(config.screen_height * 0.4)
        xsize config.screen_width
        ysize 60
        background Solid("#000000")

        # Enemy HP
        frame:
            xpos 0
            ypos 0
            xsize int(config.screen_width * 0.45)
            ysize 60
            background Solid("#8B0000")

            frame:
                xpos 0
                ypos 0
                xsize int(config.screen_width * 0.45 * (enemy_hp / float(enemy_max_hp)))
                ysize 60
                background Solid("#DC143C")

            text "Enemy HP: [enemy_hp:,]":
                xpos 20
                yalign 0.5
                color "#FFFFFF"
                size 18
                bold True

        # Round indicator
        frame:
            xpos int(config.screen_width * 0.45)
            ypos 0
            xsize int(config.screen_width * 0.1)
            ysize 60
            background Solid("#FFD700")

            text "Round\n[battle_round]":
                xalign 0.5
                yalign 0.5
                color "#000000"
                size 14
                bold True
                text_align 0.5

        # Ally HP
        frame:
            xpos int(config.screen_width * 0.55)
            ypos 0
            xsize int(config.screen_width * 0.45)
            ysize 60
            background Solid("#1E6091")

            frame:
                xpos 0
                ypos 0
                xsize int(config.screen_width * 0.45 * (ally_hp / float(ally_max_hp)))
                ysize 60
                background Solid("#1E90FF")

            text "Ally HP: [ally_hp:,]":
                xpos int(config.screen_width * 0.45) - 200
                yalign 0.5
                color "#FFFFFF"
                size 18
                bold True

    # AP system
    frame:
        xpos 0
        ypos int(config.screen_height * 0.4) + 60
        xsize config.screen_width
        ysize 50
        background Solid("#000000")

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 8

            for i in range(max_ap):
                if i < current_ap:
                    frame:
                        xsize 35
                        ysize 35
                        background Solid("#FFD700")
                        at ap_orb_glow

                        text str(i+1):
                            xalign 0.5
                            yalign 0.5
                            color "#000000"
                            size 14
                            bold True
                else:
                    frame:
                        xsize 35
                        ysize 35
                        background Solid("#333333")

                        text str(i+1):
                            xalign 0.5
                            yalign 0.5
                            color "#888888"
                            size 14
                            bold True

    # Characters area
    frame:
        xpos 0
        ypos int(config.screen_height * 0.4) + 110
        xsize config.screen_width
        ysize int(config.screen_height * 0.6) - 190
        background Solid("#1a1a2e")

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            use character_slot("kenshin", False)
            use character_slot("magic", False)
            use character_slot("rance", True)
            use character_slot("reset", False)
            use character_slot("suzume", False)

    # Controls
    frame:
        xpos 0
        ypos config.screen_height - 80
        xsize config.screen_width
        ysize 80
        background Solid("#000000")

        textbutton "MENU":
            xpos 50
            yalign 0.5
            background Solid("#95a5a6")
            hover_background Solid("#7f8c8d")
            xpadding 30
            ypadding 15
            text_color "#FFFFFF"
            text_size 16
            text_bold True
            action ShowMenu("preferences")

        textbutton "🛡️ GUARD (1 AP)":
            xalign 0.5
            yalign 0.5
            background Solid("#3498db")
            hover_background Solid("#2980b9")
            xpadding 30
            ypadding 15
            text_color "#FFFFFF"
            text_size 16
            text_bold True
            action Function(guard_action)
            sensitive current_ap >= 1

screen character_slot(char_name, is_hero):
    $ char_data = char_stats[char_name]
    $ cooldown = char_cooldowns[char_name]
    $ base_width = 160 if is_hero else 140
    $ base_height = 220 if is_hero else 200

    frame:
        xsize base_width
        ysize base_height
        background Solid("#2c3e50")

        if is_hero:
            at hero_glow
        elif cooldown > 0:
            at cooldown_effect
        else:
            at ally_hover

        vbox:
            spacing 0

            # Portrait with click zones
            frame:
                xsize base_width
                ysize int(base_height * 0.7)
                background None

                if cooldown == 0:
                    # Upper click zone
                    button:
                        xpos 0
                        ypos 0
                        xsize base_width
                        ysize int(base_height * 0.35)
                        background char_name
                        hover_background char_name
                        action Function(use_character_attack, char_name, "upper")
                        at attack_hover_effect

                    # Lower click zone
                    button:
                        xpos 0
                        ypos int(base_height * 0.35)
                        xsize base_width
                        ysize int(base_height * 0.35)
                        background char_name
                        hover_background char_name
                        action Function(use_character_attack, char_name, "lower")
                        at attack_hover_effect

                    # Attack labels (overlay)
                    frame:
                        xpos 0
                        ypos 0
                        xsize base_width
                        ysize int(base_height * 0.35)
                        background Solid("#4CAF50")
                        alpha 0.0
                        at attack_label_fade

                        text char_data["attacks"][0]:
                            xalign 0.5
                            yalign 0.5
                            color "#FFFFFF"
                            size 10
                            bold True

                    frame:
                        xpos 0
                        ypos int(base_height * 0.35)
                        xsize base_width
                        ysize int(base_height * 0.35)
                        background Solid("#4CAF50")
                        alpha 0.0
                        at attack_label_fade

                        text char_data["attacks"][1]:
                            xalign 0.5
                            yalign 0.5
                            color "#FFFFFF"
                            size 10
                            bold True
                else:
                    # Cooldown display
                    add char_name:
                        xsize base_width
                        ysize int(base_height * 0.7)
                        matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.3)

                    if cooldown > 0:
                        frame:
                            xsize 30
                            ysize 30
                            background Solid("#e74c3c")
                            xpos base_width - 40
                            ypos 10
                            at cooldown_pulse

                            text str(cooldown):
                                xalign 0.5
                                yalign 0.5
                                color "#FFFFFF"
                                size 12
                                bold True

            # Info panel
            frame:
                xsize base_width
                ysize int(base_height * 0.3)
                background Solid("#000000")
                alpha 0.8

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 3

                    text char_data["name"]:
                        xalign 0.5
                        color "#FFD700"
                        size 12
                        bold True

                    text str(char_data["hp"]):
                        xalign 0.5
                        color "#4CAF50"
                        size 11

# Transforms
transform boss_breathe:
    yoffset 0 zoom 0.65
    linear 3.0 yoffset -10 zoom 0.67
    linear 3.0 yoffset 0 zoom 0.65
    repeat

transform hero_glow:
    matrixcolor BrightnessMatrix(0.2)
    linear 2.0 matrixcolor BrightnessMatrix(0.4)
    linear 2.0 matrixcolor BrightnessMatrix(0.2)
    repeat

transform ally_hover:
    zoom 1.0 yoffset 0
    on hover:
        linear 0.3 zoom 1.05 yoffset -10
    on idle:
        linear 0.3 zoom 1.0 yoffset 0

transform cooldown_effect:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.5)
    alpha 0.6

transform cooldown_pulse:
    zoom 1.0
    linear 0.5 zoom 1.1
    linear 0.5 zoom 1.0
    repeat

transform ap_orb_glow:
    matrixcolor BrightnessMatrix(0.0)
    linear 1.0 matrixcolor BrightnessMatrix(0.3)
    linear 1.0 matrixcolor BrightnessMatrix(0.0)
    repeat

transform attack_hover_effect:
    on hover:
        linear 0.2 matrixcolor BrightnessMatrix(0.3)
    on idle:
        linear 0.2 matrixcolor BrightnessMatrix(0.0)

transform attack_label_fade:
    alpha 0.0
    on hover:
        linear 0.2 alpha 0.8
    on idle:
        linear 0.2 alpha 0.0

# Battle flow
label start_battle:
    if persistent.quickmenu:
        $ persistent.qmenu_bak = 2
    else:
        $ persistent.qmenu_bak = 1
    $ persistent.quickmenu = False
    $ config.rollback_enabled = False

    $ battle_round = 1
    $ current_ap = 4
    $ enemy_hp = enemy_max_hp
    $ ally_hp = ally_max_hp
    $ char_cooldowns = {char: 0 for char in char_cooldowns}

    show screen battle_ui

    while enemy_hp > 0 and ally_hp > 0:
        "Round [battle_round] - Choose your actions!"
        pause

        $ enemy_damage = renpy.random.randint(50000, 100000)
        $ ally_hp = max(0, ally_hp - enemy_damage)

        if enemy_hp <= 0:
            jump battle_victory
        elif ally_hp <= 0:
            jump battle_defeat

        $ advance_turn()

    hide screen battle_ui
    if persistent.qmenu_bak == 2:
        $ persistent.quickmenu = True
    $ persistent.qmenu_bak = 0
    $ renpy.block_rollback()
    $ config.rollback_enabled = True

    jump after_battle

label battle_victory:
    hide screen battle_ui
    scene black with fade
    "Victory! The boss has been defeated!"
    jump after_battle

label battle_defeat:
    hide screen battle_ui
    scene black with fade
    "Defeat! Your party has fallen."
    jump start_battle

label after_battle:
    scene forest with fade
    "The battle is over, and the heroes catch their breath."
    "Kanami: That was intense!"
    "Rance: Let's keep moving."
    return
