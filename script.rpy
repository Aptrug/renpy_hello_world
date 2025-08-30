# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

# HP Variables
default enemy_hp = 0.75
default hero_hp = 0.50
default enemy_max_hp = 100
default hero_max_hp = 100

define ROUND_RADIUS = 40  # Smaller since it's not the main focus
define ORB_RADIUS = 8
define HP_BAR_WIDTH = 300
define HP_BAR_HEIGHT = 60

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

transform hp_wave:
    alpha 0.0
    linear 0.1 alpha 1.0
    linear 2.8 alpha 1.0
    linear 0.1 alpha 0.0
    repeat

transform low_hp_pulse:
    ease 0.75 alpha 1.0
    ease 0.75 alpha 0.6
    repeat

transform critical_hp_flash:
    ease 0.3 alpha 1.0
    ease 0.3 alpha 0.7
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
        def __init__(self, width, height, is_enemy=True, **kwargs):
            super().__init__(**kwargs)
            self.width, self.height = width, height
            self.is_enemy = is_enemy

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create falchion shape points
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

            # Draw background
            c.polygon((26, 26, 26), points)

            # Draw border
            for i in range(len(points)):
                start = points[i]
                end = points[(i + 1) % len(points)]
                c.line((255, 255, 255, 40), start, end, 2)

            return r

    class FalchionHPFill(renpy.Displayable):
        def __init__(self, width, height, hp_percent, is_enemy=True, **kwargs):
            super().__init__(**kwargs)
            self.width, self.height = width, height
            self.hp_percent = hp_percent
            self.is_enemy = is_enemy

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Calculate fill width
            fill_width = self.width * self.hp_percent

            # Create falchion shape points for fill
            if self.is_enemy:
                # Enemy falchion fill
                points = [
                    (0, self.height * 0.35),
                    (min(fill_width, self.width * 0.65), self.height * 0.35),
                ]
                if fill_width > self.width * 0.65:
                    ratio = min(1.0, (fill_width - self.width * 0.65) / (self.width * 0.35))
                    points.extend([
                        (self.width * 0.65 + ratio * (self.width * 0.10), self.height * (0.35 + ratio * 0.10)),
                        (self.width * 0.65 + ratio * (self.width * 0.17), self.height * (0.35 + ratio * 0.25)),
                        (self.width * 0.65 + ratio * (self.width * 0.23), self.height * (0.35 + ratio * 0.40)),
                        (self.width * 0.65 + ratio * (self.width * 0.27), self.height * (0.35 + ratio * 0.50)),
                        (self.width * 0.65 + ratio * (self.width * 0.31), self.height * (0.35 + ratio * 0.57)),
                        (self.width * 0.65 + ratio * (self.width * 0.35), self.height * (0.35 + ratio * 0.60)),
                    ])
                    # Add return points
                    points.extend([
                        (self.width * 0.65 + ratio * (self.width * 0.33), self.height * (0.35 + ratio * 0.45)),
                        (self.width * 0.65 + ratio * (self.width * 0.29), self.height * (0.35 + ratio * 0.30)),
                        (self.width * 0.65 + ratio * (self.width * 0.23), self.height * (0.35 + ratio * 0.15)),
                        (self.width * 0.65 + ratio * (self.width * 0.17), self.height * (0.35 + ratio * 0.00)),
                        (self.width * 0.65 + ratio * (self.width * 0.10), self.height * (0.35 - ratio * 0.17)),
                        (min(fill_width, self.width * 0.65), self.height * 0.18),
                    ])
                else:
                    points.append((fill_width, self.height * 0.18))

                points.append((0, self.height * 0.18))

                # Set color based on HP
                if self.hp_percent <= 0.15:
                    color = (255, 100, 100)  # Critical red
                elif self.hp_percent <= 0.3:
                    color = (255, 150, 100)  # Warning orange
                else:
                    color = (204, 0, 0)      # Normal red
            else:
                # Hero falchion fill (right-aligned)
                start_x = self.width * (1 - self.hp_percent)
                points = [
                    (self.width, self.height * 0.65),
                    (max(start_x, self.width * 0.35), self.height * 0.65),
                ]
                if start_x < self.width * 0.35:
                    ratio = min(1.0, (self.width * 0.35 - start_x) / (self.width * 0.35))
                    points.extend([
                        (self.width * 0.35 - ratio * (self.width * 0.10), self.height * (0.65 - ratio * 0.10)),
                        (self.width * 0.35 - ratio * (self.width * 0.17), self.height * (0.65 - ratio * 0.25)),
                        (self.width * 0.35 - ratio * (self.width * 0.23), self.height * (0.65 - ratio * 0.40)),
                        (self.width * 0.35 - ratio * (self.width * 0.27), self.height * (0.65 - ratio * 0.50)),
                        (self.width * 0.35 - ratio * (self.width * 0.31), self.height * (0.65 - ratio * 0.57)),
                        (self.width * 0.35 - ratio * (self.width * 0.35), self.height * (0.65 - ratio * 0.60)),
                    ])
                    # Add return points
                    points.extend([
                        (self.width * 0.35 - ratio * (self.width * 0.33), self.height * (0.65 - ratio * 0.45)),
                        (self.width * 0.35 - ratio * (self.width * 0.29), self.height * (0.65 - ratio * 0.30)),
                        (self.width * 0.35 - ratio * (self.width * 0.23), self.height * (0.65 - ratio * 0.15)),
                        (self.width * 0.35 - ratio * (self.width * 0.17), self.height * (0.65 - ratio * 0.00)),
                        (self.width * 0.35 - ratio * (self.width * 0.10), self.height * (0.65 + ratio * 0.17)),
                        (max(start_x, self.width * 0.35), self.height * 0.82),
                    ])
                else:
                    points.append((start_x, self.height * 0.82))

                points.append((self.width, self.height * 0.82))

                # Set color based on HP
                if self.hp_percent <= 0.15:
                    color = (100, 150, 255)  # Critical blue
                elif self.hp_percent <= 0.3:
                    color = (100, 180, 255)  # Warning light blue
                else:
                    color = (0, 51, 153)     # Normal blue

            c.polygon(color, points)
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

