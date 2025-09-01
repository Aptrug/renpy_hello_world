# Can you a frame around the HP bar or something, because when it's full, it just looks like a long blue line instead of an HP bar. Look how other famous games do it. Don't add too much complexity though, less is more as they say.

# Anything I can add to make the combat experience feel more engaging & immersive but is also simple to implement?

# Enhanced Combat Experience - Simple but Immersive Additions

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

# NEW: Combat State Variables
default last_damage_taken = 0
default last_damage_dealt = 0
default combat_momentum = 0  # -3 to +3, affects visuals
default low_hp_warning = False
default critical_hp_warning = False

# NOTE: gui.notify_text_size is defined as 24 in gui.rpy

# ========================
# Enhanced ATL Transforms
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

# NEW: Combat feedback transforms
transform damage_shake:
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 xoffset 3
    linear 0.05 xoffset -3
    linear 0.05 xoffset 0

transform critical_pulse:
    ease 0.3 alpha 1.0
    ease 0.3 alpha 0.3
    repeat

transform momentum_glow:
    ease 1.0 alpha 0.8
    ease 1.0 alpha 1.0
    repeat

transform floating_damage:
    alpha 1.0
    yoffset 0
    ease 2.0 yoffset -50 alpha 0.0

# ========================
# Enhanced Python Helpers
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

    # NEW: Combat state functions
    def update_combat_state():
        """Update combat warnings and momentum"""
        global low_hp_warning, critical_hp_warning, combat_momentum

        hp_ratio = current_hp / max_hp
        low_hp_warning = hp_ratio <= 0.3
        critical_hp_warning = hp_ratio <= 0.15

        # Simple momentum system based on recent actions
        if last_damage_dealt > last_damage_taken:
            combat_momentum = min(3, combat_momentum + 1)
        elif last_damage_taken > last_damage_dealt:
            combat_momentum = max(-3, combat_momentum - 1)
        else:
            combat_momentum = max(-3, min(3, combat_momentum * 0.8))

    def get_momentum_color():
        """Get color based on combat momentum"""
        if combat_momentum > 1:
            return "#00ff00"  # Green for advantage
        elif combat_momentum < -1:
            return "#ff0000"  # Red for disadvantage
        else:
            return "#ffd700"  # Gold for neutral

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
# Enhanced Main UI Screen
# ========================
screen round_ui():
    # Update combat state
    $ update_combat_state()

    # Cache all calculations at screen level
    $ bar_width = (config.screen_width - 340) // 2
    $ circle_diameter = CIRCLE_RADIUS * 2
    $ enemy_color = get_hp_color(enemy_hp, enemy_max_hp, True)
    $ hero_color = get_hp_color(current_hp, max_hp, False)
    $ orb_positions = get_orb_positions(max_ap)
    $ momentum_color = get_momentum_color()

    add "#808080"

    # NEW: Screen flash for critical HP
    if critical_hp_warning:
        add "#ff0000" alpha 0.1 at critical_pulse

    # ORIGINAL LAYOUT: Centered horizontal layout
    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        # Enemy HP bar (LEFT) with shake on damage
        fixed:
            if last_damage_dealt > 0:
                at damage_shake
            use hp_bar_section("Enemy", enemy_hp, enemy_max_hp, enemy_color, bar_width, True)

        # Round circle (CENTER) with enhancements
        fixed:
            xsize circle_diameter
            ysize circle_diameter

            # Dynamic aura based on momentum
            if abs(combat_momentum) > 1:
                add get_circle(CIRCLE_RADIUS + 8, momentum_color) xalign 0.5 yalign 0.5 alpha 0.3 at momentum_glow

            # Subtle golden aura (baseline)
            add get_circle(CIRCLE_RADIUS + 4, "#ffd700") xalign 0.5 yalign 0.5 at sun_aura

            # Background circle - keep original color scheme
            add get_circle(CIRCLE_RADIUS, "#505050") xalign 0.5 yalign 0.5

            # Round text (same as original)
            vbox:
                xalign 0.5
                yalign 0.5
                yoffset 10
                spacing -5
                text "Round" size 20 color "#FFFFFF" xalign 0.5
                text "[current_round]" size 60 color "#FFFFFF" xalign 0.5

            # Enhanced AP Orbs with low-AP warning (same positions as original)
            for i, (x, y) in enumerate(orb_positions):
                $ is_active = i < available_ap
                $ orb_color = "#ffd700" if is_active else "#666666"
                # Pulse remaining orbs when AP is low
                $ use_warning = available_ap <= 2 and is_active
                add get_circle(ORB_RADIUS, orb_color):
                    xpos x
                    ypos y
                    at (critical_pulse if use_warning else (glow if is_active else inactive))

        # Hero HP bar (RIGHT) with shake on damage
        fixed:
            if last_damage_taken > 0:
                at damage_shake
            use hp_bar_section("Hero", current_hp, max_hp, hero_color, bar_width, False)

    # NEW: Floating damage numbers (positioned over the bars)
    if last_damage_dealt > 0:
        text "-[last_damage_dealt]" size 36 color "#ff4444" xalign 0.25 yalign 0.4 at floating_damage
    if last_damage_taken > 0:
        text "-[last_damage_taken]" size 36 color "#ff0000" xalign 0.75 yalign 0.4 at floating_damage

    # NEW: Combat status indicators (corner overlay, doesn't break layout)
    vbox:
        xalign 0.02
        yalign 0.02
        spacing 5

        if low_hp_warning and not critical_hp_warning:
            text "LOW HP" size 20 color "#ffaa00" at critical_pulse
        elif critical_hp_warning:
            text "CRITICAL!" size 24 color "#ff0000" at critical_pulse

        if available_ap <= 1:
            text "LOW AP" size 18 color "#ffaa00" at glow

