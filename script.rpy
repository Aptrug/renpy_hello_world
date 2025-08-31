# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

# I wonder, can the HP bar be made into a less boring shape (straight line) without adding too much complexity?

# ========================
# Game Variables
# ========================
default current_round = 59
default max_ap = 9
default available_ap = 3
default current_hp = 85
default max_hp = 100
default enemy_hp = 60
default enemy_max_hp = 80
default CIRCLE_RADIUS = 72
default ORB_RADIUS = 12

# NOTE: gui.notify_text_size is defined as 24 in gui.rpy

# ========================
# ATL Transforms
# ========================
transform glow:
    ease 1.5 alpha 0.6
    ease 1.5 alpha 1.0
    repeat

transform inactive:
    alpha 0.4

transform sun_aura:
    blur 2
    ease 4.0 alpha 0.05
    ease 4.0 alpha 0.15
    repeat

transform damage_flash:
    alpha 1.0
    linear 0.1 alpha 0.0
    linear 0.1 alpha 1.0
    linear 0.1 alpha 0.0
    linear 0.1 alpha 1.0

# ========================
# Python Helpers
# ========================
init python:
    import math

    # Cache orb positions and circles for lower CPU usage
    _orb_cache = {}
    _circle_cache = {}

    def get_orb_positions(num_orbs):
        if num_orbs not in _orb_cache:
            positions = []
            if num_orbs > 0:
                step = 6.283185307179586 / num_orbs  # 2*pi
                for i in range(num_orbs):
                    angle = step * i - 1.5707963267948966  # -pi/2
                    x = CIRCLE_RADIUS * (1 + math.cos(angle)) - ORB_RADIUS
                    y = CIRCLE_RADIUS * (1 + math.sin(angle)) - ORB_RADIUS
                    positions.append((int(x), int(y)))
            _orb_cache[num_orbs] = positions
        return _orb_cache[num_orbs]

    def get_circle(radius, color):
        key = (radius, color)
        if key not in _circle_cache:
            _circle_cache[key] = SimpleCircle(radius, color)
        return _circle_cache[key]

    # CRITICAL: SimpleCircle class is required for proper circular rendering
    # DO NOT REMOVE - Ren'Py's Solid creates squares, this creates actual circles
    class SimpleCircle(renpy.Displayable):
        def __init__(self, radius, color):
            super().__init__()
            self.radius = radius
            self.color = color
        def render(self, w, h, st, at):
            size = 2 * self.radius
            r = renpy.Render(size, size)
            c = r.canvas()
            c.circle(self.color, (self.radius, self.radius), self.radius)
            return r

    # Wave/Curved HP Bar
    class WaveBar(renpy.Displayable):
        def __init__(self, width, height, color, fill_percentage):
            super().__init__()
            self.width = width
            self.height = height
            self.color = color
            self.fill_percentage = fill_percentage

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Create wave points
            points = []
            wave_height = 3
            segments = 20

            for i in range(segments + 1):
                x = (i / float(segments)) * self.width
                # Create subtle wave effect
                wave_offset = wave_height * math.sin((i / float(segments)) * math.pi * 4)
                y_top = wave_offset + 2
                y_bottom = self.height - 2 - wave_offset

                if i == 0:
                    points.extend([x, y_top, x, y_bottom])
                elif i == segments:
                    points.extend([x, y_bottom, x, y_top])
                else:
                    points.extend([x, y_top])

            # Fill only up to the percentage
            fill_width = self.width * self.fill_percentage
            if fill_width > 0:
                fill_points = []
                for i in range(int(segments * self.fill_percentage) + 1):
                    x = (i / float(segments)) * self.width
                    if x > fill_width:
                        x = fill_width
                    wave_offset = wave_height * math.sin((i / float(segments)) * math.pi * 4)
                    y_top = wave_offset + 2
                    y_bottom = self.height - 2 - wave_offset

                    if i == 0:
                        fill_points.extend([x, y_top, x, y_bottom])
                    else:
                        fill_points.extend([x, y_top])

                # Close the shape
                fill_points.extend([fill_width, self.height - 2, 0, self.height - 2])

                if len(fill_points) >= 6:  # Need at least 3 points
                    c.polygon(self.color, fill_points)

            return r

    # Hexagonal HP Bar
    class HexBar(renpy.Displayable):
        def __init__(self, width, height, color, fill_percentage):
            super().__init__()
            self.width = width
            self.height = height
            self.color = color
            self.fill_percentage = fill_percentage

        def render(self, w, h, st, at):
            r = renpy.Render(self.width, self.height)
            c = r.canvas()

            # Hexagonal shape points
            hex_indent = self.height // 2
            points = [
                hex_indent, 0,  # Top left
                self.width - hex_indent, 0,  # Top right
                self.width, self.height // 2,  # Right point
                self.width - hex_indent, self.height,  # Bottom right
                hex_indent, self.height,  # Bottom left
                0, self.height // 2  # Left point
            ]

            # Fill portion based on percentage
            if self.fill_percentage > 0:
                fill_width = self.width * self.fill_percentage

                # Create clipped hexagon for fill
                fill_points = []
                for i in range(0, len(points), 2):
                    x, y = points[i], points[i + 1]
                    if x <= fill_width:
                        fill_points.extend([x, y])
                    elif len(fill_points) > 0:
                        # Add intersection point and stop
                        if y == self.height // 2:  # Right point
                            fill_points.extend([fill_width, y])
                        else:
                            fill_points.extend([fill_width, y])
                        break

                # Close the polygon properly
                if len(fill_points) >= 6:
                    # Add bottom edge if needed
                    if fill_width < self.width - hex_indent:
                        fill_points.extend([fill_width, self.height, hex_indent, self.height])
                    c.polygon(self.color, fill_points)

            return r

