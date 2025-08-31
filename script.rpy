# Simplified Game UI with HP Bars

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3
default current_hp = 85
default max_hp = 100
default enemy_hp = 60
default enemy_max_hp = 80

# ========================
# ATL Transforms
# ========================
transform glow:
    ease 1.5 alpha 0.6 zoom 1.05
    ease 1.5 alpha 1.0 zoom 1.0
    repeat

transform inactive:
    alpha 0.4

# ========================
# Python Helpers
# ========================
init python:
    import math

    def get_orb_positions(num_orbs):
        positions = []
        center = 70
        radius = 70
        orb_radius = 15
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = center + radius * math.cos(angle) - orb_radius
            y = center + radius * math.sin(angle) - orb_radius
            positions.append((int(x), int(y)))
        return positions

# ========================
# Main UI Screen
# ========================
screen round_ui():
    add "#808080"

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar
        vbox:
            spacing 5
            text "Enemy" size 14 color "#ffffff"
            fixed:
                xsize 200
                ysize 12
                add "#000000" xsize 200 ysize 12
                add "#c41e3a" xsize int(200 * enemy_hp / enemy_max_hp) ysize 12
            text "[enemy_hp]%" size 16 color "#ffffff"

        # Round circle
        fixed:
            xsize 140
            ysize 140

            # Background circle
            add Solid("#505050", xysize=(140, 140)) at transform:
                around (0.5, 0.5)

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                text "Round" size 22 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 56 color "#FFFFFF" xalign 0.5

            # AP Orbs
            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                $ is_active = i < available_ap
                add Solid("#ffd700" if is_active else "#666666", xysize=(30, 30)):
                    xpos x
                    ypos y
                    at (glow if is_active else inactive)
                    around (0.5, 0.5)

        # Hero HP bar
        vbox:
            spacing 5
            text "Hero" size 14 color "#ffffff"
            fixed:
                xsize 200
                ysize 12
                add "#000000" xsize 200 ysize 12
                add "#4169e1" xsize int(200 * current_hp / max_hp) ysize 12
            text "[current_hp]%" size 16 color "#ffffff"

# ========================
# Demo Label
# ========================
label start:
    show screen round_ui
    "Round [current_round], AP [available_ap]/[max_ap], Hero HP [current_hp]/[max_hp], Enemy HP [enemy_hp]/[enemy_max_hp]"
    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start
        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start
        "Take Damage" if current_hp > 0:
            $ current_hp = max(0, current_hp - 15)
            jump start
        "Heal" if current_hp < max_hp:
            $ current_hp = min(max_hp, current_hp + 20)
            jump start
        "Damage Enemy" if enemy_hp > 0:
            $ enemy_hp = max(0, enemy_hp - 20)
            jump start
        "Enemy Heals" if enemy_hp < enemy_max_hp:
            $ enemy_hp = min(enemy_max_hp, enemy_hp + 15)
            jump start
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start
        "Exit":
            return
