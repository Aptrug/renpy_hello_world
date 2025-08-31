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

transform hp_wave_enemy:
    xpos -180
    alpha 0.0
    linear 3.0 xpos HP_BAR_WIDTH alpha 0.6
    alpha 0.0
    repeat

transform hp_wave_hero:
    xpos HP_BAR_WIDTH + 180
    alpha 0.0
    linear 3.0 xpos -180 alpha 0.6
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

transform vs_glow:
    ease 2.0 alpha 0.8
    ease 2.0 alpha 1.0
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

    class FalchionShape(renpy.Displayable):
        def __init__(self, width, height, is_enemy=True, fill_color="#cc0000", **kwargs):
            super(FalchionShape, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy
            self.fill_color = fill_color

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create falchion blade shape points
            if self.is_enemy:
                # Enemy falchion - curves to the right (blade pointing right)
                points = [
                    (0, int(self.height * 0.4)),                    # Left start
                    (int(self.width * 0.7), int(self.height * 0.4)), # Main body top
                    (int(self.width * 0.8), int(self.height * 0.45)), # Curve start
                    (int(self.width * 0.85), int(self.height * 0.5)), # Mid curve
                    (int(self.width * 0.9), int(self.height * 0.55)), # Tip approach
                    (int(self.width * 0.95), int(self.height * 0.58)), # Near tip
                    (int(self.width), int(self.height * 0.5)),        # Sharp tip
                    (int(self.width * 0.95), int(self.height * 0.42)), # Tip back
                    (int(self.width * 0.9), int(self.height * 0.45)), # Curve back
                    (int(self.width * 0.85), int(self.height * 0.5)), # Mid back
                    (int(self.width * 0.8), int(self.height * 0.55)), # Curve back
                    (int(self.width * 0.7), int(self.height * 0.6)),  # Main body bottom
                    (0, int(self.height * 0.6))                      # Left end
                ]
            else:
                # Hero falchion - curves to the left (blade pointing left)
                points = [
                    (int(self.width), int(self.height * 0.4)),        # Right start
                    (int(self.width * 0.3), int(self.height * 0.4)),  # Main body top
                    (int(self.width * 0.2), int(self.height * 0.45)), # Curve start
                    (int(self.width * 0.15), int(self.height * 0.5)), # Mid curve
                    (int(self.width * 0.1), int(self.height * 0.55)), # Tip approach
                    (int(self.width * 0.05), int(self.height * 0.58)), # Near tip
                    (0, int(self.height * 0.5)),                      # Sharp tip
                    (int(self.width * 0.05), int(self.height * 0.42)), # Tip back
                    (int(self.width * 0.1), int(self.height * 0.45)), # Curve back
                    (int(self.width * 0.15), int(self.height * 0.5)), # Mid back
                    (int(self.width * 0.2), int(self.height * 0.55)), # Curve back
                    (int(self.width * 0.3), int(self.height * 0.6)),  # Main body bottom
                    (int(self.width), int(self.height * 0.6))         # Right end
                ]

            # Draw the falchion shape
            if isinstance(self.fill_color, tuple):
                c.polygon(self.fill_color, points)
            else:
                # Convert hex color to RGB tuple
                hex_color = self.fill_color.lstrip('#')
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                c.polygon(rgb, points)

            # Add border
            c.polygon((80, 80, 80), points, 2)

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

    def format_hp_percent(hp_value):
        """Format HP as percentage for display."""
        return str(int(hp_value * 100)) + "%"

# ========================
# Circle and Shape Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

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
        add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, True, "#1a1a1a")

        # HP Fill - clipped to current HP
        fixed:
            xsize int(HP_BAR_WIDTH * enemy_hp)
            ysize HP_BAR_HEIGHT

            if enemy_hp <= 0.15:
                add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, True, "#ff4444") at critical_hp_flash
            elif enemy_hp <= 0.30:
                add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, True, "#cc0000") at low_hp_pulse
            else:
                add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, True, "#cc0000")

            # Wave effect
            add Solid("#ffffff", xsize=180, ysize=HP_BAR_HEIGHT) alpha 0.3 at hp_wave_enemy

        # HP Text
        $ hp_text = format_hp_percent(enemy_hp)
        text "[hp_text]" color "#ff6666" size 28 outlines [(3, "#000000", 0, 0)]:
            xpos HP_BAR_WIDTH - 70
            ypos -50

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 50
        ypos 150
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background falchion shape
        add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, False, "#1a1a1a")

        # HP Fill - right-aligned clipped to current HP
        fixed:
            xpos HP_BAR_WIDTH - int(HP_BAR_WIDTH * hero_hp)
            xsize int(HP_BAR_WIDTH * hero_hp)
            ysize HP_BAR_HEIGHT

            if hero_hp <= 0.15:
                add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, False, "#4499ff") at critical_hp_flash
            elif hero_hp <= 0.30:
                add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, False, "#003399") at low_hp_pulse
            else:
                add FalchionShape(HP_BAR_WIDTH, HP_BAR_HEIGHT, False, "#003399")

            # Wave effect
            add Solid("#ffffff", xsize=180, ysize=HP_BAR_HEIGHT) alpha 0.3 at hp_wave_hero

        # HP Text
        $ hp_text = format_hp_percent(hero_hp)
        text "[hp_text]" color "#66aaff" size 28 outlines [(3, "#000000", 0, 0)]:
            xpos 70
            ypos HP_BAR_HEIGHT + 25

# ========================
# VS Circle
# ========================
screen vs_circle():
    fixed:
        xalign 0.5
        yalign 0.35
        xsize 100
        ysize 100

        # VS background circle with glow
        add Circle(40, (255, 204, 0), (184, 134, 11), 4) at vs_glow

        # VS text
        text "VS" color "#000000" size 24 bold True:
            xalign 0.5
            yalign 0.5
            outlines [(1, "#ffffff", 0, 0)]

# ========================
# Round Display
# ========================
screen round_display():
    fixed:
        xalign 0.5
        yalign 0.6
        xsize ROUND_RADIUS * 2
        ysize ROUND_RADIUS * 2

        # Round circle background
        add round_bg at round_breathe

        # Round text
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
                size 48
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

    use hp_bar_enemy
    use hp_bar_hero
    use vs_circle
    use round_display

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

# ========================
# Demo Label
# ========================
label start:
    show screen battle_ui

    $ enemy_hp_display = format_hp_percent(enemy_hp)
    $ hero_hp_display = format_hp_percent(hero_hp)

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap]"
    "Enemy HP: [enemy_hp_display] | Hero HP: [hero_hp_display]"

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
