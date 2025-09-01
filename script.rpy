# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

# I want the HP bar be made into a less amateurish and less boring shape (straight line), I want it shaped like a Sword. Don't add too much complexity though, less is more as they say

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
    _sword_cache = {}

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

    def get_sword_bar(width, height, color, fill_percent):
        key = (width, height, color, fill_percent)
        if key not in _sword_cache:
            _sword_cache[key] = SwordBar(width, height, color, fill_percent)
        return _sword_cache[key]

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

    # Sword-shaped HP bar displayable
    class SwordBar(renpy.Displayable):
        def __init__(self, width, height, color, fill_percent):
            super().__init__()
            self.width = width
            self.height = height
            self.color = color
            self.fill_percent = max(0.0, min(1.0, fill_percent))

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Sword dimensions
            blade_width = self.width * 0.8
            blade_height = self.height * 0.7
            guard_width = self.width * 0.6
            guard_height = self.height * 0.15
            handle_width = self.width * 0.12
            handle_height = self.height * 0.15

            # Calculate fill based on percentage
            fill_height = blade_height * self.fill_percent

            # Center positions
            center_x = self.width / 2
            blade_start_y = 0
            guard_y = blade_height
            handle_y = guard_y + guard_height

            # Draw background sword (dark)
            bg_color = "#333333"

            # Background blade (tapered)
            blade_points = [
                (center_x, blade_start_y),  # tip
                (center_x - blade_width/6, blade_height * 0.3),
                (center_x - blade_width/4, blade_height),
                (center_x + blade_width/4, blade_height),
                (center_x + blade_width/6, blade_height * 0.3)
            ]
            c.polygon(bg_color, blade_points)

            # Background guard
            c.rect(bg_color, (center_x - guard_width/2, guard_y, guard_width, guard_height))

            # Background handle
            c.rect(bg_color, (center_x - handle_width/2, handle_y, handle_width, handle_height))

            # Draw filled portion (colored)
            if self.fill_percent > 0:
                # Filled blade portion
                if fill_height > 0:
                    # Calculate tapered blade fill
                    top_width_ratio = 1.0/6 + (1.0/4 - 1.0/6) * min(fill_height / (blade_height * 0.3), 1.0)
                    if fill_height <= blade_height * 0.3:
                        # Only tip portion
                        tip_ratio = fill_height / (blade_height * 0.3)
                        fill_points = [
                            (center_x, blade_start_y),
                            (center_x - blade_width * top_width_ratio * tip_ratio, fill_height),
                            (center_x + blade_width * top_width_ratio * tip_ratio, fill_height)
                        ]
                    else:
                        # Full tip + partial/full main blade
                        main_fill = min(fill_height, blade_height)
                        main_width_ratio = 1.0/6 + (1.0/4 - 1.0/6) * (main_fill - blade_height * 0.3) / (blade_height * 0.7)
                        fill_points = [
                            (center_x, blade_start_y),
                            (center_x - blade_width/6, blade_height * 0.3),
                            (center_x - blade_width * main_width_ratio, main_fill),
                            (center_x + blade_width * main_width_ratio, main_fill),
                            (center_x + blade_width/6, blade_height * 0.3)
                        ]
                    c.polygon(self.color, fill_points)

                # Filled guard (if HP is full enough)
                if self.fill_percent > 0.7:
                    guard_fill = min(1.0, (self.fill_percent - 0.7) / 0.2)
                    c.rect(self.color, (center_x - guard_width/2, guard_y, guard_width, guard_height * guard_fill))

                # Filled handle (if HP is nearly full)
                if self.fill_percent > 0.9:
                    handle_fill = min(1.0, (self.fill_percent - 0.9) / 0.1)
                    c.rect(self.color, (center_x - handle_width/2, handle_y, handle_width, handle_height * handle_fill))

            # Add subtle highlight on the blade edge
            if self.fill_percent > 0:
                highlight_color = "#ffffff"
                c.line(highlight_color, (center_x - 1, blade_start_y + 2), (center_x - 1, min(fill_height, blade_height) - 2), 1)

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

        # Enemy HP bar
        use sword_hp_bar_section("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)

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

        # Hero HP bar
        use sword_hp_bar_section("Hero", current_hp, max_hp, "#4169e1", bar_width)

# ========================
# Sword-Shaped HP Bar Component
# ========================
screen sword_hp_bar_section(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        fixed:
            xsize width
            ysize 80  # Taller to accommodate sword shape

            # Animated sword HP bar
            add get_sword_bar(width, 80, color, float(hp_value) / float(max_hp_value)):
                xalign 0.5
                yalign 0.5

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
