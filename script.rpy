# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Less is more.

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
default CIRCLE_RADIUS = 72
default ORB_RADIUS = 12

# ========================
# ATL Transforms
# ========================
transform glow:
    ease 1.5 alpha 0.6
    ease 1.5 alpha 1.0
    repeat

transform inactive:
    alpha 0.4

# ========================
# Python Helpers
# ========================
init python:
    import math

    # Cache orb positions and circles
    _orb_cache = {}
    _circles = {}

    def get_orb_positions(num_orbs):
        if num_orbs not in _orb_cache:
            positions = []
            if num_orbs > 0:
                step = 6.283185307179586 / num_orbs  # 2*pi pre-calculated
                for i in range(num_orbs):
                    angle = step * i - 1.5707963267948966  # -pi/2 pre-calculated
                    x = CIRCLE_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
                    y = CIRCLE_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
                    positions.append((int(x), int(y)))
            _orb_cache[num_orbs] = positions
        return _orb_cache[num_orbs]

    def get_circle(radius, color):
        key = (radius, color)
        if key not in _circles:
            _circles[key] = SimpleCircle(radius, color)
        return _circles[key]

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
# Main UI Screen
# ========================
screen round_ui():
    add "#808080"

    $ bar_width = (config.screen_width - 340) // 2
    $ circle_size = CIRCLE_RADIUS * 2

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar
        vbox:
            spacing 5
            text "Enemy" size 14 color "#ffffff"
            fixed:
                xsize bar_width
                ysize 12
                add "#000000" xsize bar_width ysize 12
                add "#c41e3a" xsize int(bar_width * enemy_hp / enemy_max_hp) ysize 12
            text "[enemy_hp]%" size 16 color "#ffffff"

        # Round circle
        fixed:
            xsize circle_size
            ysize circle_size

            # Background circle
            add get_circle(CIRCLE_RADIUS, "#505050") align (0.5, 0.5)

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 22 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 56 color "#FFFFFF" xalign 0.5

            # AP Orbs
            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                add get_circle(ORB_RADIUS, "#ffd700" if i < available_ap else "#666666"):
                    xpos x
                    ypos y
                    at (glow if i < available_ap else inactive)

        # Hero HP bar
        vbox:
            spacing 5
            text "Hero" size 14 color "#ffffff"
            fixed:
                xsize bar_width
                ysize 12
                add "#000000" xsize bar_width ysize 12
                add "#4169e1" xsize int(bar_width * current_hp / max_hp) ysize 12
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
