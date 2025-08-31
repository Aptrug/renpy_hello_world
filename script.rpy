# I want you to add an HP bar to the top left and make it look exactly like Witcher 3 HP bar

# Simplified Game UI with Witcher 3 HP Bar

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3
default current_hp = 85
default max_hp = 100

# ========================
# ATL Transforms
# ========================
transform glow:
    ease 1.5 alpha 0.6 zoom 1.05
    ease 1.5 alpha 1.0 zoom 1.0
    repeat

transform inactive:
    alpha 0.4
    zoom 0.9

# ========================
# Python Helpers
# ========================
init python:
    import math
    def get_hp_percent():
        return current_hp / float(max_hp)

    def get_orb_positions(num_orbs, radius=70):
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = 140 + radius * math.cos(angle) - 15  # 140 = center, 15 = orb radius
            y = 140 + radius * math.sin(angle) - 15
            positions.append((int(x), int(y)))
        return positions

# ========================
# Simple Displayables
# ========================
define round_bg = "#505050"
define orb_active = "#ffd700"
define orb_inactive = "#666666"

# ========================
# HP Bar Screen
# ========================
screen hp_bar():
    fixed:
        xpos 30
        ypos 30
        # Background
        add Solid("#000000") xsize 200 ysize 12
        # Red fill
        $ fill_width = int(200 * get_hp_percent())
        add Solid("#c41e3a") xsize fill_width ysize 12
        # HP percentage
        text "[current_hp]%":
            xpos 210
            ypos -2
            size 16
            color "#ffffff"

# ========================
# Main UI Screen
# ========================
screen round_ui():
    add Solid("#808080")

    # HP bar
    use hp_bar

    # Round UI
    fixed:
        xalign 0.5
        yalign 0.75
        xsize 280
        ysize 280

        # Background circle
        add Solid(round_bg):
            xsize 140
            ysize 140
            xpos 70
            ypos 70

        # Glow effect
        add Solid("#ffd700"):
            xsize 140
            ysize 140
            xpos 70
            ypos 70
            alpha 0.3
            blur 15
            at glow

        # Round text
        vbox:
            xalign 0.5
            yalign 0.5
            text "Round" size 22 color "#FFFFFF" xalign 0.5
            text "[current_round]" size 56 color "#FFFFFF" xalign 0.5

        # AP Orbs
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            add Solid(orb_active if i < available_ap else orb_inactive):
                xpos x
                ypos y
                xsize 30
                ysize 30
                at (glow if i < available_ap else inactive)

# ========================
# Demo Label
# ========================
label start:
    show screen round_ui
    "Round [current_round], AP [available_ap]/[max_ap], HP [current_hp]/[max_hp]"
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
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start
        "Exit":
            return
