# Enhanced Rance 10 Battle System for Ren'Py
# Based on your existing code with major UI improvements

# Preload all images
image boss = "images/combat_system/boss.webp"
image kenshin = "images/combat_system/kenshin.webp"
image magic = "images/combat_system/magic.webp"
image rance = "images/combat_system/rance.webp"
image reset = "images/combat_system/reset.webp"
image suzume = "images/combat_system/suzume.webp"

# UI Elements (create simple colored rectangles if you don't have these)
image hp_bar_red = Solid("#DC143C")
image hp_bar_blue = Solid("#1E90FF")
image ap_orb_active = Solid("#FFD700")
image ap_orb_used = Solid("#333333")
image guard_button = Solid("#3498db")
image menu_button = Solid("#95a5a6")

# Battle state tracking
default persistent.qmenu_bak = 0
default battle_round = 1
default enemy_hp = 2448177
default enemy_max_hp = 2448177
default ally_hp = 3307542
default ally_max_hp = 3307542
default current_ap = 4
default max_ap = 6

# Character states (0=ready, 1-3=cooldown turns)
default char_cooldowns = {
    "kenshin": 0,
    "magic": 0,
    "rance": 0,
    "reset": 0,
    "suzume": 0
}

# Character stats
default char_stats = {
    "kenshin": {"name": "Kenshin", "hp": 132245, "attacks": ["Power Strike", "Quick Slash"]},
    "magic": {"name": "Magic Girl", "hp": 126236, "attacks": ["Fireball", "Heal"]},
    "rance": {"name": "Rance", "hp": 167787, "attacks": ["Brutal Strike", "Special Move"]},
    "reset": {"name": "Reset", "hp": 543638, "attacks": ["Holy Light", "Absorb Curse"]},
    "suzume": {"name": "Suzume", "hp": 165734, "attacks": ["Sword Dance", "Shield Bash"]}
}

init python:
    # If quit the game mid battle
    if persistent.qmenu_bak == 2:
        persistent.quickmenu = True
        persistent.qmenu_bak = 0

    def use_character_attack(char_name, attack_type):
        """Handle character attack logic"""
        global current_ap, char_cooldowns, enemy_hp

        if char_cooldowns[char_name] > 0:
            return False  # Character on cooldown

        # Set character on cooldown
        char_cooldowns[char_name] = 3

        # Calculate damage and AP cost (simplified)
        if attack_type == "upper":
            damage = renpy.random.randint(50000, 80000)
            ap_cost = 2
        else:  # lower
            damage = renpy.random.randint(30000, 60000)
            ap_cost = 1

        if current_ap >= ap_cost:
            current_ap -= ap_cost
            enemy_hp = max(0, enemy_hp - damage)
            renpy.show_screen("damage_popup", damage)
            return True
        return False

    def guard_action():
        """Handle guard button"""
        global current_ap
        if current_ap >= 1:
            current_ap -= 1
            # Add guard logic here
            renpy.notify("Guard activated!")
            return True
        return False

    def advance_turn():
        """Advance to next turn"""
        global battle_round, current_ap, char_cooldowns
        battle_round += 1
        current_ap = min(max_ap, current_ap + 2)  # Regenerate 2 AP per turn

        # Reduce all cooldowns
        for char in char_cooldowns:
            if char_cooldowns[char] > 0:
                char_cooldowns[char] -= 1

