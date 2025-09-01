# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

# Enhanced combat experience with floating damage numbers that rise and fade
# Now includes immersive damage feedback with color-coded numbers

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

# Floating damage system variables
default damage_numbers = []  # List of active damage number objects
default damage_id_counter = 0  # Unique ID for each damage number

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

# Floating damage number animations
transform float_damage(start_x, start_y):
    xpos start_x
    ypos start_y
    alpha 1.0
    # Rise up and fade out
    parallel:
        ease 2.0 ypos start_y - 100
    parallel:
        ease 0.2 alpha 1.0
        ease 1.8 alpha 0.0
    # Auto-remove after animation
    function lambda **kwargs: damage_numbers.remove(next(d for d in damage_numbers if d["id"] == kwargs["id"])) if any(d["id"] == kwargs["id"] for d in damage_numbers) else None

transform float_damage_crit(start_x, start_y):
    xpos start_x
    ypos start_y
    alpha 1.0
    # Critical hits have more dramatic movement
    parallel:
        ease 0.1 ypos start_y - 20
        ease 1.9 ypos start_y - 120
    parallel:
        ease 0.1 zoom 1.2
        ease 0.4 zoom 1.0
    parallel:
        ease 0.2 alpha 1.0
        ease 1.8 alpha 0.0

transform float_heal(start_x, start_y):
    xpos start_x
    ypos start_y
    alpha 1.0
    # Healing floats up gently
    parallel:
        ease 2.5 ypos start_y - 80
    parallel:
        ease 0.3 alpha 1.0
        ease 2.2 alpha 0.0

