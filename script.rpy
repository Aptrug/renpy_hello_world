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

# UI Constants
define ROUND_RADIUS = 50
define ORB_RADIUS = 12
define HP_BAR_WIDTH = 350
define HP_BAR_HEIGHT = 60

# ========================
# ATL Transforms
# ========================
transform orb_glow:
    parallel:
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
        repeat
    parallel:
        ease 0.1 additive 0.3
        ease 0.1 additive 0.0
        repeat

transform round_breathe:
    ease 3.0 zoom 1.05
    ease 3.0 zoom 1.0
    repeat

transform orb_inactive:
    alpha 0.4
    zoom 0.9

transform vs_glow:
    ease 2.0 alpha 0.8 additive 0.2
    ease 2.0 alpha 1.0 additive 0.0
    repeat

# HP Bar Transforms
transform hp_wave_enemy:
    xpos -150
    alpha 0.0
    linear 3.0 xpos HP_BAR_WIDTH alpha 0.6
    alpha 0.0
    repeat

transform hp_wave_hero:
    xpos HP_BAR_WIDTH + 150
    alpha 0.0
    linear 3.0 xpos -150 alpha 0.6
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

# ========================
# Python Classes & Functions
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

    class HPBar(renpy.Displayable):
        def __init__(self, width, height, is_enemy=True, **kwargs):
            super(HPBar, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Draw background rectangle with rounded corners effect
            bg_color = (26, 26, 26)  # Dark background
            border_color = (80, 80, 80)  # Gray border

            # Background
            c.rect(bg_color, (0, 0, self.width, self.height))
            # Border
            c.rect(border_color, (0, 0, self.width, self.height), 2)

            return r

    class WaveEffect(renpy.Displayable):
        def __init__(self, width, height, **kwargs):
            super(WaveEffect, self).__init__(**kwargs)
            self.width = width
            self.height = height

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create gradient wave effect
            wave_color = (255, 255, 255, int(255 * 0.3))  # Semi-transparent white
            c.rect(wave_color, (0, 0, self.width, self.height))

            return r

    def get_orb_positions(num_orbs, radius=ROUND_RADIUS):
        """Returns orb positions arranged evenly in a circle."""
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2  # Start at top
            x = radius + int(radius * 0.8 * math.cos(angle)) - ORB_RADIUS
            y = radius + int(radius * 0.8 * math.sin(angle)) - ORB_RADIUS
            positions.append((x, y))
        return positions

    def format_hp_percent(hp_value):
        """Format HP as percentage for display."""
        return "{}%".format(int(hp_value * 100))

    # Combat functions
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
# Displayable Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define vs_bg = Circle(40, (255, 204, 0), (184, 134, 11), 4)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)
define hp_bar_bg = HPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)
define wave_effect = WaveEffect(120, HP_BAR_HEIGHT)

# ========================
# Screen Components
# ========================
screen enemy_hp_bar():
    fixed:
        xpos 100
        ypos 200
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background bar
        add hp_bar_bg

        # HP Fill (clipped)
        fixed:
            xsize int(HP_BAR_WIDTH * enemy_hp)
            ysize HP_BAR_HEIGHT

            if enemy_hp <= 0.15:
                add Solid("#ff4444", xsize=HP_BAR_WIDTH, ysize=HP_BAR_HEIGHT) at critical_hp_flash
            elif enemy_hp <= 0.30:
                add Solid("#cc0000", xsize=HP_BAR_WIDTH, ysize=HP_BAR_HEIGHT) at low_hp_pulse
            else:
                add Solid("#cc0000", xsize=HP_BAR_WIDTH, ysize=HP_BAR_HEIGHT)

            # Wave effect overlay
            add wave_effect alpha 0.4 at hp_wave_enemy

        # HP Text
        text "[enemy_hp:.0%]":
            color "#ff6666"
            size 24
            bold True
            outlines [(2, "#000000", 0, 0)]
            xpos HP_BAR_WIDTH - 60
            ypos -40

screen hero_hp_bar():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 100
        ypos 200
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background bar
        add hp_bar_bg

        # HP Fill (right-aligned, clipped)
        fixed:
            xpos HP_BAR_WIDTH - int(HP_BAR_WIDTH * hero_hp)
            xsize int(HP_BAR_WIDTH * hero_hp)
            ysize HP_BAR_HEIGHT

            if hero_hp <= 0.15:
                add Solid("#4499ff", xsize=HP_BAR_WIDTH, ysize=HP_BAR_HEIGHT) at critical_hp_flash
            elif hero_hp <= 0.30:
                add Solid("#003399", xsize=HP_BAR_WIDTH, ysize=HP_BAR_HEIGHT) at low_hp_pulse
            else:
                add Solid("#003399", xsize=HP_BAR_WIDTH, ysize=HP_BAR_HEIGHT)

            # Wave effect overlay
            add wave_effect alpha 0.4 at hp_wave_hero

        # HP Text
        text "[hero_hp:.0%]":
            color "#66aaff"
            size 24
            bold True
            outlines [(2, "#000000", 0, 0)]
            xpos 60
            ypos HP_BAR_HEIGHT + 20

screen round_display():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize ROUND_RADIUS * 2 + 20
        ysize ROUND_RADIUS * 2 + 20

        # VS Circle (positioned above round circle)
        fixed:
            xalign 0.5
            ypos -60
            xsize 80
            ysize 80

            add vs_bg at vs_glow

            text "VS":
                color "#000000"
                size 16
                bold True
                xalign 0.5
                yalign 0.5
                outlines [(1, "#ffffff", 0, 0)]

        # Round Circle
        fixed:
            xalign 0.5
            yalign 0.5
            xsize ROUND_RADIUS * 2
            ysize ROUND_RADIUS * 2

            add round_bg at round_breathe

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 0

                text "Round":
                    size 14
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

                text "[current_round]":
                    size 32
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

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

    # Dark battle background
    add Solid("#0a0a0a")

    use enemy_hp_bar
    use hero_hp_bar
    use round_display

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

        "Heal Enemy":
            $ heal_enemy(0.10)
            "Enemy heals slightly."
            jump start

        "Heal Hero":
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
