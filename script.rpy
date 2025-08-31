# I want you to add an HP bar to the top left and make it look exactly like Witcher 3 HP bar

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3
default current_hp = 85
default max_hp = 100
define ROUND_RADIUS = 70
define ORB_RADIUS = 15
define AURA_PADDING = 50
define AURA_BLUR = 20
define AURA_BORDER_WIDTH = 4
define UI_SIZE = 2 * (ROUND_RADIUS + AURA_PADDING)

# HP Bar defines (Witcher 3 style)
define HP_BAR_WIDTH = 200
define HP_BAR_HEIGHT = 12
define HP_BAR_BORDER = 2

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
transform aura_glow:
    ease 3.0 zoom 1.05 alpha 0.4
    ease 3.0 zoom 1.0 alpha 0.6
    repeat
transform orb_inactive:
    alpha 0.4
    zoom 0.9

transform hp_pulse:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0

# ========================
# Python Helpers
# ========================
init python:
    import math
    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, padding=0, **kwargs):
            super().__init__(**kwargs)
            self.radius, self.color = radius, color
            self.border_color, self.border_width = border_color, border_width
            self.padding = padding
        def render(self, w, h, st, at):
            size = 2 * (self.radius + self.padding)
            r = renpy.Render(size, size)
            c = r.canvas()
            center = self.radius + self.padding
            if self.color:
                c.circle(self.color, (center, center), self.radius)
            if self.border_color:
                c.circle(self.border_color, (center, center), self.radius, self.border_width)
            return r

    class WitcherHealthBar(renpy.Displayable):
        def __init__(self, width, height, border_width=2, **kwargs):
            super().__init__(**kwargs)
            self.width = width
            self.height = height
            self.border_width = border_width

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Calculate HP percentage
            hp_percent = current_hp / float(max_hp)
            fill_width = int((self.width - 2 * self.border_width) * hp_percent)

            # Draw outer dark border (black/dark gray)
            c.rect("#1a1a1a", (0, 0, self.width, self.height))

            # Draw inner border (darker red/brown)
            c.rect("#2d1810", (self.border_width, self.border_width,
                              self.width - 2 * self.border_width,
                              self.height - 2 * self.border_width))

            # Draw HP fill (red gradient effect)
            if fill_width > 0:
                # Main red fill
                c.rect("#c41e3a", (self.border_width, self.border_width,
                                  fill_width, self.height - 2 * self.border_width))

                # Highlight on top edge for 3D effect
                if fill_width > 2:
                    c.rect("#ff4d6d", (self.border_width, self.border_width,
                                      fill_width, 2))

                # Dark shadow on bottom edge
                if fill_width > 2:
                    c.rect("#8b0000", (self.border_width, self.height - self.border_width - 2,
                                      fill_width, 2))

            renpy.redraw(self, 0.1)  # Redraw to update HP changes
            return r

    def get_orb_positions(num_orbs, center_x, center_y, orbit_radius):
        """
        Returns orb top-left positions arranged evenly in a circle around the center.
        """
        positions = []
        for i in range(num_orbs):
            angle = 2 * math.pi * i / num_orbs - math.pi/2
            orb_center_x = center_x + orbit_radius * math.cos(angle)
            orb_center_y = center_y + orbit_radius * math.sin(angle)
            x = orb_center_x - ORB_RADIUS
            y = orb_center_y - ORB_RADIUS
            positions.append((int(x), int(y)))
        return positions

# ========================
# Circle Definitions
# ========================
define round_bg = Circle(ROUND_RADIUS, (80, 80, 80), (50, 50, 50), 3)
define glow_source = Circle(ROUND_RADIUS, None, "#ffffff", AURA_BORDER_WIDTH, padding=AURA_PADDING)
define orb_active = Circle(ORB_RADIUS, (255, 215, 0), (184, 134, 11), 2)
define orb_inactive_img = Circle(ORB_RADIUS, (102, 102, 102), (60, 60, 60), 2)

# Witcher 3 HP Bar
define witcher_hp_bar = WitcherHealthBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, HP_BAR_BORDER)

# ========================
# Witcher 3 HP Bar Screen
# ========================
screen witcher_hp_bar():
    # HP Bar container in top left
    fixed:
        xpos 30
        ypos 30
        xsize HP_BAR_WIDTH + 100
        ysize 60

        # HP Bar background frame (medieval style border)
        add Solid("#0f0f0f"):
            xsize HP_BAR_WIDTH + 8
            ysize HP_BAR_HEIGHT + 8
            xpos -4
            ypos 16

        # Decorative corners (simple medieval style)
        add Solid("#3d2914"):
            xsize 6
            ysize 6
            xpos -7
            ypos 13
        add Solid("#3d2914"):
            xsize 6
            ysize 6
            xpos HP_BAR_WIDTH + 5
            ypos 13
        add Solid("#3d2914"):
            xsize 6
            ysize 6
            xpos -7
            ypos HP_BAR_HEIGHT + 17
        add Solid("#3d2914"):
            xsize 6
            ysize 6
            xpos HP_BAR_WIDTH + 5
            ypos HP_BAR_HEIGHT + 17

        # Main HP Bar
        add witcher_hp_bar:
            xpos 0
            ypos 20
            at hp_pulse

        # HP Text (Witcher 3 style font positioning)
        text "[current_hp]":
            size 16
            color "#ffffff"
            xpos HP_BAR_WIDTH + 15
            ypos 18
            outlines [(1, "#000000", 0, 0)]
            font "gui/font/DejaVuSans.ttf"

        # HP Icon (simple red cross/heart symbol)
        text "♥":
            size 20
            color "#c41e3a"
            xpos -25
            ypos 16
            outlines [(1, "#000000", 0, 0)]

# ========================
# Main UI Screen
# ========================
screen round_ui():
    add Solid("#808080")  # Gray color in hex

    # Show the Witcher 3 HP bar
    use witcher_hp_bar

    fixed:
        xalign 0.5
        yalign 0.75
        xsize UI_SIZE
        ysize UI_SIZE
        # Golden aura
        add glow_source:
            align (0.5, 0.5)
            matrixcolor TintMatrix("#ffd700")
            blur AURA_BLUR
            additive 1.0
            at aura_glow
        # Round circle background (static)
        add round_bg align (0.5, 0.5)
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
        # Orbs arranged around the circle
        $ center = UI_SIZE / 2
        for i, (x, y) in enumerate(get_orb_positions(max_ap, center, center, ROUND_RADIUS)):
            add (orb_active if i < available_ap else orb_inactive_img) at (orb_glow if i < available_ap else orb_inactive) xpos x ypos y

# ========================
# Demo Label
# ========================
label start:
    show screen round_ui
    "Round UI Demo: Round [current_round], AP [available_ap]/[max_ap], HP [current_hp]/[max_hp]"
    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start
        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start
        "Take Damage" if current_hp > 0:
            $ current_hp = max(0, current_hp - 15)
            jump start
        "Heal" if current_hp < max_hp:
            $ current_hp = min(max_hp, current_hp + 20)
            jump start
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start
        "Exit":
            return