# ========================
# HP Bar Styles (Choose One!)
# ========================

# ORIGINAL HP Bar
screen hp_bar_section(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        fixed:
            xsize width + 4
            ysize 16

            # Frame and background
            add "#333333" xsize width + 4 ysize 16
            add "#000000" xsize width ysize 12 xpos 2 ypos 2

            # Animated HP bar
            bar:
                value AnimatedValue(hp_value, max_hp_value, 0.8)
                range max_hp_value
                xsize width
                ysize 12
                xpos 2
                ypos 2
                left_bar color
                right_bar "#000000"

            # Highlight
            add "#ffffff" xsize width ysize 1 xpos 2 ypos 2 alpha 0.3

        text "[hp_value]%" size gui.notify_text_size color "#ffffff"

# ROUNDED HP Bar
screen hp_bar_rounded(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        fixed:
            xsize width + 4
            ysize 20  # Slightly taller for rounded effect

            # Rounded background
            add "#333333" xsize width + 4 ysize 20
            add "#000000" xsize width ysize 16 xpos 2 ypos 2

            # Main HP bar
            bar:
                value AnimatedValue(hp_value, max_hp_value, 0.8)
                range max_hp_value
                xsize width
                ysize 16
                xpos 2
                ypos 2
                left_bar color
                right_bar "#000000"

            # Rounded caps (circles at ends)
            if hp_value > 0:
                $ bar_fill_width = int((hp_value / float(max_hp_value)) * width)
                if bar_fill_width > 8:
                    add get_circle(8, color) xpos 2 ypos 2
                    if bar_fill_width < width - 8:
                        add get_circle(8, color) xpos 2 + bar_fill_width - 8 ypos 2
                    else:
                        add get_circle(8, color) xpos 2 + width - 8 ypos 2

            # Highlight
            add "#ffffff" xsize width ysize 1 xpos 2 ypos 2 alpha 0.3

        text "[hp_value]%" size gui.notify_text_size color "#ffffff"

# SEGMENTED HP Bar
screen hp_bar_segmented(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        fixed:
            xsize width + 4
            ysize 16

            # Background
            add "#333333" xsize width + 4 ysize 16
            add "#000000" xsize width ysize 12 xpos 2 ypos 2

            # Segmented bars
            $ segment_count = 10
            $ segment_width = (width - (segment_count - 1) * 2) // segment_count
            $ filled_segments = int((hp_value / float(max_hp_value)) * segment_count)
            $ partial_fill = ((hp_value / float(max_hp_value)) * segment_count) - filled_segments

            for i in range(segment_count):
                $ segment_x = 2 + i * (segment_width + 2)
                if i < filled_segments:
                    $ segment_color = color
                elif i == filled_segments and partial_fill > 0:
                    $ segment_color = color
                    add segment_color:
                        xsize int(segment_width * partial_fill)
                        ysize 12
                        xpos segment_x
                        ypos 2
                    $ segment_color = "#333333"
                    add segment_color:
                        xsize segment_width - int(segment_width * partial_fill)
                        ysize 12
                        xpos segment_x + int(segment_width * partial_fill)
                        ypos 2
                else:
                    $ segment_color = "#333333"
                    add segment_color:
                        xsize segment_width
                        ysize 12
                        xpos segment_x
                        ypos 2

            # Highlight
            add "#ffffff" xsize width ysize 1 xpos 2 ypos 2 alpha 0.3

        text "[hp_value]%" size gui.notify_text_size color "#ffffff"

# WAVE HP Bar
screen hp_bar_wave(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        fixed:
            xsize width + 4
            ysize 16

            # Frame
            add "#333333" xsize width + 4 ysize 16
            add "#000000" xsize width ysize 12 xpos 2 ypos 2

            # Wave bar
            add WaveBar(width, 12, color, hp_value / float(max_hp_value)) xpos 2 ypos 2

            # Highlight
            add "#ffffff" xsize width ysize 1 xpos 2 ypos 2 alpha 0.3

        text "[hp_value]%" size gui.notify_text_size color "#ffffff"

# HEXAGONAL HP Bar
screen hp_bar_hex(label, hp_value, max_hp_value, color, width):
    vbox:
        spacing 5
        text label size gui.notify_text_size color "#ffffff"

        fixed:
            xsize width + 4
            ysize 20  # Taller for hex shape

            # Frame
            add "#333333" xsize width + 4 ysize 20

            # Hex bar
            add HexBar(width, 16, color, hp_value / float(max_hp_value)) xpos 2 ypos 2

        text "[hp_value]%" size gui.notify_text_size color "#ffffff"

# ========================
# Main UI Screen
# ========================
screen round_ui():
    # Cache bar width calculation
    $ bar_width = (config.screen_width - 340) // 2
    $ circle_diameter = CIRCLE_RADIUS * 2

    add "#808080"

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar - UNCOMMENT THE ONE YOU WANT!
        # use hp_bar_section("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)  # Original
        # use hp_bar_rounded("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)  # Rounded
        use hp_bar_segmented("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)  # Segmented
        # use hp_bar_wave("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)  # Wave
        # use hp_bar_hex("Enemy", enemy_hp, enemy_max_hp, "#c41e3a", bar_width)  # Hexagonal

        # Round circle
        fixed:
            xsize circle_diameter
            ysize circle_diameter

            # Subtle golden aura (stays within orb boundary)
            add get_circle(CIRCLE_RADIUS + 4, "#ffd700") align (0.5, 0.5) at sun_aura

            # Cached background circle
            add get_circle(CIRCLE_RADIUS, "#505050") align (0.5, 0.5)

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 20 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 60 color "#FFFFFF" xalign 0.5

            # Cached AP Orbs
            for i, (x, y) in enumerate(get_orb_positions(max_ap)):
                add get_circle(ORB_RADIUS, "#ffd700" if i < available_ap else "#666666"):
                    xpos x
                    ypos y
                    at (glow if i < available_ap else inactive)

        # Hero HP bar - UNCOMMENT THE ONE YOU WANT!
        use hp_bar_section("Hero", current_hp, max_hp, "#4169e1", bar_width)  # Original
        # use hp_bar_rounded("Hero", current_hp, max_hp, "#4169e1", bar_width)  # Rounded
        # use hp_bar_segmented("Hero", current_hp, max_hp, "#4169e1", bar_width)  # Segmented
        # use hp_bar_wave("Hero", current_hp, max_hp, "#4169e1", bar_width)  # Wave
        # use hp_bar_hex("Hero", current_hp, max_hp, "#4169e1", bar_width)  # Hexagonal

# ========================
# Demo Label
# ========================
label start:
    show screen round_ui
    "Round [current_round], AP [available_ap]/[max_ap], Hero HP [current_hp]/[max_hp], Enemy HP [enemy_hp]/[enemy_max_hp]"
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
        "Damage Enemy" if enemy_hp > 0:
            $ enemy_hp = max(0, enemy_hp - 20)
            jump start
        "Enemy Heals" if enemy_hp < enemy_max_hp:
            $ enemy_hp = min(enemy_max_hp, enemy_hp + 15)
            jump start
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start
        "Exit":
            return
