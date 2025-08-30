# script.rpy
# Falchion HP Bars + Round Orb UI
# Paste this into your project (script.rpy). Adjust sizes/colors as needed.

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3

default enemy_hp = 0.75
default hero_hp  = 0.50

define ROUND_RADIUS = 70
define ORB_RADIUS = 15

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

# ========================
# Python Helpers & Displayables
# ========================
init python:
    import math, renpy

    # --- Circle Displayable for orbs / round background ---
    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.radius = int(radius)
            self.color = color
            self.border_color = border_color
            self.border_width = int(border_width)

        def render(self, w, h, st, at):
            size = self.radius * 2
            r = renpy.Render(size, size)
            c = r.canvas()

            # fill circle
            if self.color:
                try:
                    c.circle(self.color, (self.radius, self.radius), self.radius)
                except Exception:
                    # Fallback drawing if circle isn't available: use polygon approximation
                    steps = 32
                    pts = []
                    for i in range(steps):
                        ang = 2.0 * math.pi * i / steps
                        pts.append((self.radius + int(math.cos(ang)*self.radius),
                                    self.radius + int(math.sin(ang)*self.radius)))
                    c.polygon(self.color, pts)

            # border
            if self.border_color and self.border_width > 0:
                try:
                    c.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
                except Exception:
                    # fallback: approximate border
                    c.polygon(self.border_color, [(0,0),(size,0),(size,size),(0,size)], width=self.border_width)

            return r

    def get_orb_positions(num_orbs):
        """
        Returns orb positions arranged evenly in a circle around ROUND_RADIUS.
        Positions are (x, y) relative to top-left of the ROUND_RADIUS*2 area.
        """
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            x = ROUND_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
            y = ROUND_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