# ========================
# HP Bar Definitions
# ========================
define enemy_hp_bg = FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)
define hero_hp_bg = FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, False)

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# ========================
# HP Bar Screen
# ========================
screen battle_ui():
    # HP Bars positioned horizontally
    fixed:
        xalign 0.5
        yalign 0.2
        xsize 800
        ysize 200

        # Enemy HP Bar (left side)
        fixed:
            xpos 50
            ypos 70
            xsize HP_BAR_WIDTH
            ysize HP_BAR_HEIGHT

            # HP bar background
            add enemy_hp_bg

            # HP fill
            add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True):
                if enemy_hp <= 0.15:
                    at critical_hp_flash
                elif enemy_hp <= 0.3:
                    at low_hp_pulse

            # Enemy HP text (above bar)
            text "[int(enemy_hp * enemy_max_hp)]/[enemy_max_hp]":
                xalign 0.0
                ypos -35
                size 24
                color "#ff6666"
                outlines [(2, "#000000", 0, 0)]
                if enemy_hp <= 0.15:
                    at critical_hp_flash
                elif enemy_hp <= 0.3:
                    at low_hp_pulse

        # Hero HP Bar (right side)
        fixed:
            xpos 450
            ypos 70
            xsize HP_BAR_WIDTH
            ysize HP_BAR_HEIGHT

            # HP bar background
            add hero_hp_bg

            # HP fill
            add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False):
                if hero_hp <= 0.15:
                    at critical_hp_flash
                elif hero_hp <= 0.3:
                    at low_hp_pulse

            # Hero HP text (below bar)
            text "[int(hero_hp * hero_max_hp)]/[hero_max_hp]":
                xalign 1.0
                ypos HP_BAR_HEIGHT + 10
                size 24
                color "#66aaff"
                outlines [(2, "#000000", 0, 0)]
                if hero_hp <= 0.15:
                    at critical_hp_flash
                elif hero_hp <= 0.3:
                    at low_hp_pulse

# ========================
# Round UI Screen (positioned separately)
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
                size 18
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 32
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
    show screen round_ui

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap]"
    "Enemy HP: [int(enemy_hp * 100)]%, Hero HP: [int(hero_hp * 100)]%"

    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start

        "Damage Enemy" if enemy_hp > 0:
            $ enemy_hp = max(0, enemy_hp - (renpy.random.random() * 0.15 + 0.05))
            jump start

        "Damage Hero" if hero_hp > 0:
            $ hero_hp = max(0, hero_hp - (renpy.random.random() * 0.15 + 0.05))
            jump start

        "Heal Enemy" if enemy_hp < 1.0:
            $ enemy_hp = min(1.0, enemy_hp + 0.1)
            jump start

        "Heal Hero" if hero_hp < 1.0:
            $ hero_hp = min(1.0, hero_hp + 0.1)
            jump start

        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start

        "Reset HP":
            $ enemy_hp = 0.75
            $ hero_hp = 0.50
            jump start

        "Exit":
            return
