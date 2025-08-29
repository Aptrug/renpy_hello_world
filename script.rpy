# Round UI for Ren'Py - Optimized Version

# Variables
default current_round = 59
default max_ap = 9
default available_ap = 3

# ATL Transforms
transform glow:
    alpha 1.0
    parallel:
        ease 1.0 alpha 0.8
        ease 1.0 alpha 1.0
        repeat
    parallel:
        linear 0.1 additive 0.3
        linear 0.1 additive 0.0
        repeat

transform inactive:
    alpha 0.4
    zoom 0.9

transform breathe:
    ease 3.0 zoom 1.02
    ease 3.0 zoom 1.0
    repeat

# Circle Creator
init python:
    class Circle(renpy.Displayable):
        def __init__(self, r, c, b=None, w=2, **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.r, self.c, self.b, self.w = r, c, b, w

        def render(self, width, height, st, at):
            render = renpy.Render(self.r * 2, self.r * 2)
            canvas = render.canvas()
            canvas.circle(self.c, (self.r, self.r), self.r)
            if self.b:
                canvas.circle(self.b, (self.r, self.r), self.r, self.w)
            return render

    def orb_pos(n, r=125):
        import math
        return [(125 + r * math.cos(i * 6.28 / n - 1.57) - 25,
                 125 + r * math.sin(i * 6.28 / n - 1.57) - 25) for i in range(n)]

# Images
define bg = Circle(125, (80, 80, 80), (50, 50, 50), 3)
define inner = Circle(120, (128, 128, 128))
define active = Circle(25, (255, 215, 0), (184, 134, 11), 2)
define inactive_orb = Circle(25, (102, 102, 102), (60, 60, 60), 2)

# UI Screen
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.4
        xsize 250
        ysize 250

        add bg at breathe
        add inner at breathe:
            xpos 5
            ypos 5

        vbox:
            xalign 0.5
            yalign 0.5
            spacing -5
            text "Round" size 28 color "#FFF" xalign 0.5 outlines [(2, "#000", 0, 0)]
            text "[current_round]" size 72 color "#FFF" xalign 0.5 outlines [(2, "#000", 0, 0)]

        $ pos = orb_pos(max_ap)
        for i, (x, y) in enumerate(pos):
            if i < available_ap:
                add active at glow:
                    xpos x
                    ypos y
            else:
                add inactive_orb at inactive:
                    xpos x
                    ypos y

# Functions
init python:
    def update_round(r):
        global current_round
        current_round = r
        renpy.restart_interaction()

    def update_ap(a, m=None):
        global available_ap, max_ap
        if m: max_ap = max(1, m)
        available_ap = max(0, min(a, max_ap))
        renpy.restart_interaction()

    def spend_ap(a=1):
        global available_ap
        if available_ap >= a:
            available_ap -= a
            renpy.restart_interaction()
            return True
        return False

    def gain_ap(a=1):
        global available_ap
        available_ap = min(max_ap, available_ap + a)
        renpy.restart_interaction()

# Demo
label start:
    show screen round_ui
    "Round [current_round], AP: [available_ap]/[max_ap]"

    menu:
        "Spend AP" if available_ap > 0:
            $ spend_ap()
            "AP: [available_ap]/[max_ap]"
            jump start
        "Gain AP" if available_ap < max_ap:
            $ gain_ap()
            "AP: [available_ap]/[max_ap]"
            jump start
        "Next Round":
            $ update_round(current_round + 1)
            $ update_ap(max_ap)
            "Round [current_round]! AP: [available_ap]/[max_ap]"
            jump start
        "Max AP: 6":
            $ update_ap(available_ap, 6)
            jump start
        "Max AP: 12":
            $ update_ap(available_ap, 12)
            jump start
        "Exit":
            return
