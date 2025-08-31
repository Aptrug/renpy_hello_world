class FalchionHPFill(renpy.Displayable):
        def __init__(self, width, height, hp_ratio, is_enemy=True, **kwargs):
            super(FalchionHPFill, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.hp_ratio = max(0, min(1, hp_ratio))
            self.is_enemy = is_enemy

        def render(self, width, height, st, at):
            if self.hp_ratio <= 0:
                return renpy.Render(0, 0)

            # Choose colors based on HP level
            if self.hp_ratio <= 0.15:
                base_color = (255, 80, 80) if self.is_enemy else (80, 140, 255)
            elif self.hp_ratio <= 0.30:
                base_color = (220, 40, 40) if self.is_enemy else (40, 110, 220)
            else:
                base_color = (180, 20, 20) if self.is_enemy else (20, 80, 180)

            # Create a mask for HP fill
            if self.is_enemy:
                # Enemy fills left to right
                fill_width = int(self.width * self.hp_ratio)
                r = renpy.Render(fill_width, self.height)
                canvas = r.canvas()

                # Create clipped falchion shape
                points = [
                    (0, int(self.height * 0.30)),
                    (min(fill_width, int(self.width * 0.12)), int(self.height * 0.28)),
                ]

                # Progressively add more complex shape as HP fill increases
                if fill_width > int(self.width * 0.12):
                    if fill_width >= int(self.width * 0.20):
                        points.append((min(fill_width, int(self.width * 0.20)), int(self.height * 0.25)))
                    if fill_width >= int(self.width * 0.30):
                        points.append((min(fill_width, int(self.width * 0.30)), int(self.height * 0.22)))
                    if fill_width >= int(self.width * 0.45):
                        points.append((min(fill_width, int(self.width * 0.45)), int(self.height * 0.18)))
                    if fill_width >= int(self.width * 0.60):
                        points.append((min(fill_width, int(self.width * 0.60)), int(self.height * 0.15)))
                    if fill_width >= int(self.width * 0.72):
                        points.append((min(fill_width, int(self.width * 0.72)), int(self.height * 0.20)))
                    if fill_width >= int(self.width * 0.82):
                        points.append((min(fill_width, int(self.width * 0.82)), int(self.height * 0.30)))
                    if fill_width >= int(self.width * 0.90):
                        points.append((min(fill_width, int(self.width * 0.90)), int(self.height * 0.42)))
                    if fill_width >= int(self.width * 0.96):
                        points.append((min(fill_width, int(self.width * 0.96)), int(self.height * 0.48)))
                    if fill_width >= self.width:
                        points.append((self.width, int(self.height * 0.50)))

                # Create bottom edge (mirror of top)
                bottom_points = []
                for x, y in reversed(points):
                    if y != int(self.height * 0.50):  # Don't duplicate tip
                        bottom_y = self.height - y + int(self.height * 0.30) - int(self.height * 0.30)
                        bottom_y = int(self.height * 0.70) + (int(self.height * 0.30) - y)
                        bottom_points.append((x, bottom_y))

                points.extend(bottom_points)

            else:
                # Hero fills right to left
                fill_width = int(self.width * self.hp_ratio)
                start_x = self.width - fill_width
                r = renpy.Render(self.width, self.height)
                canvas = r.canvas()

                points = [
                    (self.width, int(self.height * 0.30)),
                    (max(start_x, int(self.width * 0.88)), int(self.height * 0.28)),
                ]

                # Add shape points based on fill level
                if start_x <= int(self.width * 0.88):
                    if start_x <= int(self.width * 0.80):
                        points.append((max(start_x, int(self.width * 0.80)), int(self.height * 0.25)))
                    if start_x <= int(self.width * 0.70):
                        points.append((max(start_x, int(self.width * 0.70)), int(self.height * 0.22)))
                    if start_x <= int(self.width * 0.55):
                        points.append((max(start_x, int(self.width * 0.55)), int(self.height * 0.18)))
                    if start_x <= int(self.width * 0.40):
                        points.append((max(start_x, int(self.width * 0.40)), int(self.height * 0.15)))
                    if start_x <= int(self.width * 0.28):
                        points.append((max(start_x, int(self.width * 0.28)), int(self.height * 0.20)))
                    if start_x <= int(self.width * 0.18):
                        points.append((max(start_x, int(self.width * 0.18)), int(self.height * 0.30)))
                    if start_x <= int(self.width * 0.10):
                        points.append((max(start_x, int(self.width * 0.10)), int(self.height * 0.42)))
                    if start_x <= int(self.width * 0.04):
                        points.append((max(start_x, int(self.width * 0.04)), int(self.height * 0.48)))
                    if start_x <= 0:
                        points.append((0, int(self.height * 0.50)))

                # Create bottom edge
                bottom_points = []
                for x, y in reversed(points):
                    if y != int(self.height * 0.50):
                        bottom_y = int(self.height * 0.70) + (int(self.height * 0.30) - y)
                        bottom_points.append((x, bottom_y))

                points.extend(bottom_points)

            canvas.polygon(base_color, points)
            return r# ========================
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
define ROUND_RADIUS = 65
define ORB_RADIUS = 12
define HP_BAR_WIDTH = 350
define HP_BAR_HEIGHT = 70

# ========================
# ATL Transforms
# ========================
transform orb_glow:
    parallel:
        ease 1.2 alpha 0.7
        ease 1.2 alpha 1.0
    parallel:
        ease 0.1 additive 0.4
        ease 0.1 additive 0.0
    repeat

transform round_breathe:
    ease 3.5 zoom 1.03
    ease 3.5 zoom 1.0
    repeat

transform orb_inactive:
    alpha 0.35
    zoom 0.85

transform hp_wave_enemy:
    xpos -180
    alpha 0.0
    ease 0.5 alpha 0.8
    linear 2.5 xpos HP_BAR_WIDTH
    ease 0.5 alpha 0.0
    repeat

transform hp_wave_hero:
    xpos HP_BAR_WIDTH + 180
    alpha 0.0
    ease 0.5 alpha 0.8
    linear 2.5 xpos -180
    ease 0.5 alpha 0.0
    repeat

transform low_hp_pulse:
    ease 1.2 alpha 0.8
    ease 1.2 alpha 1.0
    repeat

transform critical_hp_flash:
    ease 0.4 alpha 0.7
    ease 0.4 alpha 1.0
    repeat

transform round_glow:
    parallel:
        ease 2.5 alpha 0.85
        ease 2.5 alpha 1.0
    parallel:
        ease 0.2 additive 0.2
        ease 0.2 additive 0.0
    repeat

# ========================
# Python Classes and Helpers
# ========================
init python:
    import math

    class FalchionHPBar(renpy.Displayable):
        def __init__(self, width, height, is_enemy=True, **kwargs):
            super(FalchionHPBar, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            canvas = r.canvas()

            # Create authentic falchion blade shape
            if self.is_enemy:
                # Enemy falchion - elegant curved blade pointing right
                points = [
                    # Hilt section (left side)
                    (0, int(self.height * 0.25)),                     # Hilt top
                    (int(self.width * 0.15), int(self.height * 0.25)), # Hilt end top
                    # Blade starts with slight widening
                    (int(self.width * 0.25), int(self.height * 0.20)), # Blade start top
                    (int(self.width * 0.40), int(self.height * 0.15)), # Early blade top
                    (int(self.width * 0.60), int(self.height * 0.10)), # Mid blade top
                    (int(self.width * 0.75), int(self.height * 0.08)), # Late blade top
                    # Curved tip section
                    (int(self.width * 0.85), int(self.height * 0.15)), # Tip curve start
                    (int(self.width * 0.92), int(self.height * 0.25)), # Tip curve mid
                    (int(self.width * 0.97), int(self.height * 0.40)), # Near tip
                    (int(self.width), int(self.height * 0.50)),        # Sharp tip point
                    (int(self.width * 0.97), int(self.height * 0.60)), # Tip back
                    (int(self.width * 0.92), int(self.height * 0.75)), # Tip curve back
                    (int(self.width * 0.85), int(self.height * 0.85)), # Curve back
                    # Blade back edge
                    (int(self.width * 0.75), int(self.height * 0.92)), # Late blade bottom
                    (int(self.width * 0.60), int(self.height * 0.90)), # Mid blade bottom
                    (int(self.width * 0.40), int(self.height * 0.85)), # Early blade bottom
                    (int(self.width * 0.25), int(self.height * 0.80)), # Blade end bottom
                    # Back to hilt
                    (int(self.width * 0.15), int(self.height * 0.75)), # Hilt start bottom
                    (0, int(self.height * 0.75))                      # Hilt bottom
                ]
            else:
                # Hero falchion - mirrored elegant curved blade pointing left
                points = [
                    # Hilt section (right side)
                    (int(self.width), int(self.height * 0.25)),        # Hilt top
                    (int(self.width * 0.85), int(self.height * 0.25)), # Hilt end top
                    # Blade starts with slight widening
                    (int(self.width * 0.75), int(self.height * 0.20)), # Blade start top
                    (int(self.width * 0.60), int(self.height * 0.15)), # Early blade top
                    (int(self.width * 0.40), int(self.height * 0.10)), # Mid blade top
                    (int(self.width * 0.25), int(self.height * 0.08)), # Late blade top
                    # Curved tip section
                    (int(self.width * 0.15), int(self.height * 0.15)), # Tip curve start
                    (int(self.width * 0.08), int(self.height * 0.25)), # Tip curve mid
                    (int(self.width * 0.03), int(self.height * 0.40)), # Near tip
                    (0, int(self.height * 0.50)),                      # Sharp tip point
                    (int(self.width * 0.03), int(self.height * 0.60)), # Tip back
                    (int(self.width * 0.08), int(self.height * 0.75)), # Tip curve back
                    (int(self.width * 0.15), int(self.height * 0.85)), # Curve back
                    # Blade back edge
                    (int(self.width * 0.25), int(self.height * 0.92)), # Late blade bottom
                    (int(self.width * 0.40), int(self.height * 0.90)), # Mid blade bottom
                    (int(self.width * 0.60), int(self.height * 0.85)), # Early blade bottom
                    (int(self.width * 0.75), int(self.height * 0.80)), # Blade end bottom
                    # Back to hilt
                    (int(self.width * 0.85), int(self.height * 0.75)), # Hilt start bottom
                    (int(self.width), int(self.height * 0.75))         # Hilt bottom
                ]

            # Draw background (dark)
            canvas.polygon((25, 25, 25), points)
            # Draw border
            canvas.polygon((100, 100, 100), points, 2)

            return r

    class FalchionHPBar(renpy.Displayable):
        def __init__(self, width, height, is_enemy=True, **kwargs):
            super(FalchionHPBar, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.is_enemy = is_enemy

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            canvas = r.canvas()

            # Create authentic falchion blade shape with proper curves
            if self.is_enemy:
                # Enemy falchion - graceful S-curve pointing right
                points = [
                    # Hilt/guard section
                    (0, int(self.height * 0.30)),
                    (int(self.width * 0.12), int(self.height * 0.28)),
                    # Blade base - starts wide
                    (int(self.width * 0.20), int(self.height * 0.25)),
                    (int(self.width * 0.30), int(self.height * 0.22)),
                    (int(self.width * 0.45), int(self.height * 0.18)),
                    # Mid-blade with characteristic curve
                    (int(self.width * 0.60), int(self.height * 0.15)),
                    (int(self.width * 0.72), int(self.height * 0.20)),
                    (int(self.width * 0.82), int(self.height * 0.30)),
                    # Tip section - sharp curved point
                    (int(self.width * 0.90), int(self.height * 0.42)),
                    (int(self.width * 0.96), int(self.height * 0.48)),
                    (int(self.width), int(self.height * 0.50)),        # Sharp tip
                    (int(self.width * 0.96), int(self.height * 0.52)),
                    (int(self.width * 0.90), int(self.height * 0.58)),
                    # Back edge with reverse curve
                    (int(self.width * 0.82), int(self.height * 0.70)),
                    (int(self.width * 0.72), int(self.height * 0.80)),
                    (int(self.width * 0.60), int(self.height * 0.85)),
                    # Back to base
                    (int(self.width * 0.45), int(self.height * 0.82)),
                    (int(self.width * 0.30), int(self.height * 0.78)),
                    (int(self.width * 0.20), int(self.height * 0.75)),
                    (int(self.width * 0.12), int(self.height * 0.72)),
                    (0, int(self.height * 0.70))
                ]
            else:
                # Hero falchion - mirrored S-curve pointing left
                points = [
                    # Hilt/guard section
                    (int(self.width), int(self.height * 0.30)),
                    (int(self.width * 0.88), int(self.height * 0.28)),
                    # Blade base - starts wide
                    (int(self.width * 0.80), int(self.height * 0.25)),
                    (int(self.width * 0.70), int(self.height * 0.22)),
                    (int(self.width * 0.55), int(self.height * 0.18)),
                    # Mid-blade with characteristic curve
                    (int(self.width * 0.40), int(self.height * 0.15)),
                    (int(self.width * 0.28), int(self.height * 0.20)),
                    (int(self.width * 0.18), int(self.height * 0.30)),
                    # Tip section - sharp curved point
                    (int(self.width * 0.10), int(self.height * 0.42)),
                    (int(self.width * 0.04), int(self.height * 0.48)),
                    (0, int(self.height * 0.50)),                      # Sharp tip
                    (int(self.width * 0.04), int(self.height * 0.52)),
                    (int(self.width * 0.10), int(self.height * 0.58)),
                    # Back edge with reverse curve
                    (int(self.width * 0.18), int(self.height * 0.70)),
                    (int(self.width * 0.28), int(self.height * 0.80)),
                    (int(self.width * 0.40), int(self.height * 0.85)),
                    # Back to base
                    (int(self.width * 0.55), int(self.height * 0.82)),
                    (int(self.width * 0.70), int(self.height * 0.78)),
                    (int(self.width * 0.80), int(self.height * 0.75)),
                    (int(self.width * 0.88), int(self.height * 0.72)),
                    (int(self.width), int(self.height * 0.70))
                ]

            # Draw background (dark metallic)
            canvas.polygon((25, 25, 25), points)
            # Draw metallic border
            canvas.polygon((120, 120, 120), points, 2)

            return r

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
            canvas = r.canvas()

            if self.color:
                canvas.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                canvas.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return r

    def get_orb_positions(num_orbs, center_x, center_y):
        """Returns orb positions arranged evenly in a circle."""
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = center_x + ROUND_RADIUS * math.cos(angle) - ORB_RADIUS
            y = center_y + ROUND_RADIUS * math.sin(angle) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

    def format_hp_display(hp_value):
        """Format HP as percentage for display."""
        return "{:.0f}%".format(hp_value * 100)

# ========================
# Displayable Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (60, 60, 60), (40, 40, 40), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (180, 130, 10), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (80, 80, 80), (50, 50, 50), 2)

# ========================
# Battle UI Screen
# ========================
screen battle_ui():
    modal False

    # Main UI container
    fixed:
        xsize config.screen_width
        ysize config.screen_height

        # Enemy HP Bar (Left)
        fixed:
            xpos 80
            ypos 200
            xsize HP_BAR_WIDTH
            ysize HP_BAR_HEIGHT

            # Background shape
            add FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, True)

            # HP Fill with animations
            if enemy_hp <= 0.15:
                add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True) at critical_hp_flash
            elif enemy_hp <= 0.30:
                add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True) at low_hp_pulse
            else:
                add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, enemy_hp, True)

            # Wave effect overlay
            add Solid("#ffffff") xsize 180 ysize HP_BAR_HEIGHT alpha 0.2 at hp_wave_enemy

        # Enemy HP Text
        text "[format_hp_display(enemy_hp)]":
            xpos 60
            ypos 130
            size 24
            color "#ff6666"
            outlines [(2, "#000000", 0, 0)]
            if enemy_hp <= 0.15:
                at critical_hp_flash
            elif enemy_hp <= 0.30:
                at low_hp_pulse

        # Hero HP Bar (Right)
        fixed:
            xpos config.screen_width - HP_BAR_WIDTH - 80
            ypos 200
            xsize HP_BAR_WIDTH
            ysize HP_BAR_HEIGHT

            # Background shape
            add FalchionHPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, False)

            # HP Fill with animations
            if hero_hp <= 0.15:
                add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False) at critical_hp_flash
            elif hero_hp <= 0.30:
                add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False) at low_hp_pulse
            else:
                add FalchionHPFill(HP_BAR_WIDTH, HP_BAR_HEIGHT, hero_hp, False)

            # Wave effect overlay
            add Solid("#ffffff") xsize 180 ysize HP_BAR_HEIGHT alpha 0.2 at hp_wave_hero

        # Hero HP Text
        text "[format_hp_display(hero_hp)]":
            xpos config.screen_width - 140
            ypos 300
            size 24
            color "#66aaff"
            outlines [(2, "#000000", 0, 0)]
            if hero_hp <= 0.15:
                at critical_hp_flash
            elif hero_hp <= 0.30:
                at low_hp_pulse

        # Central Round Circle
        fixed:
            xalign 0.5
            yalign 0.3
            xsize (ROUND_RADIUS + ORB_RADIUS) * 2 + 40
            ysize (ROUND_RADIUS + ORB_RADIUS) * 2 + 40

            # Round circle background
            add round_bg at round_breathe:
                xpos ROUND_RADIUS + ORB_RADIUS + 20 - ROUND_RADIUS
                ypos ROUND_RADIUS + ORB_RADIUS + 20 - ROUND_RADIUS

            # Round number display
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 0

                text "Round":
                    size 16
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]

                text "[current_round]":
                    size 36
                    color "#FFFFFF"
                    xalign 0.5
                    outlines [(2, "#000000", 0, 0)]
                    bold True

            # AP Orbs arranged around the circle
            $ center_x = ROUND_RADIUS + ORB_RADIUS + 20
            $ center_y = ROUND_RADIUS + ORB_RADIUS + 20

            for i, (x, y) in enumerate(get_orb_positions(max_ap, center_x, center_y)):
                if i < available_ap:
                    add orb_active at orb_glow xpos x ypos y
                else:
                    add orb_inactive_img at orb_inactive xpos x ypos y

