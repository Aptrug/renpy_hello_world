# ========================
# Game Variables
# ========================
default current_round = 18
default max_ap = 6
default available_ap = 4

# HP Variables
default enemy_hp = 0.75
default enemy_max_hp = 1.0
default hero_hp = 0.50
default hero_max_hp = 1.0

define ROUND_RADIUS = 70
define ORB_RADIUS = 15

# HP Bar Constants
define HP_BAR_WIDTH = 400
define HP_BAR_HEIGHT = 80

# ========================
# ATL Transforms
# ========================
transform orb_glow:
    parallel:
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
    parallel:
        ease 0.1 additive 0.3
        ease 0.1 additive 0.0
    repeat

transform round_breathe:
    ease 3.0 zoom 1.05 alpha 0.8
    ease 3.0 zoom 1.0 alpha 1.0
    repeat

transform orb_inactive:
    alpha 0.4
    zoom 0.9

# Wave animations for HP bars
transform hp_wave_enemy(wave_speed=3.0):
    xpos -180
    alpha 0.0
    linear wave_speed xpos HP_BAR_WIDTH alpha 0.6
    alpha 0.0
    repeat

transform hp_wave_hero(wave_speed=3.0):
    xpos HP_BAR_WIDTH + 180
    alpha 0.0
    linear wave_speed xpos -180 alpha 0.6
    alpha 0.0
    repeat

# Health state animations
transform low_hp_pulse:
    ease 1.5 alpha 0.7 additive 0.2
    ease 1.5 alpha 1.0 additive 0.0
    repeat

transform critical_hp_flash:
    ease 0.6 alpha 0.8 additive 0.4
    ease 0.6 alpha 1.0 additive 0.0
    repeat

transform critical_hp_text:
    ease 0.8 zoom 1.0 alpha 0.9
    ease 0.8 zoom 1.1 alpha 1.0
    repeat

transform low_hp_text:
    ease 1.2 zoom 1.0
    ease 1.2 zoom 1.05
    repeat

# VS Circle glow
transform vs_glow:
    parallel:
        ease 2.0 alpha 0.8 additive 0.3
        ease 2.0 alpha 1.0 additive 0.0
    parallel:
        ease 2.0 zoom 1.0
        ease 2.0 zoom 1.05
    repeat

