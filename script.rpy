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
define HP_BAR_BORDER = 3

# ========================
# ATL Transforms
# ========================
transform orb_glow:
    parallel:
        ease 1.2 alpha 0.7
        ease 1.2 alpha 1.0
    parallel:
        ease 0.8 zoom 0.95
        ease 0.8 zoom 1.0
    repeat

transform round_breathe:
    parallel:
        ease 2.5 zoom 1.03
        ease 2.5 zoom 1.0
    parallel:
        ease 3.0 alpha 0.9
        ease 3.0 alpha 1.0
    repeat

transform orb_inactive:
    alpha 0.3
    zoom 0.85

transform hp_wave_enemy:
    xpos -180
    alpha 0.0
    ease 0.5 alpha 0.4
    linear 2.0 xpos HP_BAR_WIDTH
    ease 0.5 alpha 0.0
    pause 1.0
    repeat

transform hp_wave_hero:
    xpos HP_BAR_WIDTH + 180
    alpha 0.0
    ease 0.5 alpha 0.4
    linear 2.0 xpos -180
    ease 0.5 alpha 0.0
    pause 1.0
    repeat

transform low_hp_pulse:
    ease 1.0 alpha 0.8
    ease 1.0 alpha 1.0
    repeat

transform critical_hp_flash:
    ease 0.4 alpha 0.7
    ease 0.4 alpha 1.0
    repeat

transform vs_glow:
    parallel:
        ease 2.0 alpha 0.85
        ease 2.0 alpha 1.0
    parallel:
        linear 0.2 additive 0.1
        linear 0.2 additive 0.0
    repeat

