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
define HP_BAR_WIDTH = 380
define HP_BAR_HEIGHT = 65

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
transform hp_wave_right:
    xpos -180
    alpha 0.0
    linear 3.0 xpos HP_BAR_WIDTH alpha 1.0
    alpha 0.0
    repeat

transform hp_wave_left:
    xpos HP_BAR_WIDTH + 180
    alpha 0.0
    linear 3.0 xpos -180 alpha 1.0
    alpha 0.0
    repeat

transform hp_bar_fill_update:
    linear 0.8 truecenter

transform low_hp_pulse:
    ease 1.5 alpha 0.7
    ease 1.5 alpha 1.0
    repeat

transform critical_hp_flash:
    ease 0.6 alpha 0.8
    ease 0.6 alpha 1.0
    repeat

transform hp_text_pulse:
    ease 1.2 zoom 1.0
    ease 1.2 zoom 1.05
    repeat

transform critical_text_flash:
    ease 0.8 zoom 1.0 alpha 0.9
    ease 0.8 zoom 1.1 alpha 1.0
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
                # Enemy falchion (left-pointing)
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
                # Hero falchion (right-pointing)
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

            # Draw the falchion shape
            c.polygon((30, 30, 30), points)
            c.polygon((80, 80, 80), points, 2)  # Border

            return r

    def get_orb_positions(num_orbs):
        """Returns orb positions arranged evenly in a circle around ROUND_RADIUS."""
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = ROUND_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
            y = ROUND_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

    def get_hp_transform(hp_ratio):
        """Returns appropriate transform for HP state"""
        if hp_ratio <= 0.15:
            return "critical_hp_flash"
        elif hp_ratio <= 0.30:
            return "low_hp_pulse"
        return None

    def get_hp_text_transform(hp_ratio):
        """Returns appropriate text transform for HP state"""
        if hp_ratio <= 0.15:
            return "critical_text_flash"
        elif hp_ratio <= 0.30:
            return "hp_text_pulse"
        return None

# ========================
# Circle and HP Bar Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

define enemy_hp_bar_bg = FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)
define hero_hp_bar_bg = FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, False)

# ========================
# HP Bar Screen Components
# ========================
screen hp_bar_enemy():
    fixed:
        xpos 50
        ypos 100
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background shape
        add enemy_hp_bar_bg

        # HP fill with clipping
        fixed:
            xsize int(HP_BAR_WIDTH * enemy_hp)
            ysize HP_BAR_HEIGHT

            $ hp_transform = get_hp_transform(enemy_hp)
            if hp_transform:
                add "#cc0000" at eval(hp_transform)
            else:
                add "#cc0000"

            # Wave effect
            add Solid("#ffffff", xsize=180, ysize=HP_BAR_HEIGHT) alpha 0.3 at hp_wave_right

        # HP Text
        $ text_transform = get_hp_text_transform(enemy_hp)
        if text_transform:
            text "{color=#ff6666}[enemy_hp:.0%]{/color}" at eval(text_transform):
                xpos HP_BAR_WIDTH - 80
                ypos -50
                size 22
                outlines [(2, "#000000", 0, 0)]
        else:
            text "{color=#ff6666}[enemy_hp:.0%]{/color}":
                xpos HP_BAR_WIDTH - 80
                ypos -50
                size 22
                outlines [(2, "#000000", 0, 0)]

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 50
        ypos 100
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background shape
        add hero_hp_bar_bg

        # HP fill with clipping (right-aligned)
        fixed:
            xpos HP_BAR_WIDTH - int(HP_BAR_WIDTH * hero_hp)
            xsize int(HP_BAR_WIDTH * hero_hp)
            ysize HP_BAR_HEIGHT

            $ hp_transform = get_hp_transform(hero_hp)
            if hp_transform:
                add "#003399" at eval(hp_transform)
            else:
                add "#003399"

            # Wave effect
            add Solid("#ffffff", xsize=180, ysize=HP_BAR_HEIGHT) alpha 0.3 at hp_wave_left

        # HP Text
        $ text_transform = get_hp_text_transform(hero_hp)
        if text_transform:
            text "{color=#66aaff}[hero_hp:.0%]{/color}" at eval(text_transform):
                xpos 80
                ypos HP_BAR_HEIGHT + 20
                size 22
                outlines [(2, "#000000", 0, 0)]
        else:
            text "{color=#66aaff}[hero_hp:.0%]{/color}":
                xpos 80
                ypos HP_BAR_HEIGHT + 20
                size 22
                outlines [(2, "#000000", 0, 0)]

