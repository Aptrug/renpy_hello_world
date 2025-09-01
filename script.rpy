# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

# I want the HP bar be made into a less amateurish and less boring shape (straight line), I want it shaped like a Kilij, make the hero bar pointed up, while enemies pointed down

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

# NOTE: gui.notify_text_size is defined as 24 in gui.rpy

# ========================
# ATL Transforms
# ========================
transform glow:
    ease 1.5 alpha 0.6
    ease 1.5 alpha 1.0
    repeat

transform inactive:
    alpha 0.4

transform sun_aura:
    blur 2
    ease 4.0 alpha 0.05
    ease 4.0 alpha 0.15
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

    # Kilij HP Bar Displayable
    class KilijHPBar(renpy.Displayable):
        def __init__(self, width, height, current_hp, max_hp, color, upward=True):
            super().__init__()
            self.width = width
            self.height = height
            self.current_hp = current_hp
            self.max_hp = max_hp
            self.color = color
            self.upward = upward

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Calculate HP percentage
            hp_percent = self.current_hp / float(self.max_hp) if self.max_hp > 0 else 0

            # Kilij blade dimensions
            blade_width = self.width - 20
            blade_height = self.height - 25
            hilt_width = 30
            hilt_height = 15

            # Starting positions
            start_x = 10
            start_y = 10 if self.upward else self.height - 25

            if self.upward:
                # Hero kilij (pointing up)
                # Create the kilij shape path - blade pointing upward
                points = [
                    # Hilt (bottom)
                    (start_x + blade_width//2 - hilt_width//2, start_y + blade_height),
                    (start_x + blade_width//2 + hilt_width//2, start_y + blade_height),
                    (start_x + blade_width//2 + hilt_width//2, start_y + blade_height + hilt_height),
                    (start_x + blade_width//2 - hilt_width//2, start_y + blade_height + hilt_height),

                    # Back to hilt connection
                    (start_x + blade_width//2 - hilt_width//2, start_y + blade_height),

                    # Blade left edge (curved outward)
                    (start_x + blade_width//2 - 25, start_y + blade_height * 0.7),
                    (start_x + blade_width//2 - 30, start_y + blade_height * 0.4),
                    (start_x + blade_width//2 - 25, start_y + blade_height * 0.1),

                    # Tip (pointed)
                    (start_x + blade_width//2, start_y),

                    # Blade right edge (curved outward)
                    (start_x + blade_width//2 + 25, start_y + blade_height * 0.1),
                    (start_x + blade_width//2 + 30, start_y + blade_height * 0.4),
                    (start_x + blade_width//2 + 25, start_y + blade_height * 0.7),

                    # Back to hilt
                    (start_x + blade_width//2 + hilt_width//2, start_y + blade_height)
                ]
            else:
                # Enemy kilij (pointing down)
                points = [
                    # Hilt (top)
                    (start_x + blade_width//2 - hilt_width//2, start_y),
                    (start_x + blade_width//2 + hilt_width//2, start_y),
                    (start_x + blade_width//2 + hilt_width//2, start_y + hilt_height),
                    (start_x + blade_width//2 - hilt_width//2, start_y + hilt_height),

                    # Blade connection
                    (start_x + blade_width//2 - hilt_width//2, start_y + hilt_height),

                    # Blade left edge (curved outward)
                    (start_x + blade_width//2 - 25, start_y + hilt_height + blade_height * 0.3),
                    (start_x + blade_width//2 - 30, start_y + hilt_height + blade_height * 0.6),
                    (start_x + blade_width//2 - 25, start_y + hilt_height + blade_height * 0.9),

                    # Tip (pointed down)
                    (start_x + blade_width//2, start_y + hilt_height + blade_height),

                    # Blade right edge (curved outward)
                    (start_x + blade_width//2 + 25, start_y + hilt_height + blade_height * 0.9),
                    (start_x + blade_width//2 + 30, start_y + hilt_height + blade_height * 0.6),
                    (start_x + blade_width//2 + 25, start_y + hilt_height + blade_height * 0.3),

                    # Back to hilt
                    (start_x + blade_width//2 + hilt_width//2, start_y + hilt_height)
                ]

            # Draw background kilij (dark outline)
            c.polygon("#333333", points)

            # Calculate filled area based on HP
            if hp_percent > 0:
                if self.upward:
                    # Fill from bottom up for hero
                    fill_height = blade_height * hp_percent
                    fill_y = start_y + blade_height - fill_height

                    # Create filled kilij shape
                    fill_points = []
                    if hp_percent >= 0.95:  # Almost full - include most of the blade
                        fill_points = points[4:-1]  # Exclude hilt, include most blade
                    elif hp_percent >= 0.7:  # Upper portion
                        mid_point = int(len(points[4:-1]) * (hp_percent - 0.7) / 0.25)
                        fill_points = [
                            (start_x + blade_width//2 - hilt_width//2, start_y + blade_height),
                            (start_x + blade_width//2 + hilt_width//2, start_y + blade_height)
                        ] + points[4:4+mid_point+1]
                    else:  # Lower portion (hilt area)
                        fill_points = [
                            (start_x + blade_width//2 - hilt_width//2, start_y + blade_height),
                            (start_x + blade_width//2 + hilt_width//2, start_y + blade_height),
                            (start_x + blade_width//2 + hilt_width//2, start_y + blade_height + hilt_height * hp_percent/0.7),
                            (start_x + blade_width//2 - hilt_width//2, start_y + blade_height + hilt_height * hp_percent/0.7)
                        ]
                else:
                    # Fill from top down for enemy
                    fill_height = (blade_height + hilt_height) * hp_percent

                    if hp_percent >= 0.8:  # Include blade
                        blade_percent = (hp_percent - 0.2) / 0.8
                        mid_point = int(len(points[4:-1]) * blade_percent)
                        fill_points = points[0:4] + points[4:4+mid_point+1]
                    else:  # Just hilt
                        hilt_fill = hilt_height * (hp_percent / 0.2)
                        fill_points = [
                            (start_x + blade_width//2 - hilt_width//2, start_y),
                            (start_x + blade_width//2 + hilt_width//2, start_y),
                            (start_x + blade_width//2 + hilt_width//2, start_y + hilt_fill),
                            (start_x + blade_width//2 - hilt_width//2, start_y + hilt_fill)
                        ]

                if fill_points:
                    c.polygon(self.color, fill_points)

            return r

# ========================
# Main UI Screen
# ========================
screen round_ui():
    # Cache bar width calculation
    $ bar_width = (config.screen_width - 340) // 2
    $ circle_diameter = CIRCLE_RADIUS * 2

    add "#808080"

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar (kilij pointing down)
        use kilij_hp_bar_section("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width, False)

        # Round circle
        fixed:
            xsize circle_diameter
            ysize circle_diameter

            # Subtle golden aura (stays within orb boundary)
            add get_circle(CIRCLE_RADIUS + 4, "#ffd700") align (0.5, 0.5) at sun_aura

            # Cached background circle
            add get_circle(CIRCLE_RADIUS, "#505050") align (0.5, 0.5)

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 20 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 60 color "#FFFFFF" xalign 0.5

            # Cached AP Orbs
            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                add get_circle(ORB_RADIUS, "#ffd700" if i < available_ap else "#666666"):
                    xpos x
                    ypos y
                    at (glow if i < available_ap else inactive)

        # Hero HP bar (kilij pointing up)
        use kilij_hp_bar_section("Hero", current_hp, max_hp, "#4169e1", bar_width, True)

# ========================
# Kilij HP Bar Component
# ========================
screen kilij_hp_bar_section(label, hp_value, max_hp_value, color, width, upward):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        # Kilij-shaped HP bar
        add KilijHPBar(width, 80, hp_value, max_hp_value, color, upward)

        text "[hp_value]%" size gui.notify_text_size color "#ffffff"

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
