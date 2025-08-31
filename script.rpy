# Simplified Game UI with Witcher 3 HP Bar

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
    zoom 0.9

# ========================
# Python Helpers
# ========================
init python:
    import math
    def get_hp_percent():
        return current_hp / float(max_hp)

    def get_enemy_hp_percent():
        return enemy_hp / float(enemy_max_hp)

    def get_orb_positions(num_orbs, radius=70):
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = 140 + radius * math.cos(angle) - 15
            y = 140 + radius * math.sin(angle) - 15
            positions.append((int(x), int(y)))
        return positions

    class SimpleCircle(renpy.Displayable):
        def __init__(self, radius, color):
            super().__init__()
            self.radius = radius
            self.color = color
        def render(self, w, h, st, at):
            size = 2 * self.radius
            r = renpy.Render(size, size)
            c = r.canvas()
            c.circle(self.color, (self.radius, self.radius), self.radius)
            return r

# ========================
# Simple Displayables
# ========================
define round_bg = SimpleCircle(70, "#505050")
define orb_active = SimpleCircle(15, "#ffd700")
define orb_inactive = SimpleCircle(15, "#666666")

# ========================
# Main UI Screen
# ========================
screen round_ui():
    add Solid("#808080")

    # Enemy HP bar (left of center)
    fixed:
        xpos 50
        ypos 200
        add Solid("#000000") xsize 200 ysize 12
        $ fill_width = int(200 * get_enemy_hp_percent())
        add Solid("#c41e3a") xsize fill_width ysize 12
        text "[enemy_hp]%":
            xpos 210
            ypos -2
            size 16
            color "#ffffff"

    # Round circle (center)
    fixed:
        xalign 0.5
        yalign 0.5
        xsize 280
        ysize 280

        # Background circle
        add round_bg:
            xpos 70
            ypos 70

        # Round text
        vbox:
            xalign 0.5
            yalign 0.5
            text "Round" size 22 color "#FFFFFF" xalign 0.5
            text "[current_round]" size 56 color "#FFFFFF" xalign 0.5

        # AP Orbs
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            add (orb_active if i < available_ap else orb_inactive):
                xpos x
                ypos y
                at (glow if i < available_ap else inactive)

    # Hero HP bar (right of center)
    fixed:
        xpos 1100
        ypos 200
        add Solid("#000000") xsize 200 ysize 12
        $ fill_width = int(200 * get_hp_percent())
        add Solid("#4169e1") xsize fill_width ysize 12
        text "[current_hp]%":
            xpos 210
            ypos -2
            size 16
            color "#ffffff"

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
