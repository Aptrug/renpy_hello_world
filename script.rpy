# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

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

transform golden_glow:
    ease 2.0 alpha 0.3
    ease 2.0 alpha 0.8
    repeat

# ========================
# Python Helpers
# ========================
init python:
    import math

    # Cache orb positions and circles for lower CPU usage
    _orb_cache = {}
    _circle_cache = {}

    def get_orb_positions(num_orbs):
        if num_orbs not in _orb_cache:
            positions = []
            if num_orbs > 0:
                step = 6.283185307179586 / num_orbs  # 2*pi
                for i in range(num_orbs):
                    angle = step * i - 1.5707963267948966  # -pi/2
                    x = CIRCLE_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
                    y = CIRCLE_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
                    positions.append((int(x), int(y)))
            _orb_cache[num_orbs] = positions
        return _orb_cache[num_orbs]

    def get_circle(radius, color):
        key = (radius, color)
        if key not in _circle_cache:
            _circle_cache[key] = SimpleCircle(radius, color)
        return _circle_cache[key]

    # CRITICAL: SimpleCircle class is required for proper circular rendering
    # DO NOT REMOVE - Ren'Py's Solid creates squares, this creates actual circles
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
    # Cache bar width calculation
    $ bar_width = (config.screen_width - 340) // 2

    add "#808080"

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar
        use hp_bar_section("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)

        # Round circle
        fixed:
            xsize (CIRCLE_RADIUS + 8) * 2
            ysize (CIRCLE_RADIUS + 8) * 2

            # Golden glow aura (larger circle behind)
            add get_circle(CIRCLE_RADIUS + 8, "#ffd700") align (0.5, 0.5) at golden_glow

            # Main background circle
            add get_circle(CIRCLE_RADIUS, "#505050") align (0.5, 0.5)

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 22 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 56 color "#FFFFFF" xalign 0.5

            # Cached AP Orbs
            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                add get_circle(ORB_RADIUS, "#ffd700" if i < available_ap else "#666666"):
                    xpos x
                    ypos y
                    at (glow if i < available_ap else inactive)

        # Hero HP bar
        use hp_bar_section("Hero", current_hp, max_hp, "#4169e1", bar_width)

# ========================
# Reusable HP Bar Component
# ========================
screen hp_bar_section(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size 14 color "#ffffff"

        fixed:
            xsize width + 4
            ysize 16

            # Frame and background
            add "#333333" xsize width + 4 ysize 16
            add "#000000" xsize width ysize 12 xpos 2 ypos 2

            # Animated HP bar
            bar:
                value AnimatedValue(hp_value, max_hp_value, 0.8)
                range max_hp_value
                xsize width
                ysize 12
                xpos 2
                ypos 2
                left_bar color
                right_bar "#000000"

            # Highlight
            add "#ffffff" xsize width ysize 1 xpos 2 ypos 2 alpha 0.3

        text "[hp_value]%" size 16 color "#ffffff"

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
