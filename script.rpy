# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

default enemy_hp = 0.75
default hero_hp = 0.50

define ROUND_RADIUS = 70
define ORB_RADIUS = 15
define HP_WIDTH = 400
define HP_HEIGHT = 80

# ========================
# Shaders
# ========================
init python:
    renpy.register_shader(
        "custom.horizontal_gradient",
        variables="""
            uniform vec4 u_color_start;
            uniform vec4 u_color_mid;
            uniform vec4 u_color_end;
            uniform vec2 u_model_size;
        """,
        fragment_300="""
            float t = gl_FragCoord.x / u_model_size.x;
            vec4 color;
            if (t < 0.5) {
                color = mix(u_color_start, u_color_mid, t * 2.0);
            } else {
                color = mix(u_color_mid, u_color_end, (t - 0.5) * 2.0);
            }
            gl_FragColor = color;
        """
    )

    renpy.register_shader(
        "custom.wave_gradient",
        variables="""
            uniform vec2 u_model_size;
        """,
        fragment_300="""
            float t = gl_FragCoord.x / u_model_size.x;
            float a = 0.0;
            if (t < 0.15) {
                a = t / 0.15 * 0.1;
            } else if (t < 0.30) {
                a = 0.1 + (t - 0.15) / 0.15 * 0.2;
            } else if (t < 0.45) {
                a = 0.3 + (t - 0.30) / 0.15 * 0.4;
            } else if (t < 0.50) {
                a = 0.7 + (t - 0.45) / 0.05 * 0.2;
            } else if (t < 0.55) {
                a = 0.9 + (t - 0.50) / 0.05 * (-0.2);
            } else if (t < 0.70) {
                a = 0.7 + (t - 0.55) / 0.15 * (-0.4);
            } else if (t < 0.85) {
                a = 0.3 + (t - 0.70) / 0.15 * (-0.2);
            } else {
                a = 0.1 + (t - 0.85) / 0.15 * (-0.1);
            }
            gl_FragColor = vec4(1.0, 1.0, 1.0, a);
        """
    )

# ========================
# Custom Displayables
# ========================
init python:
    import math

    class ShapeMask(renpy.Displayable):
        def __init__(self, points, width, height, **kwargs):
            super(ShapeMask, self).__init__(**kwargs)
            self.points = points
            self.width = width
            self.height = height

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()
            c.polygon("#ffffffff", self.points, 0)
            return r

    class HpContainer(renpy.Displayable):
        def __init__(self, is_hero, hp, width=HP_WIDTH, height=HP_HEIGHT, **kwargs):
            super(HpContainer, self).__init__(**kwargs)
            self.is_hero = is_hero
            self.hp = hp
            self.width = width
            self.height = height
            self.wave_duration = max(0.4, 3 * self.hp)

            if self.is_hero:
                points_perc = [
                    (1.00, 0.65), (0.35, 0.65), (0.25, 0.55), (0.18, 0.40), (0.12, 0.25),
                    (0.08, 0.15), (0.04, 0.08), (0.00, 0.05), (0.02, 0.20), (0.06, 0.35),
                    (0.12, 0.50), (0.18, 0.65), (0.25, 0.75), (0.35, 0.82), (1.00, 0.82)
                ]
                self.start_color = "#003399"
                self.mid_color = "#4499ff"
                self.end_color = "#66aaff"
                self.fill_align = (1.0, 0.0)
            else:
                points_perc = [
                    (0.00, 0.35), (0.65, 0.35), (0.75, 0.45), (0.82, 0.60), (0.88, 0.75),
                    (0.92, 0.85), (0.96, 0.92), (1.00, 0.95), (0.98, 0.80), (0.94, 0.65),
                    (0.88, 0.50), (0.82, 0.35), (0.75, 0.25), (0.65, 0.18), (0.00, 0.18)
                ]
                self.start_color = "#cc0000"
                self.mid_color = "#ff4444"
                self.end_color = "#ff6666"
                self.fill_align = (0.0, 0.0)

            self.points = [(int(p[0] * width), int(p[1] * height)) for p in points_perc]
            self.shape_mask = ShapeMask(self.points, width, height)

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Background
            c.polygon("#1a1a1a", self.points, 0)
            c.polygon("#ffffff26", self.points, 2)  # rgba(255,255,255,0.15) approx

            # Calculate fill width
            fill_width = int(self.hp * self.width)

            # Wave position and alpha
            t = (st % self.wave_duration) / self.wave_duration
            wave_alpha = 0.0
            if t < 0.1:
                wave_alpha = t / 0.1
            elif t > 0.9:
                wave_alpha = (1.0 - t) / 0.1
            else:
                wave_alpha = 1.0

            if self.is_hero:
                wave_pos = -180 + t * (self.width + 360)
            else:
                wave_pos = self.width + 180 - t * (self.width + 360)

            # Fill gradient model
            gradient_model = Model().shader(
                "custom.horizontal_gradient",
                u_color_start=self.start_color,
                u_color_mid=self.mid_color,
                u_color_end=self.end_color
            )

            # Wave model
            wave_model = Model().shader("custom.wave_gradient")

            # Fill inner (gradient + wave)
            fill_inner = Fixed(
                xsize=fill_width,
                ysize=self.height,
                Transform(gradient_model, xsize=fill_width, ysize=self.height, xalign=0.0, yalign=0.0),
                Transform(wave_model, xsize=180, ysize=self.height, xpos=wave_pos, alpha=wave_alpha)
            )

            # Fill base
            fill_base = Fixed(
                xsize=self.width,
                ysize=self.height,
                Transform(fill_inner, xalign=self.fill_align[0], yalign=self.fill_align[1])
            )

            # Masked fill
            masked_fill = AlphaMask(fill_base, self.shape_mask)

            # Place masked fill
            r.place(masked_fill, 0, 0)

            return r

        def event(self, ev, x, y, st):
            if st is None:
                return None
            return 0.033  # Redraw ~30fps for animation

        def visit(self):
            return []

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

