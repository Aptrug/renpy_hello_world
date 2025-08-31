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
define HP_BAR_WIDTH = 420
define HP_BAR_HEIGHT = 90

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
    xpos -200
    alpha 0.0
    linear 4.0 xpos HP_BAR_WIDTH + 50 alpha 0.8
    alpha 0.0
    repeat

transform hp_wave_hero:
    xpos HP_BAR_WIDTH + 200
    alpha 0.0
    linear 4.0 xpos -50 alpha 0.8
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

    class FalchionMask(renpy.Displayable):
        """Creates a white falchion shape on black background for masking"""
        def __init__(self, width, height, is_enemy=True, **kwargs):
            super(FalchionMask, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Black background
            c.rect((0, 0, 0, 255), (0, 0, self.width, self.height))

            # Create smooth falchion curve using multiple points
            if self.is_enemy:
                # Enemy falchion - curves right (blade pointing right)
                points = []
                # Top edge - smooth curve
                for i in range(101):
                    x = int(self.width * i / 100.0)
                    if x <= self.width * 0.7:
                        y = int(self.height * 0.35)  # Straight handle
                    else:
                        # Curved blade tip
                        progress = (x - self.width * 0.7) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.35 + curve * 0.15))
                    points.append((x, y))

                # Bottom edge - smooth curve (reverse)
                for i in range(100, -1, -1):
                    x = int(self.width * i / 100.0)
                    if x <= self.width * 0.7:
                        y = int(self.height * 0.65)  # Straight handle
                    else:
                        # Curved blade tip
                        progress = (x - self.width * 0.7) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.65 - curve * 0.15))
                    points.append((x, y))
            else:
                # Hero falchion - curves left (blade pointing left)
                points = []
                # Top edge
                for i in range(101):
                    x = int(self.width * (100 - i) / 100.0)
                    if x >= self.width * 0.3:
                        y = int(self.height * 0.35)  # Straight handle
                    else:
                        # Curved blade tip
                        progress = (self.width * 0.3 - x) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.35 + curve * 0.15))
                    points.append((x, y))

                # Bottom edge (reverse)
                for i in range(100, -1, -1):
                    x = int(self.width * (100 - i) / 100.0)
                    if x >= self.width * 0.3:
                        y = int(self.height * 0.65)  # Straight handle
                    else:
                        # Curved blade tip
                        progress = (self.width * 0.3 - x) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.65 - curve * 0.15))
                    points.append((x, y))

            # Draw white falchion shape for masking
            c.polygon((255, 255, 255, 255), points)

            return r

    class FalchionOutline(renpy.Displayable):
        """Creates the outline border of the falchion"""
        def __init__(self, width, height, is_enemy=True, **kwargs):
            super(FalchionOutline, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Same shape logic as mask, but just outline
            if self.is_enemy:
                points = []
                for i in range(101):
                    x = int(self.width * i / 100.0)
                    if x <= self.width * 0.7:
                        y = int(self.height * 0.35)
                    else:
                        progress = (x - self.width * 0.7) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.35 + curve * 0.15))
                    points.append((x, y))

                for i in range(100, -1, -1):
                    x = int(self.width * i / 100.0)
                    if x <= self.width * 0.7:
                        y = int(self.height * 0.65)
                    else:
                        progress = (x - self.width * 0.7) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.65 - curve * 0.15))
                    points.append((x, y))
            else:
                points = []
                for i in range(101):
                    x = int(self.width * (100 - i) / 100.0)
                    if x >= self.width * 0.3:
                        y = int(self.height * 0.35)
                    else:
                        progress = (self.width * 0.3 - x) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.35 + curve * 0.15))
                    points.append((x, y))

                for i in range(100, -1, -1):
                    x = int(self.width * (100 - i) / 100.0)
                    if x >= self.width * 0.3:
                        y = int(self.height * 0.65)
                    else:
                        progress = (self.width * 0.3 - x) / (self.width * 0.3)
                        curve = math.sin(progress * math.pi * 0.5)
                        y = int(self.height * (0.65 - curve * 0.15))
                    points.append((x, y))

            # Draw dark background shape
            c.polygon((26, 26, 26, 255), points)
            # Draw lighter outline
            c.polygon((80, 80, 80, 255), points, 3)

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
        xpos 80
        ypos 120
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background outline
        add FalchionOutline(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)

        # HP Fill using AlphaMask for proper clipping
        add AlphaMask(
            child=Fixed(
                # Main HP fill
                Solid("#cc0000", xsize=int(HP_BAR_WIDTH * enemy_hp), ysize=HP_BAR_HEIGHT),
                # Wave effect
                Solid("#ffffff", xsize=200, ysize=HP_BAR_HEIGHT) at hp_wave_enemy,
                xsize=HP_BAR_WIDTH,
                ysize=HP_BAR_HEIGHT
            ),
            mask=FalchionMask(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)
        ):
            if enemy_hp <= 0.15:
                at critical_hp_flash
            elif enemy_hp <= 0.30:
                at low_hp_pulse

        # HP Text
        $ hp_text = format_hp_percent(enemy_hp)
        text "[hp_text]" color "#ff6666" size 32 bold True outlines [(3, "#000000", 0, 0)]:
            xpos HP_BAR_WIDTH - 80
            ypos -60

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 80
        ypos 120
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT

        # Background outline
        add FalchionOutline(HP_BAR_WIDTH, HP_BAR_HEIGHT, False)

        # HP Fill using AlphaMask - right-aligned
        add AlphaMask(
            child=Fixed(
                # Main HP fill (right-aligned)
                Solid("#003399",
                    xpos=HP_BAR_WIDTH - int(HP_BAR_WIDTH * hero_hp),
                    xsize=int(HP_BAR_WIDTH * hero_hp),
                    ysize=HP_BAR_HEIGHT
                ),
                # Wave effect
                Solid("#ffffff", xsize=200, ysize=HP_BAR_HEIGHT) at hp_wave_hero,
                xsize=HP_BAR_WIDTH,
                ysize=HP_BAR_HEIGHT
            ),
            mask=FalchionMask(HP_BAR_WIDTH, HP_BAR_HEIGHT, False)
        ):
            if hero_hp <= 0.15:
                at critical_hp_flash
            elif hero_hp <= 0.30:
                at low_hp_pulse

        # HP Text
        $ hp_text = format_hp_percent(hero_hp)
        text "[hp_text]" color "#66aaff" size 32 bold True outlines [(3, "#000000", 0, 0)]:
            xpos 80
            ypos HP_BAR_HEIGHT + 30

# ========================
# VS Circle
# ========================
screen vs_circle():
    fixed:
        xalign 0.5
        yalign 0.25
        xsize 100
        ysize 100

        # VS background circle with glow
        add Circle(45, (255, 204, 0), (184, 134, 11), 4) at vs_glow

        # VS text
        text "VS" color "#000000" size 28 bold True:
            xalign 0.5
            yalign 0.5
            outlines [(2, "#ffffff", 0, 0)]

# ========================
# Round Display
# ========================
screen round_display():
    fixed:
        xalign 0.5
        yalign 0.5
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