# ========================
# Enhanced HP Bar Component
# ========================
screen hp_bar_section(label, hp_value, max_hp_value, color, width, is_enemy=False):
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

            # Enhanced highlight with warning flash
            $ highlight_alpha = 0.5 if (not is_enemy and critical_hp_warning) else 0.3
            add "#ffffff" xsize width ysize 1 xpos 2 ypos 2 alpha highlight_alpha

        # Enhanced HP text with percentage and warnings
        hbox:
            spacing 10
            text "[hp_value]%" size gui.notify_text_size color "#ffffff"

            # NEW: Status indicators for low HP
            if not is_enemy and hp_value <= 30:
                if hp_value <= 15:
                    text "⚠" size gui.notify_text_size color "#ff0000" at critical_pulse
                else:
                    text "⚠" size gui.notify_text_size color "#ffaa00"

# ========================
# Enhanced Demo with Combat Feedback
# ========================
label start:
    show screen round_ui
    "Round [current_round], AP [available_ap]/[max_ap], Hero HP [current_hp]/[max_hp], Enemy HP [enemy_hp]/[enemy_max_hp]"

    # Reset damage indicators at start of each turn
    $ last_damage_taken = 0
    $ last_damage_dealt = 0

    menu:
        "Spend AP" if available_ap > 0:
            $ available_ap -= 1
            jump start
        "Gain AP" if available_ap < max_ap:
            $ available_ap += 1
            jump start
        "Take Damage" if current_hp > 0:
            $ damage = 15
            $ current_hp = max(0, current_hp - damage)
            $ last_damage_taken = damage
            "You take [damage] damage!"
            jump start
        "Heal" if current_hp < max_hp:
            $ heal = 20
            $ current_hp = min(max_hp, current_hp + heal)
            "You heal [heal] HP!"
            jump start
        "Damage Enemy" if enemy_hp > 0:
            $ damage = 20
            $ enemy_hp = max(0, enemy_hp - damage)
            $ last_damage_dealt = damage
            "You deal [damage] damage!"
            jump start
        "Enemy Heals" if enemy_hp < enemy_max_hp:
            $ enemy_hp = min(enemy_max_hp, enemy_hp + 15)
            jump start
        "Next Round":
            $ current_round += 1
            $ available_ap = max_ap
            $ last_damage_taken = 0
            $ last_damage_dealt = 0
            jump start
        "Exit":
            return