# Enhanced battle screen with all UI improvements
screen battle_ui():
    # Background with gradient effect
    add Solid("#2a1810")
    add Solid("#5c2d1a") at transform:
        alpha 0.7

    # Boss area - upper 40% of screen
    frame:
        xfill True
        yfill False
        ysize int(config.screen_height * 0.4)
        background Solid("#8B0000")

        # Boss image with floating effect
        add "boss" at boss_breathe:
            xalign 0.5
            yalign 0.5
            zoom 0.65

        # Boss HP indicator (optional)
        if enemy_hp < enemy_max_hp * 0.3:
            text "BOSS WEAKENED!" at damage_float:
                xalign 0.5
                yalign 0.3
                color "#FF0000"
                size 40
                bold True

    # HP bars - horizontal split
    frame:
        ypos int(config.screen_height * 0.4)
        xfill True
        ysize 60
        background Solid("#000000")

        hbox:
            spacing 0

            # Enemy HP bar (left half)
            frame:
                xsize int(config.screen_width * 0.45)
                ysize 60
                background Solid("#8B0000")

                # HP fill
                frame:
                    xsize int(config.screen_width * 0.45 * (enemy_hp / float(enemy_max_hp)))
                    ysize 60
                    background Solid("#DC143C")

                text "Enemy HP: [enemy_hp:,]":
                    xalign 0.05
                    yalign 0.5
                    color "#FFFFFF"
                    size 18
                    bold True

            # Round indicator (center)
            frame:
                xsize int(config.screen_width * 0.1)
                ysize 60
                background Solid("#000000")

                text "Round\n[battle_round]":
                    xalign 0.5
                    yalign 0.5
                    color "#FFD700"
                    size 14
                    bold True
                    text_align 0.5

            # Ally HP bar (right half)
            frame:
                xsize int(config.screen_width * 0.45)
                ysize 60
                background Solid("#1E6091")

                # HP fill
                frame:
                    xsize int(config.screen_width * 0.45 * (ally_hp / float(ally_max_hp)))
                    ysize 60
                    background Solid("#1E90FF")

                text "Ally HP: [ally_hp:,]":
                    xalign 0.95
                    yalign 0.5
                    color "#FFFFFF"
                    size 18
                    bold True

    # AP System
    frame:
        ypos int(config.screen_height * 0.4) + 60
        xfill True
        ysize 50
        background Solid("#000000")

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 8

            for i in range(max_ap):
                if i < current_ap:
                    button:
                        xsize 35
                        ysize 35
                        background Solid("#FFD700")
                        hover_background Solid("#FFA500")
                        at ap_orb_glow
                        action NullAction()

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

    # Characters area - bottom section
    frame:
        ypos int(config.screen_height * 0.4) + 110
        xfill True
        ysize int(config.screen_height * 0.6) - 190
        background Solid("#1a1a2e")

        # Character lineup
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            # Kenshin
            call screen character_button("kenshin", char_cooldowns["kenshin"])

            # Magic
            call screen character_button("magic", char_cooldowns["magic"])

            # Rance (Hero - centered and larger)
            call screen character_button("rance", char_cooldowns["rance"], is_hero=True)

            # Reset
            call screen character_button("reset", char_cooldowns["reset"])

            # Suzume
            call screen character_button("suzume", char_cooldowns["suzume"])

    # Control buttons at bottom
    frame:
        ypos int(config.screen_height - 80)
        xfill True
        ysize 80
        background Solid("#000000")

        hbox:
            xfill True
            yalign 0.5

            # Menu button
            textbutton "MENU":
                xalign 0.1
                style "battle_button"
                text_style "battle_button_text"
                action ShowMenu("preferences")

            # Guard button (center)
            textbutton "🛡️ GUARD (1 AP)":
                xalign 0.5
                style "guard_button"
                text_style "guard_button_text"
                action Function(guard_action)
                sensitive current_ap >= 1