transform low_hp:
    matrixcolor Brightness(1.0)
    ease 1.5 matrixcolor Brightness(1.4)
    repeat

transform critical_hp:
    alpha 0.8
    ease 0.6 alpha 1.0
    repeat

transform low_hp_text:
    zoom 1.0
    ease 1.2 zoom 1.05
    repeat

transform critical_hp_text:
    zoom 1.0 alpha 0.9
    ease 0.8 zoom 1.1 alpha 1.0
    repeat

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, "#505050", "#323232", 3)
define orb_active = Circle(ORB_RADIUS, "#ffd700", "#b8860b", 2)
define orb_inactive_img = Circle(ORB_RADIUS, "#666666", "#3c3c3c", 2)

# ========================
# Main UI Screen
# ========================
screen battle_ui():
    hbox:
        xalign 0.5
        yalign 0.75
        spacing 30

        # Enemy HP
        vbox:
            xsize HP_WIDTH
            spacing 8
            align (0.5, 0.5)

            text "{:d}%".format(int(enemy_hp * 100)):
                xalign 0.0
                color "#ff6666"
                size 18
                bold True
                outlines [(1, "#000000", 0, 0)]
                at (critical_hp_text if enemy_hp <= 0.15 else low_hp_text if enemy_hp <= 0.3 else None)

            add HpContainer(False, enemy_hp, HP_WIDTH, HP_HEIGHT):
                at (critical_hp if enemy_hp <= 0.15 else low_hp if enemy_hp <= 0.3 else None)

        # Round UI
        fixed:
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
                add (orb_active if i < available_ap else orb_inactive_img) xpos x ypos y at (orb_glow if i < available_ap else orb_inactive)

        # Hero HP
        vbox:
            xsize HP_WIDTH
            spacing 8
            align (0.5, 0.5)

            add HpContainer(True, hero_hp, HP_WIDTH, HP_HEIGHT):
                at (critical_hp if hero_hp <= 0.15 else low_hp if hero_hp <= 0.3 else None)

            text "{:d}%".format(int(hero_hp * 100)):
                xalign 1.0
                color "#66aaff"
                size 18
                bold True
                outlines [(1, "#000000", 0, 0)]
                at (critical_hp_text if hero_hp <= 0.15 else low_hp_text if hero_hp <= 0.3 else None)

# ========================
# Demo Label
# ========================
label start:
    show screen battle_ui

    "Battle UI Demo: Round [current_round], AP [available_ap]/[max_ap], Enemy HP [enemy_hp:.0%], Hero HP [hero_hp:.0%]"

    menu:
        "Damage Enemy" if enemy_hp > 0:
            $ enemy_hp = max(0, enemy_hp - renpy.random.uniform(0.02, 0.05))
            jump start

        "Damage Hero" if hero_hp > 0:
            $ hero_hp = max(0, hero_hp - renpy.random.uniform(0.02, 0.05))
            jump start

        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start

        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start

        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            $ enemy_hp = renpy.random.uniform(0.6, 1.0)
            $ hero_hp = renpy.random.uniform(0.6, 1.0)
            jump start

        "Exit":
            return