# ========================
# Python Helpers & Custom Displayables
# ========================
init python:
    import math
    import pygame

    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.radius = radius
            self.color = color
            self.border_color = border_color
            self.border_width = border_width

        def render(self, width, height, st, at):
            size = self.radius * 2
            r = renpy.Render(size, size)
            c = r.canvas()

            if self.color:
                c.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                c.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return r

    class FalchionBar(renpy.Displayable):
        def __init__(self, width, height, is_enemy=True, bg_color="#1a1a1a", **kwargs):
            super(FalchionBar, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy
            self.bg_color = bg_color

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create falchion blade shape points based on CSS clip-path
            if self.is_enemy:
                # Enemy: polygon(0 35%, 65% 35%, 75% 45%, 82% 60%, 88% 75%, 92% 85%, 96% 92%, 100% 95%, 98% 80%, 94% 65%, 88% 50%, 82% 35%, 75% 25%, 65% 18%, 0 18%)
                points = [
                    (0, int(self.height * 0.35)),
                    (int(self.width * 0.65), int(self.height * 0.35)),
                    (int(self.width * 0.75), int(self.height * 0.45)),
                    (int(self.width * 0.82), int(self.height * 0.60)),
                    (int(self.width * 0.88), int(self.height * 0.75)),
                    (int(self.width * 0.92), int(self.height * 0.85)),
                    (int(self.width * 0.96), int(self.height * 0.92)),
                    (int(self.width * 1.0), int(self.height * 0.95)),
                    (int(self.width * 0.98), int(self.height * 0.80)),
                    (int(self.width * 0.94), int(self.height * 0.65)),
                    (int(self.width * 0.88), int(self.height * 0.50)),
                    (int(self.width * 0.82), int(self.height * 0.35)),
                    (int(self.width * 0.75), int(self.height * 0.25)),
                    (int(self.width * 0.65), int(self.height * 0.18)),
                    (0, int(self.height * 0.18))
                ]
            else:
                # Hero: polygon(100% 65%, 35% 65%, 25% 55%, 18% 40%, 12% 25%, 8% 15%, 4% 8%, 0% 5%, 2% 20%, 6% 35%, 12% 50%, 18% 65%, 25% 75%, 35% 82%, 100% 82%)
                points = [
                    (int(self.width * 1.0), int(self.height * 0.65)),
                    (int(self.width * 0.35), int(self.height * 0.65)),
                    (int(self.width * 0.25), int(self.height * 0.55)),
                    (int(self.width * 0.18), int(self.height * 0.40)),
                    (int(self.width * 0.12), int(self.height * 0.25)),
                    (int(self.width * 0.08), int(self.height * 0.15)),
                    (int(self.width * 0.04), int(self.height * 0.08)),
                    (int(self.width * 0.0), int(self.height * 0.05)),
                    (int(self.width * 0.02), int(self.height * 0.20)),
                    (int(self.width * 0.06), int(self.height * 0.35)),
                    (int(self.width * 0.12), int(self.height * 0.50)),
                    (int(self.width * 0.18), int(self.height * 0.65)),
                    (int(self.width * 0.25), int(self.height * 0.75)),
                    (int(self.width * 0.35), int(self.height * 0.82)),
                    (int(self.width * 1.0), int(self.height * 0.82))
                ]

            # Convert hex color to RGB
            if isinstance(self.bg_color, str) and self.bg_color.startswith('#'):
                hex_color = self.bg_color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                rgb_color = self.bg_color

            # Draw the falchion shape
            c.polygon(rgb_color, points)

            # Add subtle border
            c.polygon((80, 80, 80), points, 2)

            return r

    class FalchionFill(renpy.Displayable):
        def __init__(self, width, height, hp_percent, is_enemy=True, fill_color="#cc0000", **kwargs):
            super(FalchionFill, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.hp_percent = hp_percent
            self.is_enemy = is_enemy
            self.fill_color = fill_color

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Calculate fill width
            if self.is_enemy:
                fill_width = int(self.width * self.hp_percent)
            else:
                fill_width = int(self.width * self.hp_percent)

            if fill_width <= 0:
                return r

            # Create falchion shape points (same as background)
            if self.is_enemy:
                points = [
                    (0, int(self.height * 0.35)),
                    (int(fill_width * 0.65), int(self.height * 0.35)),
                    (int(fill_width * 0.75), int(self.height * 0.45)),
                    (int(fill_width * 0.82), int(self.height * 0.60)),
                    (int(fill_width * 0.88), int(self.height * 0.75)),
                    (int(fill_width * 0.92), int(self.height * 0.85)),
                    (int(fill_width * 0.96), int(self.height * 0.92)),
                    (int(fill_width * 1.0), int(self.height * 0.95)),
                    (int(fill_width * 0.98), int(self.height * 0.80)),
                    (int(fill_width * 0.94), int(self.height * 0.65)),
                    (int(fill_width * 0.88), int(self.height * 0.50)),
                    (int(fill_width * 0.82), int(self.height * 0.35)),
                    (int(fill_width * 0.75), int(self.height * 0.25)),
                    (int(fill_width * 0.65), int(self.height * 0.18)),
                    (0, int(self.height * 0.18))
                ]
            else:
                # For hero, we need to clip from the right side
                offset = self.width - fill_width
                points = [
                    (int(self.width), int(self.height * 0.65)),
                    (max(offset, int(self.width * 0.35)), int(self.height * 0.65)),
                    (max(offset, int(self.width * 0.25)), int(self.height * 0.55)),
                    (max(offset, int(self.width * 0.18)), int(self.height * 0.40)),
                    (max(offset, int(self.width * 0.12)), int(self.height * 0.25)),
                    (max(offset, int(self.width * 0.08)), int(self.height * 0.15)),
                    (max(offset, int(self.width * 0.04)), int(self.height * 0.08)),
                    (max(offset, int(self.width * 0.0)), int(self.height * 0.05)),
                    (max(offset, int(self.width * 0.02)), int(self.height * 0.20)),
                    (max(offset, int(self.width * 0.06)), int(self.height * 0.35)),
                    (max(offset, int(self.width * 0.12)), int(self.height * 0.50)),
                    (max(offset, int(self.width * 0.18)), int(self.height * 0.65)),
                    (max(offset, int(self.width * 0.25)), int(self.height * 0.75)),
                    (max(offset, int(self.width * 0.35)), int(self.height * 0.82)),
                    (int(self.width), int(self.height * 0.82))
                ]

            # Convert hex color to RGB
            if isinstance(self.fill_color, str) and self.fill_color.startswith('#'):
                hex_color = self.fill_color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                rgb_color = self.fill_color

            # Draw the filled falchion shape
            c.polygon(rgb_color, points)

            return r

    class WaveEffect(renpy.Displayable):
        def __init__(self, width=180, height=80, **kwargs):
            super(WaveEffect, self).__init__(**kwargs)
            self.width = width
            self.height = height

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create a gradient wave effect using multiple rectangles
            for i in range(self.width):
                x_ratio = float(i) / self.width
                # Create wave intensity based on position (bell curve-like)
                if x_ratio < 0.15:
                    alpha = int(255 * (x_ratio / 0.15) * 0.1)
                elif x_ratio < 0.3:
                    alpha = int(255 * 0.3)
                elif x_ratio < 0.45:
                    alpha = int(255 * 0.7)
                elif x_ratio < 0.55:
                    alpha = int(255 * 0.9)  # Peak
                elif x_ratio < 0.7:
                    alpha = int(255 * 0.7)
                elif x_ratio < 0.85:
                    alpha = int(255 * 0.3)
                else:
                    alpha = int(255 * ((1.0 - x_ratio) / 0.15) * 0.1)

                color = (255, 255, 255, alpha)
                c.rect(color, (i, 0, 1, self.height))

            return r

    def get_orb_positions(num_orbs, radius=ROUND_RADIUS, orb_radius=ORB_RADIUS):
        """Returns orb positions arranged evenly in a circle around radius."""
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = radius + radius * math.cos(angle) - orb_radius
            y = radius + radius * math.sin(angle) - orb_radius
            positions.append((int(x), int(y)))
        return positions

    def format_hp_percent(hp_value):
        """Format HP as percentage for display."""
        return str(int(hp_value * 100)) + "%"

    def get_hp_fill_color(hp_percent, is_enemy=True):
        """Get HP fill color based on health level."""
        if is_enemy:
            if hp_percent <= 0.15:
                return "#ff4444"
            elif hp_percent <= 0.30:
                return "#cc0000"
            else:
                return "#cc0000"
        else:
            if hp_percent <= 0.15:
                return "#4499ff"
            elif hp_percent <= 0.30:
                return "#003399"
            else:
                return "#003399"

    def get_wave_speed(hp_percent):
        """Get wave animation speed based on HP (faster when low)."""
        return max(0.8, 3.0 * hp_percent)

# ========================
# Circle and Shape Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# VS Circle with gradient effect
define vs_circle_bg = Circle(40, (255, 204, 0), (184, 134, 11), 4)

# ========================
# HP Bar Screens
# ========================
screen hp_bar_enemy():
    fixed:
        xpos 50
        ypos 150
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background falchion shape
        add FalchionBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True, "#1a1a1a")

        # HP Fill with proper health state
        $ fill_color = get_hp_fill_color(enemy_hp, True)
        if enemy_hp <= 0.15:
            add FalchionFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True, fill_color) at critical_hp_flash
        elif enemy_hp <= 0.30:
            add FalchionFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True, fill_color) at low_hp_pulse
        else:
            add FalchionFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True, fill_color)

        # Wave effect (only show if HP > 0)
        if enemy_hp > 0:
            $ wave_speed = get_wave_speed(enemy_hp)
            add WaveEffect(180, HP_BAR_HEIGHT) at hp_wave_enemy(wave_speed)

        # HP Text positioned above the bar
        $ hp_text = format_hp_percent(enemy_hp)
        if enemy_hp <= 0.15:
            text "[hp_text]" color "#ff6666" size 28 bold True at critical_hp_text:
                xpos HP_BAR_WIDTH - 70
                ypos -50
                outlines [(3, "#000000", 0, 0)]
        elif enemy_hp <= 0.30:
            text "[hp_text]" color "#ff6666" size 28 bold True at low_hp_text:
                xpos HP_BAR_WIDTH - 70
                ypos -50
                outlines [(3, "#000000", 0, 0)]
        else:
            text "[hp_text]" color "#ff6666" size 28 bold True:
                xpos HP_BAR_WIDTH - 70
                ypos -50
                outlines [(3, "#000000", 0, 0)]

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 50
        ypos 150
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background falchion shape
        add FalchionBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, False, "#1a1a1a")

        # HP Fill with proper health state
        $ fill_color = get_hp_fill_color(hero_hp, False)
        if hero_hp <= 0.15:
            add FalchionFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False, fill_color) at critical_hp_flash
        elif hero_hp <= 0.30:
            add FalchionFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False, fill_color) at low_hp_pulse
        else:
            add FalchionFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False, fill_color)

        # Wave effect (only show if HP > 0)
        if hero_hp > 0:
            $ wave_speed = get_wave_speed(hero_hp)
            add WaveEffect(180, HP_BAR_HEIGHT) at hp_wave_hero(wave_speed)

        # HP Text positioned below the bar
        $ hp_text = format_hp_percent(hero_hp)
        if hero_hp <= 0.15:
            text "[hp_text]" color "#66aaff" size 28 bold True at critical_hp_text:
                xpos 70
                ypos HP_BAR_HEIGHT + 25
                outlines [(3, "#000000", 0, 0)]
        elif hero_hp <= 0.30:
            text "[hp_text]" color "#66aaff" size 28 bold True at low_hp_text:
                xpos 70
                ypos HP_BAR_HEIGHT + 25
                outlines [(3, "#000000", 0, 0)]
        else:
            text "[hp_text]" color "#66aaff" size 28 bold True:
                xpos 70
                ypos HP_BAR_HEIGHT + 25
                outlines [(3, "#000000", 0, 0)]

