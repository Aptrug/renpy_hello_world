# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

# HP System Variables
default player_hp = 100
default player_max_hp = 100
default enemy_hp = 75
default enemy_max_hp = 100

define ROUND_RADIUS = 70
define ORB_RADIUS = 15

# HP Bar dimensions
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
        linear 0.1 additive 0.3
        linear 0.1 additive 0.0
    repeat

transform round_breathe:
    ease 3.0 zoom 1.05
    ease 3.0 zoom 1.0
    repeat

transform orb_inactive:
    alpha 0.4
    zoom 0.9

# HP Bar Transforms
transform hp_bar_appear:
    alpha 0.0 yoffset 20
    ease 0.5 alpha 1.0 yoffset 0

transform hp_fill_transition:
    linear 0.8 alpha 1.0

transform low_hp_pulse:
    ease 1.5 additive 0.4
    ease 1.5 additive 0.0
    repeat

transform critical_hp_flash:
    ease 0.6 additive 0.6
    ease 0.6 additive 0.0
    repeat

transform hp_wave_enemy:
    xoffset -180 alpha 0.0
    linear 3.0 xoffset 400 alpha 1.0
    repeat

transform hp_wave_hero:
    xoffset 400 alpha 0.0
    linear 3.0 xoffset -180 alpha 1.0
    repeat

# ========================
# Python Helpers
# ========================
init python:
    import math

    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super().__init__(**kwargs)
            self.radius, self.color = radius, color
            self.border_color, self.border_width = border_color, border_width

        def render(self, w, h, st, at):
            size = self.radius * 2
            r = renpy.Render(size, size)
            c = r.canvas()

            if self.color:
                c.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                c.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return r

    class FalchionHPBar(renpy.Displayable):
        def __init__(self, width, height, is_enemy=False, **kwargs):
            super().__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create falchion shape path
            if self.is_enemy:
                # Enemy falchion (pointing right)
                points = [
                    (0, self.height * 0.35),
                    (self.width * 0.65, self.height * 0.35),
                    (self.width * 0.75, self.height * 0.45),
                    (self.width * 0.82, self.height * 0.60),
                    (self.width * 0.88, self.height * 0.75),
                    (self.width * 0.92, self.height * 0.85),
                    (self.width * 0.96, self.height * 0.92),
                    (self.width, self.height * 0.95),
                    (self.width * 0.98, self.height * 0.80),
                    (self.width * 0.94, self.height * 0.65),
                    (self.width * 0.88, self.height * 0.50),
                    (self.width * 0.82, self.height * 0.35),
                    (self.width * 0.75, self.height * 0.25),
                    (self.width * 0.65, self.height * 0.18),
                    (0, self.height * 0.18)
                ]
            else:
                # Hero falchion (pointing left)
                points = [
                    (self.width, self.height * 0.65),
                    (self.width * 0.35, self.height * 0.65),
                    (self.width * 0.25, self.height * 0.55),
                    (self.width * 0.18, self.height * 0.40),
                    (self.width * 0.12, self.height * 0.25),
                    (self.width * 0.08, self.height * 0.15),
                    (self.width * 0.04, self.height * 0.08),
                    (0, self.height * 0.05),
                    (self.width * 0.02, self.height * 0.20),
                    (self.width * 0.06, self.height * 0.35),
                    (self.width * 0.12, self.height * 0.50),
                    (self.width * 0.18, self.height * 0.65),
                    (self.width * 0.25, self.height * 0.75),
                    (self.width * 0.35, self.height * 0.82),
                    (self.width, self.height * 0.82)
                ]

            # Draw background shape
            c.polygon((26, 26, 26), points)
            c.polygon((255, 255, 255, 38), points, 2)  # Border

            return r

    class HPWave(renpy.Displayable):
        def __init__(self, width, height, **kwargs):
            super().__init__(**kwargs)
            self.width = width
            self.height = height

        def render(self, w, h, st, at):
            r = renpy.Render(180, self.height)
            c = r.canvas()

            # Create wave gradient effect
            for i in range(180):
                alpha_val = int(255 * (0.5 + 0.5 * math.sin(i * math.pi / 90)))
                c.rect((255, 255, 255, alpha_val // 3), (i, 0, 1, self.height))

            return r

    def get_orb_positions(num_orbs):
        """
        Returns orb positions arranged evenly in a circle around ROUND_RADIUS.
        Offsets by ORB_RADIUS so they align properly.
        """
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = ROUND_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
            y = ROUND_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

    def get_hp_percentage(current, maximum):
        return float(current) / float(maximum) if maximum > 0 else 0.0

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# HP Bar Components
define falchion_enemy_bg = FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)
define falchion_hero_bg = FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, False)
define hp_wave = HPWave(180, HP_BAR_HEIGHT)