# ========================
# Python Helpers
# ========================
init python:
    import math

    class RoundedRect(renpy.Displayable):
        def __init__(self, width, height, color, border_color=None, border_width=2, corner_radius=8, **kwargs):
            super(RoundedRect, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.color = color
            self.border_color = border_color
            self.border_width = border_width
            self.corner_radius = corner_radius

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Draw main rounded rectangle
            if self.color:
                c.rect(self.color, (0, 0, self.width, self.height))

            # Draw border if specified
            if self.border_color and self.border_width > 0:
                c.rect(self.border_color, (0, 0, self.width, self.height), self.border_width)

            return r

    class GradientRect(renpy.Displayable):
        def __init__(self, width, height, color_start, color_end, **kwargs):
            super(GradientRect, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.color_start = color_start
            self.color_end = color_end

        def render(self, width, height, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Simple gradient simulation with multiple rectangles
            steps = 20
            for i in range(steps):
                factor = float(i) / (steps - 1)
                r_val = int(self.color_start[0] * (1-factor) + self.color_end[0] * factor)
                g_val = int(self.color_start[1] * (1-factor) + self.color_end[1] * factor)
                b_val = int(self.color_start[2] * (1-factor) + self.color_end[2] * factor)

                rect_height = self.height // steps
                y_pos = i * rect_height
                c.rect((r_val, g_val, b_val), (0, y_pos, self.width, rect_height))

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
            c = r.canvas()

            if self.color:
                c.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                c.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return r

    def get_orb_positions(num_orbs, radius=ROUND_RADIUS):
        """Returns orb positions arranged evenly in a circle."""
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = radius + radius * 0.8 * math.cos(angle) - ORB_RADIUS
            y = radius + radius * 0.8 * math.sin(angle) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

    def format_hp_percent(hp_value):
        """Format HP as percentage for display."""
        return str(int(hp_value * 100)) + "%"

    def get_hp_color(hp_ratio, is_enemy=True):
        """Get HP bar color based on current HP ratio."""
        if hp_ratio <= 0.15:
            return (255, 100, 100) if is_enemy else (100, 150, 255)
        elif hp_ratio <= 0.30:
            return (204, 0, 0) if is_enemy else (0, 51, 153)
        else:
            return (170, 0, 0) if is_enemy else (0, 100, 200)

# ========================
# UI Elements
# ========================
define round_bg = Circle(ROUND_RADIUS, (60, 60, 60), (40, 40, 40), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (200, 150, 0), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (80, 80, 80), (50, 50, 50), 2)

# ========================
# HP Bar Components
# ========================
screen hp_bar_enemy():
    fixed:
        xpos 100
        ypos 200
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT + 100

        # HP Bar Background
        add RoundedRect(HP_BAR_WIDTH, HP_BAR_HEIGHT, (25, 25, 25), (100, 100, 100), HP_BAR_BORDER, 6)

        # HP Fill
        $ fill_width = int(HP_BAR_WIDTH * enemy_hp)
        if fill_width > 0:
            fixed:
                xpos HP_BAR_BORDER
                ypos HP_BAR_BORDER
                xsize fill_width - (HP_BAR_BORDER * 2)
                ysize HP_BAR_HEIGHT - (HP_BAR_BORDER * 2)

                $ hp_color = get_hp_color(enemy_hp, True)

                if enemy_hp <= 0.15:
                    add GradientRect(fill_width - (HP_BAR_BORDER * 2), HP_BAR_HEIGHT - (HP_BAR_BORDER * 2), hp_color, (255, 150, 150)) at critical_hp_flash
                elif enemy_hp <= 0.30:
                    add GradientRect(fill_width - (HP_BAR_BORDER * 2), HP_BAR_HEIGHT - (HP_BAR_BORDER * 2), hp_color, (255, 100, 100)) at low_hp_pulse
                else:
                    add GradientRect(fill_width - (HP_BAR_BORDER * 2), HP_BAR_HEIGHT - (HP_BAR_BORDER * 2), hp_color, (255, 80, 80))

                # Wave effect
                add Solid("#ffffff") alpha 0.15 xsize 120 ysize HP_BAR_HEIGHT - (HP_BAR_BORDER * 2) at hp_wave_enemy

        # HP Text with backdrop
        $ hp_text = format_hp_percent(enemy_hp)
        fixed:
            xpos HP_BAR_WIDTH - 80
            ypos -40
            xsize 70
            ysize 30

            add RoundedRect(70, 30, (0, 0, 0, 180), (255, 100, 100), 1, 15)
            text "[hp_text]" color "#ff6666" size 20 bold True:
                xalign 0.5
                yalign 0.5
                outlines [(2, "#000000", 0, 0)]

screen hp_bar_hero():
    fixed:
        xpos config.screen_width - HP_BAR_WIDTH - 100
        ypos 200
        xsize HP_BAR_WIDTH
        ysize HP_BAR_HEIGHT + 100

        # HP Bar Background
        add RoundedRect(HP_BAR_WIDTH, HP_BAR_HEIGHT, (25, 25, 25), (100, 100, 100), HP_BAR_BORDER, 6)

        # HP Fill (right-aligned)
        $ fill_width = int(HP_BAR_WIDTH * hero_hp)
        if fill_width > 0:
            fixed:
                xpos HP_BAR_WIDTH - fill_width + HP_BAR_BORDER
                ypos HP_BAR_BORDER
                xsize fill_width - (HP_BAR_BORDER * 2)
                ysize HP_BAR_HEIGHT - (HP_BAR_BORDER * 2)

                $ hp_color = get_hp_color(hero_hp, False)

                if hero_hp <= 0.15:
                    add GradientRect(fill_width - (HP_BAR_BORDER * 2), HP_BAR_HEIGHT - (HP_BAR_BORDER * 2), hp_color, (150, 200, 255)) at critical_hp_flash
                elif hero_hp <= 0.30:
                    add GradientRect(fill_width - (HP_BAR_BORDER * 2), HP_BAR_HEIGHT - (HP_BAR_BORDER * 2), hp_color, (100, 180, 255)) at low_hp_pulse
                else:
                    add GradientRect(fill_width - (HP_BAR_BORDER * 2), HP_BAR_HEIGHT - (HP_BAR_BORDER * 2), hp_color, (80, 160, 255))

                # Wave effect
                add Solid("#ffffff") alpha 0.15 xsize 120 ysize HP_BAR_HEIGHT - (HP_BAR_BORDER * 2) at hp_wave_hero

        # HP Text with backdrop
        $ hp_text = format_hp_percent(hero_hp)
        fixed:
            xpos 10
            ypos HP_BAR_HEIGHT + 10
            xsize 70
            ysize 30

            add RoundedRect(70, 30, (0, 0, 0, 180), (100, 150, 255), 1, 15)
            text "[hp_text]" color "#66aaff" size 20 bold True:
                xalign 0.5
                yalign 0.5
                outlines [(2, "#000000", 0, 0)]

# ========================
# Central Round Circle
# ========================
screen round_circle():
    fixed:
        xalign 0.5
        yalign 0.25
        xsize (ROUND_RADIUS + 30) * 2
        ysize (ROUND_RADIUS + 30) * 2

        # Outer glow circle
        add Circle(ROUND_RADIUS + 8, (255, 204, 0, 80)) at vs_glow

        # Main round background
        add Circle(ROUND_RADIUS, (80, 80, 80), (200, 150, 0), 4) at round_breathe

        # Round text
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
                outlines [(3, "#000000", 0, 0)]
                bold True

        # AP Orbs around the circle
        for i, (x, y) in enumerate(get_orb_positions(max_ap, ROUND_RADIUS + 30)):
            if i < available_ap:
                add orb_active at orb_glow xpos x ypos y
            else:
                add orb_inactive_img at orb_inactive xpos x ypos y

# ========================
# Main Battle UI Screen
# ========================
screen battle_ui():
    modal False

    # Dark overlay background
    add Solid("#000000") alpha 0.3

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

    def spend_ap():
        global available_ap
        if available_ap > 0:
            available_ap -= 1
            renpy.restart_interaction()

    def gain_ap():
        global available_ap
        if available_ap < max_ap:
            available_ap += 1
            renpy.restart_interaction()

# ========================
# Demo Label
# ========================
label start:
    scene black
    show screen battle_ui

    $ enemy_hp_display = format_hp_percent(enemy_hp)
    $ hero_hp_display = format_hp_percent(hero_hp)

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap]"
    "Enemy HP: [enemy_hp_display] | Hero HP: [hero_hp_display]"

    menu:
        "Attack Enemy" if available_ap > 0:
            $ spend_ap()
            $ damage_enemy(0.12)
            "You strike the enemy! They take damage."
            jump start

        "Enemy Attack" if available_ap > 0:
            $ spend_ap()
            $ damage_hero(0.08)
            "The enemy retaliates and hits you!"
            jump start

        "Heal Enemy (10%)":
            $ heal_enemy(0.10)
            "Enemy recovers some health."
            jump start

        "Heal Hero (10%)":
            $ heal_hero(0.10)
            "You recover some health."
            jump start

        "Gain AP" if available_ap < max_ap:
            $ gain_ap()
            "You gain an Action Point."
            jump start

        "Next Round":
            $ next_round()
            "Round [current_round] begins!"
            jump start

        "Reset Battle":
            $ enemy_hp = 0.75
            $ hero_hp = 0.50
            $ available_ap = 4
            $ current_round = 18
            "Battle state reset."
            jump start

        "Exit Demo":
            hide screen battle_ui
            "Demo ended."
            return