# ========================
# Round Circle (replacing VS)
# ========================
screen round_circle():
    fixed:
        xalign 0.5
        yalign 0.35
        xsize ROUND_RADIUS * 2
        ysize ROUND_RADIUS * 2

        # Round circle background with glow
        add vs_circle_bg at vs_glow

        # Round text
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 2

            text "Round":
                size 16
                color "#000000"
                xalign 0.5
                outlines [(1, "#ffffff", 0, 0)]
                bold True

            text "[current_round]":
                size 32
                color "#000000"
                xalign 0.5
                outlines [(1, "#ffffff", 0, 0)]
                bold True

        # AP Orbs around the circle
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            if i < available_ap:
                add orb_active at orb_glow xpos x ypos y
            else:
                add orb_inactive_img at orb_inactive xpos x ypos y

# ========================
# Main Battle UI Screen
# ========================
screen battle_ui():
    modal False

    # Dark gradient background for better visual appeal
    add Solid("#000000")

    use hp_bar_enemy
    use hp_bar_hero
    use round_circle

# ========================
# Combat Functions
# ========================
init python:
    def damage_enemy(amount):
        global enemy_hp
        enemy_hp = max(0.0, enemy_hp - amount)

    def damage_hero(amount):
        global hero_hp
        hero_hp = max(0.0, hero_hp - amount)

    def heal_enemy(amount):
        global enemy_hp
        enemy_hp = min(enemy_max_hp, enemy_hp + amount)

    def heal_hero(amount):
        global hero_hp
        hero_hp = min(hero_max_hp, hero_hp + amount)

    def next_round():
        global current_round, available_ap
        current_round += 1
        available_ap = max_ap

    def spend_ap():
        global available_ap
        if available_ap > 0:
            available_ap -= 1