# Individual character button screen
screen character_button(char_name, cooldown, is_hero=False):
    $ char_data = char_stats[char_name]
    $ base_size = 160 if is_hero else 140
    $ char_height = 220 if is_hero else 200

    frame:
        xsize base_size
        ysize char_height
        background Solid("#2c3e50" if cooldown == 0 else "#1a1a1a")

        if is_hero:
            at hero_glow
        elif cooldown > 0:
            at cooldown_effect
        else:
            at ally_hover

        vbox:
            spacing 0

            # Character portrait (clickable area)
            if cooldown == 0:
                frame:
                    xsize base_size
                    ysize int(char_height * 0.7)
                    background None

                    # Upper half click area
                    button:
                        xsize base_size
                        ysize int(char_height * 0.35)
                        background char_name
                        hover_background char_name
                        action Function(use_character_attack, char_name, "upper")
                        at attack_hover_effect

                        # Attack name overlay
                        text char_data["attacks"][0]:
                            xalign 0.5
                            yalign 0.5
                            color "#FFFFFF"
                            size 12
                            bold True
                            background Solid("#4CAF50")
                            alpha 0.0

                    # Lower half click area
                    button:
                        ypos int(char_height * 0.35)
                        xsize base_size
                        ysize int(char_height * 0.35)
                        background char_name
                        hover_background char_name
                        action Function(use_character_attack, char_name, "lower")
                        at attack_hover_effect

                        text char_data["attacks"][1]:
                            xalign 0.5
                            yalign 0.5
                            color "#FFFFFF"
                            size 12
                            bold True
                            background Solid("#4CAF50")
                            alpha 0.0
            else:
                # Grayed out portrait when on cooldown
                add char_name:
                    xsize base_size
                    ysize int(char_height * 0.7)
                    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.3)

                # Cooldown timer
                frame:
                    xsize 30
                    ysize 30
                    background Solid("#e74c3c")
                    xalign 1.0
                    yalign 0.0
                    xoffset -10
                    yoffset -10
                    at cooldown_pulse

                    text str(cooldown):
                        xalign 0.5
                        yalign 0.5
                        color "#FFFFFF"
                        size 12
                        bold True

            # Character info panel
            frame:
                xsize base_size
                ysize int(char_height * 0.3)
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

# Damage popup screen
screen damage_popup(damage):
    timer 1.5 action Hide("damage_popup")

    text "-[damage:,]":
        xalign 0.5
        yalign 0.3
        color "#FF4444"
        size 60
        bold True
        at damage_float

# Enhanced transform effects
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

transform damage_float:
    yoffset 0 alpha 1.0
    linear 1.5 yoffset -100 alpha 0.0

# Button styles
style battle_button:
    background Solid("#95a5a6")
    hover_background Solid("#7f8c8d")
    xpadding 30
    ypadding 15

style battle_button_text:
    color "#FFFFFF"
    size 16
    bold True

style guard_button:
    background Solid("#3498db")
    hover_background Solid("#2980b9")
    xpadding 30
    ypadding 15

style guard_button_text:
    color "#FFFFFF"
    size 16
    bold True

# Battle flow labels (keeping your structure)
label start_battle:
    if persistent.quickmenu:
        $persistent.qmenu_bak = 2
    else:
        $persistent.qmenu_bak = 1
    $persistent.quickmenu = False
    $config.rollback_enabled = False

    # Initialize battle state
    $ battle_round = 1
    $ current_ap = 4
    $ enemy_hp = enemy_max_hp
    $ ally_hp = ally_max_hp
    $ char_cooldowns = {char: 0 for char in char_cooldowns}

    show screen battle_ui

    # Battle loop
    while enemy_hp > 0 and ally_hp > 0:
        "Turn [battle_round] - Choose your actions!"

        # Wait for player input or advance turn
        $ advance_turn()

        # Check win condition
        if enemy_hp <= 0:
            "Victory! The boss has been defeated!"
            jump battle_victory
        elif ally_hp <= 0:
            "Defeat... Your party has fallen."
            jump battle_defeat

    # Cleanup
    if persistent.qmenu_bak == 2:
        $persistent.quickmenu = True
    $persistent.qmenu_bak = 0
    hide screen battle_ui
    $renpy.block_rollback()
    $config.rollback_enabled = True

    jump after_battle

label battle_victory:
    hide screen battle_ui
    scene black with fade
    "Congratulations! You've won the battle!"
    jump after_battle

label battle_defeat:
    hide screen battle_ui
    scene black with fade
    "Game Over. Try again?"
    jump start_battle

label after_battle:
    scene forest with fade
    "The battle is over, and the heroes catch their breath."
    "Kanami: That was intense!"
    "Rance: Let's keep moving."
    return