# ========================
# Battle UI Screen
# ========================
screen battle_ui():
    # Background with effects
    add Solid("#000000")

    fixed:
        xalign 0.5
        yalign 0.5

        # Enemy HP Bar (Left side)
        fixed:
            xpos 50
            ypos 200

            # HP Value display (above bar for enemy)
            text "[enemy_hp]%":
                xpos 0
                ypos -60
                size 18
                color "#ff6666"
                outlines [(1, "#000000", 0, 0)]
                at (low_hp_pulse if get_hp_percentage(enemy_hp, enemy_max_hp) <= 0.3 else None)

            # Falchion background
            add falchion_enemy_bg at hp_bar_appear

            # HP Fill with clipping
            fixed:
                # This creates the HP fill effect
                bar:
                    value AnimatedValue(enemy_hp, enemy_max_hp, delay=0.8)
                    xsize HP_BAR_WIDTH * get_hp_percentage(enemy_hp, enemy_max_hp)
                    ysize HP_BAR_HEIGHT
                    left_bar Solid("#cc0000")
                    right_bar Solid("#ff6666")
                    at (critical_hp_flash if get_hp_percentage(enemy_hp, enemy_max_hp) <= 0.15
                        else low_hp_pulse if get_hp_percentage(enemy_hp, enemy_max_hp) <= 0.3
                        else hp_fill_transition)

                # Animated wave effect
                if get_hp_percentage(enemy_hp, enemy_max_hp) > 0:
                    add hp_wave at hp_wave_enemy

        # Round Circle (Center)
        fixed:
            xalign 0.5
            yalign 0.5
            xsize ROUND_RADIUS*2
            ysize ROUND_RADIUS*2

            # Round circle background with breathing animation
            add round_bg at round_breathe

            # Round number in the center
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 2

                text "Round":
                    size 22
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

                text "[current_round]":
                    size 56
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

            # Orbs arranged around the circle
            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                add (orb_active if i < available_ap else orb_inactive_img) at (orb_glow if i < available_ap else orb_inactive) xpos x ypos y

        # Hero HP Bar (Right side)
        fixed:
            xpos config.screen_width - 50 - HP_BAR_WIDTH
            ypos 200

            # Falchion background
            add falchion_hero_bg at hp_bar_appear

            # HP Fill with clipping
            fixed:
                # This creates the HP fill effect
                bar:
                    value AnimatedValue(player_hp, player_max_hp, delay=0.8)
                    xsize HP_BAR_WIDTH * get_hp_percentage(player_hp, player_max_hp)
                    ysize HP_BAR_HEIGHT
                    left_bar Solid("#003399")
                    right_bar Solid("#4499ff")
                    at (critical_hp_flash if get_hp_percentage(player_hp, player_max_hp) <= 0.15
                        else low_hp_pulse if get_hp_percentage(player_hp, player_max_hp) <= 0.3
                        else hp_fill_transition)

                # Animated wave effect
                if get_hp_percentage(player_hp, player_max_hp) > 0:
                    add hp_wave at hp_wave_hero

            # HP Value display (below bar for hero)
            text "[player_hp]%":
                xpos HP_BAR_WIDTH - 60
                ypos HP_BAR_HEIGHT + 20
                size 18
                color "#66aaff"
                outlines [(1, "#000000", 0, 0)]
                at (low_hp_pulse if get_hp_percentage(player_hp, player_max_hp) <= 0.3 else None)

# ========================
# Alternative Round-only UI Screen
# ========================
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.75
        xsize ROUND_RADIUS*2
        ysize ROUND_RADIUS*2

        # Round circle background with breathing animation
        add round_bg at round_breathe

        # Round number in the center
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 2

            text "Round":
                size 22
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 56
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

        # Orbs arranged around the circle
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            add (orb_active if i < available_ap else orb_inactive_img) at (orb_glow if i < available_ap else orb_inactive) xpos x ypos y

# ========================
# Demo Label
# ========================
label start:
    show screen battle_ui

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap]"
    "Player HP: [player_hp]/[player_max_hp] | Enemy HP: [enemy_hp]/[enemy_max_hp]"

    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start

        "Damage Player":
            $ player_hp = max(0, player_hp - renpy.random.randint(10, 25))
            jump start

        "Damage Enemy":
            $ enemy_hp = max(0, enemy_hp - renpy.random.randint(10, 25))
            jump start

        "Heal Player":
            $ player_hp = min(player_max_hp, player_hp + renpy.random.randint(15, 30))
            jump start

        "Heal Enemy":
            $ enemy_hp = min(enemy_max_hp, enemy_hp + renpy.random.randint(15, 30))
            jump start

        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start

        "Reset HP":
            $ player_hp = player_max_hp
            $ enemy_hp = enemy_max_hp
            jump start

        "Switch to Round UI only":
            hide screen battle_ui
            show screen round_ui
            jump start

        "Switch to Battle UI":
            hide screen round_ui
            show screen battle_ui
            jump start

        "Exit":
            return