# ========================
# Demo Label
# ========================
label start:
    show screen battle_ui

    $ enemy_hp_display = format_hp_percent(enemy_hp)
    $ hero_hp_display = format_hp_percent(hero_hp)

    "Falchion Battle UI - Round [current_round], AP [available_ap]/[max_ap]"
    "Enemy HP: [enemy_hp_display] | Hero HP: [hero_hp_display]"

    menu:
        "Attack Enemy" if available_ap > 0:
            $ spend_ap()
            $ damage_enemy(0.15)
            "You strike the enemy with your falchion!"
            jump start

        "Enemy Attack" if available_ap > 0:
            $ spend_ap()
            $ damage_hero(0.12)
            "The enemy's blade finds its mark!"
            jump start

        "Heal Hero":
            $ heal_hero(0.15)
            "You recover some health!"
            jump start

        "Heal Enemy":
            $ heal_enemy(0.10)
            "Enemy recovers slightly."
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            "Action point restored!"
            jump start

        "Next Round":
            $ next_round()
            "A new round begins!"
            jump start

        "Reset Battle":
            $ enemy_hp = 0.75
            $ hero_hp = 0.50
            $ current_round = 18
            $ available_ap = 4
            "Battle reset!"
            jump start

        "Exit":
            "Thanks for testing the Falchion HP system!"
            return
