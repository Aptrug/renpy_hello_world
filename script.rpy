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

# ========================
# HP Bar Screen Components
# ========================
screen hp_bar_enemy():
    fixed:
        xpos 50
        ypos 200
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background
        frame:
            xsize HP_BAR_WIDTH
            ysize HP_BAR_HEIGHT
            background Solid("#1a1a1a")

            # HP fill
            frame:
                xsize int(HP_BAR_WIDTH * enemy_hp)
                ysize HP_BAR_HEIGHT
                background Solid("#cc0000")

                if enemy_hp <= 0.15:
                    at critical_hp_flash
                elif enemy_hp <= 0.30:
                    at low_hp_pulse

        # HP Text
        $ hp_percent = int(enemy_hp * 100)
        if enemy_hp <= 0.15:
            text "[hp_percent]%" color "#ff6666" size 24 outlines [(2, "#000000", 0, 0)] at critical_text_flash:
                xpos HP_BAR_WIDTH - 60
                ypos -40
        elif enemy_hp <= 0.30:
            text "[hp_percent]%" color "#ff6666" size 24 outlines [(2, "#000000", 0, 0)] at hp_text_pulse:
                xpos HP_BAR_WIDTH - 60
                ypos -40
        else:
            text "[hp_percent]%" color "#ff6666" size 24 outlines [(2, "#000000", 0, 0)]:
                xpos HP_BAR_WIDTH - 60
                ypos -40

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 50
        ypos 200
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background
        frame:
            xsize HP_BAR_WIDTH
            ysize HP_BAR_HEIGHT
            background Solid("#1a1a1a")

            # HP fill (right-aligned)
            frame:
                xpos HP_BAR_WIDTH - int(HP_BAR_WIDTH * hero_hp)
                xsize int(HP_BAR_WIDTH * hero_hp)
                ysize HP_BAR_HEIGHT
                background Solid("#003399")

                if hero_hp <= 0.15:
                    at critical_hp_flash
                elif hero_hp <= 0.30:
                    at low_hp_pulse

        # HP Text
        $ hp_percent = int(hero_hp * 100)
        if hero_hp <= 0.15:
            text "[hp_percent]%" color "#66aaff" size 24 outlines [(2, "#000000", 0, 0)] at critical_text_flash:
                xpos 60
                ypos HP_BAR_HEIGHT + 20
        elif hero_hp <= 0.30:
            text "[hp_percent]%" color "#66aaff" size 24 outlines [(2, "#000000", 0, 0)] at hp_text_pulse:
                xpos 60
                ypos HP_BAR_HEIGHT + 20
        else:
            text "[hp_percent]%" color "#66aaff" size 24 outlines [(2, "#000000", 0, 0)]:
                xpos 60
                ypos HP_BAR_HEIGHT + 20

# ========================
# Main Battle UI Screen
# ========================
screen battle_ui():
    modal False

    # HP Bars
    use hp_bar_enemy
    use hp_bar_hero

    # Round Circle (center)
    fixed:
        xalign 0.5
        yalign 0.3
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
            if i < available_ap:
                add orb_active at orb_glow xpos x ypos y
            else:
                add orb_inactive_img at orb_inactive xpos x ypos y

# ========================
# Combat Actions
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

# ========================
# Demo Label
# ========================
label start:
    show screen battle_ui

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap]"
    "Enemy HP: [enemy_hp:.1%] | Hero HP: [hero_hp:.1%]"

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