# ========================
# Enhanced HP Bar with Improved Clipping
# ========================
init python:
    class AdvancedFalchionBar(renpy.Displayable):
        def __init__(self, width, height, is_enemy=False, current_hp=100, max_hp=100, **kwargs):
            super().__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy
            self.current_hp = current_hp
            self.max_hp = max_hp

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            hp_percentage = float(self.current_hp) / float(self.max_hp) if self.max_hp > 0 else 0.0

            # Background shape
            if self.is_enemy:
                # Enemy falchion shape
                bg_points = [
                    (0, self.height * 0.35), (self.width * 0.65, self.height * 0.35),
                    (self.width * 0.75, self.height * 0.45), (self.width * 0.82, self.height * 0.60),
                    (self.width * 0.88, self.height * 0.75), (self.width * 0.92, self.height * 0.85),
                    (self.width * 0.96, self.height * 0.92), (self.width, self.height * 0.95),
                    (self.width * 0.98, self.height * 0.80), (self.width * 0.94, self.height * 0.65),
                    (self.width * 0.88, self.height * 0.50), (self.width * 0.82, self.height * 0.35),
                    (self.width * 0.75, self.height * 0.25), (self.width * 0.65, self.height * 0.18),
                    (0, self.height * 0.18)
                ]
                fill_color = (204, 0, 0) if hp_percentage > 0.3 else (255, 68, 68)
            else:
                # Hero falchion shape
                bg_points = [
                    (self.width, self.height * 0.65), (self.width * 0.35, self.height * 0.65),
                    (self.width * 0.25, self.height * 0.55), (self.width * 0.18, self.height * 0.40),
                    (self.width * 0.12, self.height * 0.25), (self.width * 0.08, self.height * 0.15),
                    (self.width * 0.04, self.height * 0.08), (0, self.height * 0.05),
                    (self.width * 0.02, self.height * 0.20), (self.width * 0.06, self.height * 0.35),
                    (self.width * 0.12, self.height * 0.50), (self.width * 0.18, self.height * 0.65),
                    (self.width * 0.25, self.height * 0.75), (self.width * 0.35, self.height * 0.82),
                    (self.width, self.height * 0.82)
                ]
                fill_color = (0, 51, 153) if hp_percentage > 0.3 else (68, 153, 255)

            # Draw background
            c.polygon((26, 26, 26), bg_points)

            # Draw HP fill (clipped to percentage)
            if hp_percentage > 0:
                fill_width = self.width * hp_percentage

                if self.is_enemy:
                    # Fill from left for enemy
                    fill_points = [(x, y) for x, y in bg_points if x <= fill_width]
                    if fill_points:
                        c.polygon(fill_color, fill_points)
                else:
                    # Fill from right for hero
                    offset = self.width * (1 - hp_percentage)
                    fill_points = [(x - offset, y) for x, y in bg_points if x >= offset]
                    if fill_points:
                        c.polygon(fill_color, fill_points)

            # Border
            c.polygon((255, 255, 255, 38), bg_points, 2)

            return r

# ========================
# Alternative Enhanced Battle Screen
# ========================
screen enhanced_battle_ui():
    add Solid("#000000")

    fixed:
        xalign 0.5
        yalign 0.5

        # Enemy HP (Left)
        fixed:
            xpos 50
            ypos 150

            text "Enemy: [enemy_hp]/[enemy_max_hp]":
                xpos 0
                ypos -40
                size 16
                color "#ff6666"

            add AdvancedFalchionBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True, enemy_hp, enemy_max_hp) at hp_bar_appear

        # Round Circle (Center) - keeping your existing implementation
        fixed:
            xalign 0.5
            yalign 0.5
            xsize ROUND_RADIUS*2
            ysize ROUND_RADIUS*2

            add round_bg at round_breathe

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 2

                text "Round":
                    size 22
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

                text "[current_round]":
                    size 56
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                add (orb_active if i < available_ap else orb_inactive_img) at (orb_glow if i < available_ap else orb_inactive) xpos x ypos y

        # Hero HP (Right)
        fixed:
            xpos config.screen_width - 50 - HP_BAR_WIDTH
            ypos 150

            add AdvancedFalchionBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, False, player_hp, player_max_hp) at hp_bar_appear

            text "Hero: [player_hp]/[player_max_hp]":
                xpos HP_BAR_WIDTH - 120
                ypos HP_BAR_HEIGHT + 20
                size 16
                color "#66aaff"