# ========================
# Combat Functions
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

    def spend_ap(amount=1):
        global available_ap
        if available_ap >= amount:
            available_ap -= amount
            renpy.restart_interaction()
            return True
        return False

    def gain_ap(amount=1):
        global available_ap
        available_ap = min(max_ap, available_ap + amount)
        renpy.restart_interaction()

    def next_round():
        global current_round, available_ap
        current_round += 1
        available_ap = max_ap
        renpy.restart_interaction()

    def reset_battle():
        global enemy_hp, hero_hp, current_round, available_ap
        enemy_hp = 0.75
        hero_hp = 0.50
        current_round = 18
        available_ap = 4
        renpy.restart_interaction()

# ========================
# Demo Label
# ========================
label start:
    scene black
    show screen battle_ui

    $ enemy_hp_text = format_hp_display(enemy_hp)
    $ hero_hp_text = format_hp_display(hero_hp)

    "Battle UI - Round [current_round] | AP: [available_ap]/[max_ap]"
    "Enemy: [enemy_hp_text] | Hero: [hero_hp_text]"

    menu:
        "Attack Enemy (1 AP)" if available_ap > 0:
            if spend_ap(1):
                $ damage_enemy(0.12)
                "You attack the enemy!"
            jump start

        "Powerful Attack (2 AP)" if available_ap >= 2:
            if spend_ap(2):
                $ damage_enemy(0.25)
                "Critical hit on enemy!"
            jump start

        "Enemy Attacks":
            $ damage_hero(0.08)
            "The enemy strikes back!"
            jump start

        "Heal Self (1 AP)" if available_ap > 0:
            if spend_ap(1):
                $ heal_hero(0.15)
                "You recover some health!"
            jump start

        "Enemy Heals":
            $ heal_enemy(0.10)
            "Enemy regenerates!"
            jump start

        "Gain 1 AP" if available_ap < max_ap:
            $ gain_ap(1)
            jump start

        "Next Round":
            $ next_round()
            "Round [current_round] begins!"
            jump start

        "Reset Battle":
            $ reset_battle()
            "Battle reset!"
            jump start

        "Exit Demo":
            hide screen battle_ui
            "Demo ended."
            return