# ========================
# Main Battle UI Screen
# ========================
screen battle_ui():
    # HP Bars
    use hp_bar_enemy
    use hp_bar_hero

    # Round Circle (center)
    fixed:
        xalign 0.5
        yalign 0.25
        xsize ROUND_RADIUS * 2
        ysize ROUND_RADIUS * 2

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

        # AP Orbs arranged around the circle
        for i, (x, y) in enumerate(get_orb_positions(max_ap)):
            add (orb_active if i < available_ap else orb_inactive_img) at (orb_glow if i < available_ap else orb_inactive) xpos x ypos y

# ========================
# Combat Actions
# ========================
init python:
    def damage_enemy(amount):
        global enemy_hp
        enemy_hp = max(0.0, enemy_hp - amount)
        renpy.restart_interaction()

    def damage_hero(amount):
        global hero_hp
        hero_hp = max(0.0, hero_hp - amount)
        renpy.restart_interaction()

    def heal_enemy(amount):
        global enemy_hp
        enemy_hp = min(enemy_max_hp, enemy_hp + amount)
        renpy.restart_interaction()

    def heal_hero(amount):
        global hero_hp
        hero_hp = min(hero_max_hp, hero_hp + amount)
        renpy.restart_interaction()

    def next_round():
        global current_round, available_ap
        current_round += 1
        available_ap = max_ap
        renpy.restart_interaction()

# ========================
# Demo Label
# ========================
label start:
    show screen battle_ui

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap]"
    "Enemy HP: [enemy_hp:.0%] | Hero HP: [hero_hp:.0%]"

    menu:
        "Attack Enemy" if available_ap > 0:
            $ available_ap -= 1
            $ damage_enemy(0.15)
            "You deal damage to the enemy!"
            jump start

        "Attack Hero" if available_ap > 0:
            $ available_ap -= 1
            $ damage_hero(0.10)
            "The enemy attacks you!"
            jump start

        "Heal Enemy" if available_ap > 0:
            $ available_ap += 1
            $ heal_enemy(0.10)
            "Enemy heals slightly."
            jump start

        "Heal Hero" if available_ap > 0:
            $ available_ap += 1
            $ heal_hero(0.10)
            "You heal slightly."
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start

        "Next Round":
            $ next_round()
            jump start

        "Reset HP":
            $ enemy_hp = 0.75
            $ hero_hp = 0.50
            jump start

        "Exit":
            return

# ========================
# Alternative Simplified Version (if the above is too complex)
# ========================

# Simple HP bar using built-in Bar displayable
screen simple_battle_ui():
    # Enemy HP (left side)
    vbox:
        xpos 50
        ypos 100
        spacing 10

        text "Enemy HP":
            color "#ff6666"
            size 20
            outlines [(2, "#000000", 0, 0)]

        bar:
            value AnimatedValue(enemy_hp, enemy_max_hp, 0.8)
            range enemy_max_hp
            xsize HP_BAR_WIDTH
            ysize 30
            left_bar Frame("gui/bar/left.png", 6, 6)
            right_bar Frame("gui/bar/right.png", 6, 6)
            thumb None

    # Hero HP (right side)
    vbox:
        xpos config.screen_width - HP_BAR_WIDTH - 50
        ypos 100
        spacing 10

        text "Hero HP":
            color "#66aaff"
            size 20
            outlines [(2, "#000000", 0, 0)]

        bar:
            value AnimatedValue(hero_hp, hero_max_hp, 0.8)
            range hero_max_hp
            xsize HP_BAR_WIDTH
            ysize 30
            left_bar Frame("gui/bar/left.png", 6, 6)
            right_bar Frame("gui/bar/right.png", 6, 6)
            thumb None

    # Round UI (center) - same as before
    fixed:
        xalign 0.5
        yalign 0.25
        xsize ROUND_RADIUS * 2
        ysize ROUND_RADIUS * 2

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