# define round/orb Displayables
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# ========================
# HPBar Displayable (falchion-like)
# ========================
init python:
    # basic lerp helpers
    def lerp(a, b, t):
        return a + (b - a) * t

    def lerp_color(c1, c2, t):
        return (int(lerp(c1[0], c2[0], t)),
                int(lerp(c1[1], c2[1], t)),
                int(lerp(c1[2], c2[2], t)))

    class HPBar(renpy.Displayable):
        """
        HPBar(width, height, get_hp=lambda:1.0, color_from=(r,g,b), color_to=(r,g,b), bg_color, side)
        get_hp must be a callable returning a float 0.0..1.0
        side: 'left' or 'right' (affects angled end)
        """
        def __init__(self, width=360, height=68, get_hp=lambda:1.0,
                     color_from=(204,0,0), color_to=(255,102,102),
                     bg_color=(18,18,18), border_color=(60,60,60),
                     side='left', **kwargs):
            super(HPBar, self).__init__(**kwargs)
            self.width = int(width)
            self.height = int(height)
            self.get_hp = get_hp
            self.color_from = color_from
            self.color_to = color_to
            self.bg_color = bg_color
            self.border_color = border_color
            self.side = side
            self.wave_width = int(self.width * 0.18)
            self.strip_count = 28

        def render(self, w, h, st, at):
            w = self.width
            h = self.height
            r = renpy.Render(w, h)
            c = r.canvas()

            # fetch hp safely
            try:
                hp = float(self.get_hp())
            except Exception:
                hp = 0.0
            hp = max(0.0, min(1.0, hp))

            # base background
            try:
                c.rect(self.bg_color, (0,0), (w,h))
            except Exception:
                # fallback: fill polygon
                c.polygon(self.bg_color, [(0,0),(w,0),(w,h),(0,h)])

            # border (simple)
            try:
                c.polygon(self.border_color, [(0,0),(w,0),(w,h),(0,h)], width=2)
            except Exception:
                pass

            # compute fill width
            fill_w = int(w * hp)

            # gradient-like fill using strips
            if fill_w > 0:
                for i in range(self.strip_count):
                    x0 = int(i * fill_w / self.strip_count)
                    x1 = int((i + 1) * fill_w / self.strip_count)
                    t = (i + 0.5) / max(1, self.strip_count)
                    color = lerp_color(self.color_from, self.color_to, t)
                    try:
                        c.rect(color, (x0, 0), (x1 - x0, h))
                    except Exception:
                        c.polygon(color, [(x0,0),(x1,0),(x1,h),(x0,h)])

                # subtle top highlight
                highlight_h = int(h * 0.18)
                try:
                    c.rect((255,255,255,30), (0,0), (fill_w, highlight_h))
                except Exception:
                    pass

            # angled falchion-ish triangle tail (approximation)
            slash_width = int(h * 0.6)
            try:
                if self.side == 'left':
                    # angled tail on right of fill
                    if fill_w > 0:
                        poly = [(fill_w, 0), (min(w, fill_w + slash_width), int(h / 2)), (fill_w, h)]
                        c.polygon((255,255,255,30), poly)
                else:
                    # angled tail on left (mirror)
                    if fill_w > 0:
                        poly = [(w - fill_w, 0), (max(0, w - fill_w - slash_width), int(h / 2)), (w - fill_w, h)]
                        c.polygon((255,255,255,30), poly)
            except Exception:
                pass

            # wave highlight animation (uses 'st' for continuous animation)
            if fill_w > 0:
                speed = max(30.0, 80.0 * (0.4 + hp))
                wave_total = fill_w + self.wave_width + 8
                wave_x = int(((st * speed) % (wave_total)) - self.wave_width)
                band_w = self.wave_width
                if wave_x < fill_w:
                    # draw band clipped to fill_w
                    band_w_eff = min(band_w, max(0, fill_w - max(0, wave_x)))
                    if band_w_eff > 0:
                        try:
                            c.rect((255,255,255,60), (max(0, wave_x), 0), (band_w_eff, h))
                        except Exception:
                            pass

            # low / critical pulsing overlay
            try:
                if hp <= 0.15:
                    pulse = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(st * 10.0))
                    glow_color = (255, 80, 80, int(120 * pulse))
                    c.polygon(glow_color, [(0,0),(w,0),(w,h),(0,h)])
                elif hp <= 0.30:
                    pulse = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(st * 3.0))
                    glow_color = (255, 140, 140, int(80 * pulse))
                    c.polygon(glow_color, [(0,0),(w,0),(w,h),(0,h)])
            except Exception:
                pass

            return r

    # small wrappers to pass into HPBar
    def get_enemy_hp():
        return enemy_hp

    def get_hero_hp():
        return hero_hp

# ========================
# Round UI Screen (center orb, left/right HP bars)
# ========================
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.5

        hbox:
            spacing 24
            xalign 0.5
            yalign 0.5

            # LEFT HP (enemy)
            add HPBar(width=360, height=68, get_hp=get_enemy_hp,
                    color_from=(204,0,0), color_to=(255,102,102),
                    bg_color=(16,16,16), border_color=(50,50,50), side='left')

            # Center round orb area
            frame:
                xsize ROUND_RADIUS*2
                ysize ROUND_RADIUS*2
                background None

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

                # Orbs arranged around the circle
                for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                    if i < available_ap:
                        add orb_active at orb_glow xpos x ypos y
                    else:
                        add orb_inactive_img at orb_inactive xpos x ypos y

            # RIGHT HP (hero)
            add HPBar(width=360, height=68, get_hp=get_hero_hp,
                    color_from=(0,51,153), color_to=(102,170,255),
                    bg_color=(16,16,16), border_color=(50,50,50), side='right')

# ========================
# Demo label / Start
# ========================
label start:
    # Show the Round UI by default
    show screen round_ui

    "Round UI Demo — Round [current_round], AP [available_ap]/[max_ap]."

    menu:
        "Damage enemy":
            $ enemy_hp = max(0.0, enemy_hp - 0.12)
            jump start

        "Heal enemy":
            $ enemy_hp = min(1.0, enemy_hp + 0.12)
            jump start

        "Damage hero":
            $ hero_hp = max(0.0, hero_hp - 0.12)
            jump start

        "Heal hero":
            $ hero_hp = min(1.0, hero_hp + 0.12)
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
            jump start

        "Exit":
            hide screen round_ui
            return