# ========================
# Python Helpers
# ========================
init python:
    import math
    import random

    # Cache orb positions, circles, and colors for lower CPU usage
    _orb_cache = {}
    _circle_cache = {}
    _hp_color_cache = {}

    # Pre-computed constants for faster color calculations
    ENEMY_COLOR_BASE = (0x66, 0x00, 0x00)  # Dark clotted red base
    ENEMY_COLOR_RANGE = (0x99, 0x33, 0x33)  # Range to bright red
    HERO_COLOR_BASE = (0x1a, 0x23, 0x7e)   # Dark blue base
    HERO_COLOR_RANGE = (0x27, 0x46, 0x63)  # Range to bright blue

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

    # HP Color cache to avoid recalculating identical values
    def get_hp_color(current, maximum, is_enemy=False):
        """Calculate HP bar color based on current/max ratio - cached for efficiency"""
        cache_key = (current, maximum, is_enemy)

        if cache_key not in _hp_color_cache:
            ratio = current / maximum if maximum > 0 else 0.0

            if is_enemy:
                r = int(ENEMY_COLOR_BASE[0] + ENEMY_COLOR_RANGE[0] * ratio)
                g = int(ENEMY_COLOR_BASE[1] + ENEMY_COLOR_RANGE[1] * ratio)
                b = int(ENEMY_COLOR_BASE[2] + ENEMY_COLOR_RANGE[2] * ratio)
            else:
                r = int(HERO_COLOR_BASE[0] + HERO_COLOR_RANGE[0] * ratio)
                g = int(HERO_COLOR_BASE[1] + HERO_COLOR_RANGE[1] * ratio)
                b = int(HERO_COLOR_BASE[2] + HERO_COLOR_RANGE[2] * ratio)

            _hp_color_cache[cache_key] = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return _hp_color_cache[cache_key]

    # Floating damage number system
    def add_damage_number(amount, x, y, damage_type="damage"):
        """Add a floating damage number at the specified position"""
        global damage_id_counter
        damage_id_counter += 1

        # Add some random offset to prevent overlapping
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-10, 10)

        # Determine color and prefix based on damage type
        if damage_type == "heal":
            color = "#00ff66"  # Bright green
            prefix = "+"
            text_size = 32
        elif damage_type == "critical":
            color = "#ff3366"  # Bright red
            prefix = "-"
            text_size = 40
        else:  # regular damage
            color = "#ffaa33"  # Orange
            prefix = "-"
            text_size = 36

        damage_obj = {
            "id": damage_id_counter,
            "amount": amount,
            "x": x + offset_x,
            "y": y + offset_y,
            "color": color,
            "prefix": prefix,
            "size": text_size,
            "type": damage_type
        }

        damage_numbers.append(damage_obj)

        # Clean up old damage numbers (keep list from growing infinitely)
        if len(damage_numbers) > 10:
            damage_numbers.pop(0)

    def get_enemy_damage_position():
        """Get position near enemy HP bar for damage numbers"""
        bar_width = (config.screen_width - 340) // 2
        return (bar_width // 2, config.screen_height // 2 - 100)

    def get_hero_damage_position():
        """Get position near hero HP bar for damage numbers"""
        bar_width = (config.screen_width - 340) // 2
        return (config.screen_width - bar_width // 2, config.screen_height // 2 - 100)

    # CRITICAL: SimpleCircle class is required for proper circular rendering
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

# ========================
# Enhanced Action Functions
# ========================
init python:
    def deal_damage_to_enemy(amount, is_critical=False):
        """Deal damage to enemy and show floating number"""
        global enemy_hp
        old_hp = enemy_hp
        enemy_hp = max(0, enemy_hp - amount)
        actual_damage = old_hp - enemy_hp

        if actual_damage > 0:
            x, y = get_enemy_damage_position()
            damage_type = "critical" if is_critical else "damage"
            add_damage_number(actual_damage, x, y, damage_type)

    def deal_damage_to_hero(amount):
        """Deal damage to hero and show floating number"""
        global current_hp
        old_hp = current_hp
        current_hp = max(0, current_hp - amount)
        actual_damage = old_hp - current_hp

        if actual_damage > 0:
            x, y = get_hero_damage_position()
            add_damage_number(actual_damage, x, y, "damage")

    def heal_hero(amount):
        """Heal hero and show floating number"""
        global current_hp
        old_hp = current_hp
        current_hp = min(max_hp, current_hp + amount)
        actual_heal = current_hp - old_hp

        if actual_heal > 0:
            x, y = get_hero_damage_position()
            add_damage_number(actual_heal, x, y, "heal")

    def heal_enemy(amount):
        """Heal enemy and show floating number"""
        global enemy_hp
        old_hp = enemy_hp
        enemy_hp = min(enemy_max_hp, enemy_hp + amount)
        actual_heal = enemy_hp - old_hp

        if actual_heal > 0:
            x, y = get_enemy_damage_position()
            add_damage_number(actual_heal, x, y, "heal")

# ========================
# Main UI Screen with Floating Damage
# ========================
screen round_ui():
    # Cache all calculations at screen level
    $ bar_width = (config.screen_width - 340) // 2
    $ circle_diameter = CIRCLE_RADIUS * 2
    $ enemy_color = get_hp_color(enemy_hp, enemy_max_hp, True)
    $ hero_color = get_hp_color(current_hp, max_hp, False)
    $ orb_positions = get_orb_positions(max_ap)

    add "#808080"

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar with cached color
        use hp_bar_section("Enemy", enemy_hp, enemy_max_hp, enemy_color, bar_width)

        # Round circle
        fixed:
            xsize circle_diameter
            ysize circle_diameter

            # Subtle golden aura
            add get_circle(CIRCLE_RADIUS + 4, "#ffd700") xalign 0.5 yalign 0.5 at sun_aura

            # Background circle
            add get_circle(CIRCLE_RADIUS, "#505050") xalign 0.5 yalign 0.5

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 20 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 60 color "#FFFFFF" xalign 0.5

            # AP Orbs
            for i, (x, y) in enumerate(orb_positions):
                $ is_active = i < available_ap
                add get_circle(ORB_RADIUS, "#ffd700" if is_active else "#666666"):
                    xpos x
                    ypos y
                    at (glow if is_active else inactive)

        # Hero HP bar with cached color
        use hp_bar_section("Hero", current_hp, max_hp, hero_color, bar_width)

    # Floating damage numbers layer
    for damage in damage_numbers:
        $ transform_func = float_heal if damage["type"] == "heal" else (float_damage_crit if damage["type"] == "critical" else float_damage)
        text "[damage[prefix]][damage[amount]]":
            size damage["size"]
            color damage["color"]
            outlines [(2, "#000000", 0, 0)]
            at transform_func(damage["x"], damage["y"])
            id damage["id"]

# ========================
# Reusable HP Bar Component
# ========================
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

            # Animated HP bar with dynamic color
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

# ========================
# Enhanced Demo Label
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
        "Take Damage":
            $ deal_damage_to_hero(15)
            jump start
        "Heal":
            $ heal_hero(20)
            jump start
        "Attack Enemy":
            $ deal_damage_to_enemy(20)
            jump start
        "Critical Hit Enemy!":
            $ deal_damage_to_enemy(35, True)
            jump start
        "Enemy Heals":
            $ heal_enemy(15)
            jump start
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            jump start
        "Clear Damage Numbers":
            $ damage_numbers = []
            jump start
        "Exit":
            return
