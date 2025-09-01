# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

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

# ========================
# Python Helpers
# ========================
init python:
    import math

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
    _hp_color_cache = {}

    def get_hp_color(current, maximum, is_enemy=False):
        """Calculate HP bar color based on current/max ratio - cached for efficiency"""
        # Create cache key from the parameters that affect color
        cache_key = (current, maximum, is_enemy)

        if cache_key not in _hp_color_cache:
            ratio = current / maximum if maximum > 0 else 0.0

            if is_enemy:
                # Enemy HP: Use pre-computed constants
                r = int(ENEMY_COLOR_BASE[0] + ENEMY_COLOR_RANGE[0] * ratio)
                g = int(ENEMY_COLOR_BASE[1] + ENEMY_COLOR_RANGE[1] * ratio)
                b = int(ENEMY_COLOR_BASE[2] + ENEMY_COLOR_RANGE[2] * ratio)
            else:
                # Hero HP: Use pre-computed constants
                r = int(HERO_COLOR_BASE[0] + HERO_COLOR_RANGE[0] * ratio)
                g = int(HERO_COLOR_BASE[1] + HERO_COLOR_RANGE[1] * ratio)
                b = int(HERO_COLOR_BASE[2] + HERO_COLOR_RANGE[2] * ratio)

            _hp_color_cache[cache_key] = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return _hp_color_cache[cache_key]

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

# ========================
# Main UI Screen
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

            # Subtle golden aura (stays within orb boundary)
            add get_circle(CIRCLE_RADIUS + 4, "#ffd700") xalign 0.5 yalign 0.5 at sun_aura

            # Cached background circle
            add get_circle(CIRCLE_RADIUS, "#505050") xalign 0.5 yalign 0.5

            # Round text
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 20 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 60 color "#FFFFFF" xalign 0.5

            # Optimized AP Orbs - cache positions and minimize function calls
            for i, (x, y) in enumerate(orb_positions):
                $ is_active = i < available_ap
                add get_circle(ORB_RADIUS, "#ffd700" if is_active else "#666666"):
                    xpos x
                    ypos y
                    at (glow if is_active else inactive)

        # Hero HP bar with cached color
        use hp_bar_section("Hero", current_hp, max_hp, hero_color, bar_width)

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

# I want you to integrate the code below in the code above
# The battle UI will be like
# Big centered boss image
# 2 HP bars & Circle
# Hero party


# Preload all images
image boss = "images/combat_system/boss.webp"
image kenshin = "images/combat_system/kenshin.webp"
image magic = "images/combat_system/magic.webp"
image rance = "images/combat_system/rance.webp"
image reset = "images/combat_system/reset.webp"
image suzume = "images/combat_system/suzume.webp"

# 0 all good
# 1 still all good
# 2 must re-enable quickmenu later
default persistent.qmenu_bak = 0

init python:
    # If quit the game mid battle
    if persistent.qmenu_bak == 2:
        persistent.quickmenu = True
        persistent.qmenu_bak = 0

screen battle_ui():
    # Feldgrau background
    add Solid("#4D5D53")

    # Boss image, centered top, 70% height, top margin 30px
    add "boss" at idle_float:
        xalign 0.5
        yalign 0.1
        zoom 0.65

    # Allies row, bottom center
    hbox:
        xalign 0.5
        yalign 0.95
        spacing 20

        add "kenshin" at ally_hover
        add "magic" at gentle_float
        add "rance" at ally_selected_effect
        add "reset" at ally_idle
        add "suzume" at ally_selected_effect

# Bunch of effects, some used, some not
transform idle_float:
    yoffset 0
    linear 2.0 yoffset -5
    linear 2.0 yoffset 0
    repeat

transform pulse_glow:
    alpha 0.5
    linear 1.0 alpha 0.8
    linear 1.0 alpha 0.5
    repeat

transform slow_pulse:
    alpha 0.9
    linear 1.5 alpha 1.0
    linear 1.5 alpha 0.9
    repeat

transform hit_shake:
    linear 0.1 xoffset 10
    linear 0.1 xoffset -10
    linear 0.1 xoffset 0

transform ally_selected_effect:
    matrixcolor BrightnessMatrix(0.3)
    linear 0.8 matrixcolor BrightnessMatrix(0.1)
    linear 0.8 matrixcolor BrightnessMatrix(0.3)
    repeat

transform boss_breathe:
    yoffset 30 zoom 0.7
    linear 3.0 yoffset 25 zoom 0.72
    linear 3.0 yoffset 30 zoom 0.7
    repeat

transform ally_hover_effect:
    zoom 1.08
    matrixcolor BrightnessMatrix(0.2)

transform ally_hover:
    zoom 1.0
    linear 0.25 zoom 1.08

transform gentle_float:
    yoffset 0
    linear 4.0 yoffset -8
    linear 4.0 yoffset 0
    repeat

transform ally_idle:
    linear 0.25 zoom 1.0

# === Extra Effects (High Impact, Low Cost) ===

# Quick "anticipation" zoom before attacks, then reset
transform attack_zoom:
    zoom 1.0
    linear 0.15 zoom 1.1
    linear 0.15 zoom 1.0

# Simple white flash overlay for hits
transform hit_flash:
    alpha 0.0
    linear 0.05 alpha 0.6
    linear 0.2 alpha 0.0

# Smooth health bar changes (use on bar images)
transform smooth_hp:
    linear 0.5 xzoom 1.0  # You'd adjust size dynamically, this smooths it visually

# Floating damage numbers or text (up and fade out)
transform damage_float:
    yoffset 0 alpha 1.0
    linear 0.8 yoffset -40 alpha 0.0

# Attack "impact shake" (slightly bigger than hit_shake)
transform impact_shake:
    linear 0.05 xoffset 15
    linear 0.05 xoffset -15
    linear 0.05 xoffset 10
    linear 0.05 xoffset -10
    linear 0.05 xoffset 0

# Parallax-like background drift
transform bg_drift:
    xpos 0.0
    linear 20.0 xpos -50.0
    linear 20.0 xpos 0.0
    repeat

label start_battle:
    if persistent.quickmenu:
        $persistent.qmenu_bak = 2
    else:
        $persistent.qmenu_bak = 1
    $persistent.quickmenu = False

    $config.rollback_enabled = False

    show screen battle_ui

    "A wild boss appears!"
    "Kenshin attacks!"
    "Boss retaliates!"

    if persistent.qmenu_bak == 2:
        $persistent.quickmenu = True
    $persistent.qmenu_bak = 0

    hide screen battle_ui

    $renpy.block_rollback()
    $config.rollback_enabled = True

    scene forest with fade

    # Jump back to main story/dialogue
    jump after_battle

label after_battle:
    "The battle is over, and the heroes catch their breath."
    "Kenshin: That was intense!"
    "Rance: Let's keep moving."

    # Continue with normal story
    return
