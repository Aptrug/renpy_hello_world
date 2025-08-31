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

# HP Bar Constants - Made much thicker and more prominent
define HP_BAR_WIDTH = 450
define HP_BAR_HEIGHT = 120

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
    alpha 0.0
    xpos -220
    pause 0.5
    linear wave_speed xpos HP_BAR_WIDTH + 50 alpha 0.8
    alpha 0.0
    repeat

transform hp_wave_hero(wave_speed=3.0):
    alpha 0.0
    xpos HP_BAR_WIDTH + 220
    pause 0.5
    linear wave_speed xpos -50 alpha 0.8
    alpha 0.0
    repeat

# Health state animations
transform low_hp_pulse:
    ease 1.5 alpha 0.8 additive 0.2
    ease 1.5 alpha 1.0 additive 0.0
    repeat

transform critical_hp_flash:
    ease 0.6 alpha 0.7 additive 0.5
    ease 0.6 alpha 1.0 additive 0.0
    repeat

transform critical_hp_text:
    ease 0.8 zoom 1.0 alpha 0.9
    ease 0.8 zoom 1.15 alpha 1.0
    repeat

transform low_hp_text:
    ease 1.2 zoom 1.0
    ease 1.2 zoom 1.08
    repeat

# VS Circle glow
transform vs_glow:
    parallel:
        ease 2.0 alpha 0.8 additive 0.3
        ease 2.0 alpha 1.0 additive 0.0
    parallel:
        ease 2.0 zoom 1.0
        ease 2.0 zoom 1.08
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

            # Create much more dramatic falchion blade shape points
            if self.is_enemy:
                # Enemy falchion with more pronounced curve and longer blade tip
                points = [
                    (0, int(self.height * 0.25)),                     # Top left start
                    (int(self.width * 0.55), int(self.height * 0.25)), # Main blade top
                    (int(self.width * 0.65), int(self.height * 0.30)), # Start curve
                    (int(self.width * 0.72), int(self.height * 0.38)), # Curve progression
                    (int(self.width * 0.78), int(self.height * 0.45)), # Mid curve
                    (int(self.width * 0.83), int(self.height * 0.48)), # Tip approach top
                    (int(self.width * 0.88), int(self.height * 0.49)), # Near tip
                    (int(self.width * 0.95), int(self.height * 0.495)), # Very near tip
                    (int(self.width), int(self.height * 0.5)),         # Sharp tip point
                    (int(self.width * 0.95), int(self.height * 0.505)), # Very near tip bottom
                    (int(self.width * 0.88), int(self.height * 0.51)), # Near tip bottom
                    (int(self.width * 0.83), int(self.height * 0.52)), # Tip approach bottom
                    (int(self.width * 0.78), int(self.height * 0.55)), # Mid curve bottom
                    (int(self.width * 0.72), int(self.height * 0.62)), # Curve progression bottom
                    (int(self.width * 0.65), int(self.height * 0.70)), # End curve
                    (int(self.width * 0.55), int(self.height * 0.75)), # Main blade bottom
                    (0, int(self.height * 0.75))                      # Bottom left end
                ]
            else:
                # Hero falchion with dramatic left-pointing blade
                points = [
                    (int(self.width), int(self.height * 0.25)),        # Top right start
                    (int(self.width * 0.45), int(self.height * 0.25)), # Main blade top
                    (int(self.width * 0.35), int(self.height * 0.30)), # Start curve
                    (int(self.width * 0.28), int(self.height * 0.38)), # Curve progression
                    (int(self.width * 0.22), int(self.height * 0.45)), # Mid curve
                    (int(self.width * 0.17), int(self.height * 0.48)), # Tip approach top
                    (int(self.width * 0.12), int(self.height * 0.49)), # Near tip
                    (int(self.width * 0.05), int(self.height * 0.495)), # Very near tip
                    (0, int(self.height * 0.5)),                       # Sharp tip point
                    (int(self.width * 0.05), int(self.height * 0.505)), # Very near tip bottom
                    (int(self.width * 0.12), int(self.height * 0.51)), # Near tip bottom
                    (int(self.width * 0.17), int(self.height * 0.52)), # Tip approach bottom
                    (int(self.width * 0.22), int(self.height * 0.55)), # Mid curve bottom
                    (int(self.width * 0.28), int(self.height * 0.62)), # Curve progression bottom
                    (int(self.width * 0.35), int(self.height * 0.70)), # End curve
                    (int(self.width * 0.45), int(self.height * 0.75)), # Main blade bottom
                    (int(self.width), int(self.height * 0.75))         # Bottom right end
                ]

            # Convert hex color to RGB
            if isinstance(self.bg_color, str) and self.bg_color.startswith('#'):
                hex_color = self.bg_color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                rgb_color = self.bg_color

            # Draw the falchion shape with dark gradient effect
            c.polygon((26, 26, 26), points)  # Darker base

            # Add inner shadow effect
            inner_points = [(x-2 if i % 2 == 0 else x+2, y+1) for i, (x, y) in enumerate(points)]
            c.polygon((13, 13, 13), inner_points)

            # Add border
            c.polygon((120, 120, 120), points, 3)

            return r

    class FalchionFill(renpy.Displayable):
        def __init__(self, width, height, hp_percent, is_enemy=True, fill_color="#cc0000", **kwargs):
            super(FalchionFill, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.hp_percent = max(0.0, min(1.0, hp_percent))
            self.is_enemy = is_enemy
            self.fill_color = fill_color

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)

            if self.hp_percent <= 0:
                return r

            c = r.canvas()

            # Create clipping mask based on HP percentage
            if self.is_enemy:
                # Enemy fills from left to right
                fill_width = self.width * self.hp_percent
                points = [
                    (0, int(self.height * 0.25)),
                    (min(fill_width, int(self.width * 0.55)), int(self.height * 0.25)),
                    (min(fill_width, int(self.width * 0.65)), int(self.height * 0.30)),
                    (min(fill_width, int(self.width * 0.72)), int(self.height * 0.38)),
                    (min(fill_width, int(self.width * 0.78)), int(self.height * 0.45)),
                    (min(fill_width, int(self.width * 0.83)), int(self.height * 0.48)),
                    (min(fill_width, int(self.width * 0.88)), int(self.height * 0.49)),
                    (min(fill_width, int(self.width * 0.95)), int(self.height * 0.495)),
                    (min(fill_width, int(self.width)), int(self.height * 0.5)),
                    (min(fill_width, int(self.width * 0.95)), int(self.height * 0.505)),
                    (min(fill_width, int(self.width * 0.88)), int(self.height * 0.51)),
                    (min(fill_width, int(self.width * 0.83)), int(self.height * 0.52)),
                    (min(fill_width, int(self.width * 0.78)), int(self.height * 0.55)),
                    (min(fill_width, int(self.width * 0.72)), int(self.height * 0.62)),
                    (min(fill_width, int(self.width * 0.65)), int(self.height * 0.70)),
                    (min(fill_width, int(self.width * 0.55)), int(self.height * 0.75)),
                    (0, int(self.height * 0.75))
                ]

                # Ensure we don't go beyond the actual fill width
                points = [(min(x, fill_width), y) for x, y in points]

            else:
                # Hero fills from right to left
                fill_width = self.width * self.hp_percent
                start_x = self.width - fill_width

                points = [
                    (int(self.width), int(self.height * 0.25)),
                    (max(start_x, int(self.width * 0.45)), int(self.height * 0.25)),
                    (max(start_x, int(self.width * 0.35)), int(self.height * 0.30)),
                    (max(start_x, int(self.width * 0.28)), int(self.height * 0.38)),
                    (max(start_x, int(self.width * 0.22)), int(self.height * 0.45)),
                    (max(start_x, int(self.width * 0.17)), int(self.height * 0.48)),
                    (max(start_x, int(self.width * 0.12)), int(self.height * 0.49)),
                    (max(start_x, int(self.width * 0.05)), int(self.height * 0.495)),
                    (max(start_x, 0), int(self.height * 0.5)),
                    (max(start_x, int(self.width * 0.05)), int(self.height * 0.505)),
                    (max(start_x, int(self.width * 0.12)), int(self.height * 0.51)),
                    (max(start_x, int(self.width * 0.17)), int(self.height * 0.52)),
                    (max(start_x, int(self.width * 0.22)), int(self.height * 0.55)),
                    (max(start_x, int(self.width * 0.28)), int(self.height * 0.62)),
                    (max(start_x, int(self.width * 0.35)), int(self.height * 0.70)),
                    (max(start_x, int(self.width * 0.45)), int(self.height * 0.75)),
                    (int(self.width), int(self.height * 0.75))
                ]

            # Convert hex color to RGB
            if isinstance(self.fill_color, str) and self.fill_color.startswith('#'):
                hex_color = self.fill_color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                rgb_color = self.fill_color

            # Draw gradient fill effect
            # Base color
            c.polygon(rgb_color, points)

            # Add highlight gradient on top portion
            highlight_points = points[:len(points)//2]
            highlight_color = tuple(min(255, int(c * 1.3)) for c in rgb_color)
            c.polygon(highlight_color, highlight_points)

            # Add subtle inner glow
            inner_points = [(x-1, y-1) for x, y in points]
            glow_color = tuple(min(255, int(c * 1.5)) for c in rgb_color)
            c.polygon(glow_color, inner_points, 2)

            return r

    class WaveEffect(renpy.Displayable):
        def __init__(self, width=220, height=120, **kwargs):
            super(WaveEffect, self).__init__(**kwargs)
            self.width = width
            self.height = height

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create a more dramatic wave gradient
            segments = 40
            for i in range(segments):
                x = int((float(i) / segments) * self.width)
                x_ratio = float(i) / segments

                # Create smooth wave intensity (bell curve)
                if x_ratio < 0.1:
                    intensity = x_ratio * 10 * 0.15
                elif x_ratio < 0.25:
                    intensity = 0.15 + (x_ratio - 0.1) / 0.15 * 0.25
                elif x_ratio < 0.4:
                    intensity = 0.4 + (x_ratio - 0.25) / 0.15 * 0.35
                elif x_ratio < 0.5:
                    intensity = 0.75 + (x_ratio - 0.4) / 0.1 * 0.25  # Peak
                elif x_ratio < 0.6:
                    intensity = 1.0 - (x_ratio - 0.5) / 0.1 * 0.25
                elif x_ratio < 0.75:
                    intensity = 0.75 - (x_ratio - 0.6) / 0.15 * 0.35
                elif x_ratio < 0.9:
                    intensity = 0.4 - (x_ratio - 0.75) / 0.15 * 0.25
                else:
                    intensity = 0.15 - (x_ratio - 0.9) / 0.1 * 0.15

                alpha = max(0, min(255, int(255 * intensity)))
                segment_width = max(1, self.width // segments)

                # Use white with alpha for screen blend mode effect
                color = (255, 255, 255, alpha)
                c.rect(color, (x, 0, segment_width, self.height))

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
                return "#ff6666"  # Bright red for critical
            elif hp_percent <= 0.30:
                return "#ff4444"  # Medium red for low
            else:
                return "#cc0000"  # Dark red for normal
        else:
            if hp_percent <= 0.15:
                return "#66aaff"  # Bright blue for critical
            elif hp_percent <= 0.30:
                return "#4499ff"  # Medium blue for low
            else:
                return "#003399"  # Dark blue for normal

    def get_wave_speed(hp_percent):
        """Get wave animation speed based on HP (faster when low)."""
        return max(1.2, 3.5 * hp_percent)

# ========================
# Circle and Shape Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# Round Circle with gradient effect
define round_circle_bg = Circle(50, (255, 204, 0), (184, 134, 11), 4)

# ========================
# HP Bar Screens
# ========================
screen hp_bar_enemy():
    fixed:
        xpos 80
        ypos 100
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

        # Wave effect (only show if HP > 0) - more prominent
        if enemy_hp > 0:
            $ wave_speed = get_wave_speed(enemy_hp)
            add WaveEffect(220, HP_BAR_HEIGHT) at hp_wave_enemy(wave_speed)

        # HP Text positioned above the bar
        $ hp_text = format_hp_percent(enemy_hp)
        if enemy_hp <= 0.15:
            text "[hp_text]" color "#ff6666" size 32 bold True at critical_hp_text:
                xpos HP_BAR_WIDTH - 90
                ypos -60
                outlines [(3, "#000000", 0, 0)]
        elif enemy_hp <= 0.30:
            text "[hp_text]" color "#ff6666" size 32 bold True at low_hp_text:
                xpos HP_BAR_WIDTH - 90
                ypos -60
                outlines [(3, "#000000", 0, 0)]
        else:
            text "[hp_text]" color "#ff6666" size 32 bold True:
                xpos HP_BAR_WIDTH - 90
                ypos -60
                outlines [(3, "#000000", 0, 0)]

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 80
        ypos 100
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

        # Wave effect (only show if HP > 0) - more prominent
        if hero_hp > 0:
            $ wave_speed = get_wave_speed(hero_hp)
            add WaveEffect(220, HP_BAR_HEIGHT) at hp_wave_hero(wave_speed)

        # HP Text positioned below the bar
        $ hp_text = format_hp_percent(hero_hp)
        if hero_hp <= 0.15:
            text "[hp_text]" color "#66aaff" size 32 bold True at critical_hp_text:
                xpos 90
                ypos HP_BAR_HEIGHT + 30
                outlines [(3, "#000000", 0, 0)]
        elif hero_hp <= 0.30:
            text "[hp_text]" color "#66aaff" size 32 bold True at low_hp_text:
                xpos 90
                ypos HP_BAR_HEIGHT + 30
                outlines [(3, "#000000", 0, 0)]
        else:
            text "[hp_text]" color "#66aaff" size 32 bold True:
                xpos 90
                ypos HP_BAR_HEIGHT + 30
                outlines [(3, "#000000", 0, 0)]

# ========================
# Round Circle (center of screen)
# ========================
screen round_circle():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize ROUND_RADIUS * 2
        ysize ROUND_RADIUS * 2

        # Round circle background with glow
        add round_circle_bg at vs_glow:
            xalign 0.5
            yalign 0.5

        # Round text
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 2

            text "Round":
                size 20
                color "#000000"
                xalign 0.5
                outlines [(2, "#ffffff", 0, 0)]
                bold True

            text "[current_round]":
                size 36
                color "#000000"
                xalign 0.5
                outlines [(2, "#ffffff", 0, 0)]
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

    # Rich dark gradient background
    add "#000000"

    # Add subtle radial gradient effect
    add Solid("#111111") alpha 0.3:
        xalign 0.5
        yalign 0.5

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
