# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

default hero_hp = 0.5      # 50%
default enemy_hp = 0.7      # 70%

define ROUND_RADIUS = 70
define ORB_RADIUS = 15
define BAR_WIDTH = 300
define BAR_HEIGHT = 40

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

transform orb_inactive:
    alpha 0.4
    zoom 0.9

transform hp_wave_left:
    xalign 0.0
    linear 1.5 xoffset 30
    linear 1.5 xoffset 0
    repeat

transform hp_wave_right:
    xalign 1.0
    linear 1.5 xoffset -30
    linear 1.5 xoffset 0
    repeat

transform low_hp:
    ease 0.6 alpha 0.5
    ease 0.6 alpha 1.0
    repeat

# ========================
# Circle Displayable
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
    def get_orb_positions(num_orbs):
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = ROUND_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
            y = ROUND_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# ========================
# Gradient Bar Helper
# ========================
screen gradient_bar(width, height, color1, color2):
    fixed:
        xsize width
        ysize height
        add Solid(color1) xysize (width, height//2)
        add Solid(color2) xysize (width, height//2) ypos height//2

# ========================
# Main UI Screen
# ========================
screen round_ui():
    hbox:
        xalign 0.5
        yalign 0.75
        spacing 80

        # --- Hero HP Bar (Left) ---
        fixed:
            xsize BAR_WIDTH
            ysize BAR_HEIGHT
            add Screen("gradient_bar", BAR_WIDTH, BAR_HEIGHT, "#3282FF", "#143CC8") xsize int(hero_hp*BAR_WIDTH) at hp_wave_left
            if hero_hp <= 0.3:
                add Screen("gradient_bar", BAR_WIDTH, BAR_HEIGHT, "#3282FF", "#143CC8") xsize int(hero_hp*BAR_WIDTH) at low_hp

        # --- Round Circle ---
        fixed:
            xsize ROUND_RADIUS*2
            ysize ROUND_RADIUS*2
            add round_bg

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

        # --- Enemy HP Bar (Right) ---
        fixed:
            xsize BAR_WIDTH
            ysize BAR_HEIGHT
            add Screen("gradient_bar", BAR_WIDTH, BAR_HEIGHT, "#FF5050", "#C81E1E") xpos (BAR_WIDTH - int(enemy_hp*BAR_WIDTH)) xsize int(enemy_hp*BAR_WIDTH) at hp_wave_right
            if enemy_hp <= 0.3:
                add Screen("gradient_bar", BAR_WIDTH, BAR_HEIGHT, "#FF5050", "#C81E1E") xpos (BAR_WIDTH - int(enemy_hp*BAR_WIDTH)) xsize int(enemy_hp*BAR_WIDTH) at low_hp

# ========================
# Demo
# ========================
label start:
    show screen round_ui

    "Round UI Demo: Round [current_round], AP [available_ap]/[max_ap]"

    menu:
        "Damage Hero":
            $ hero_hp = max(0, hero_hp - 0.1)
            jump start
        "Damage Enemy":
            $ enemy_hp = max(0, enemy_hp - 0.1)
            jump start
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start
        "Exit":
            return
