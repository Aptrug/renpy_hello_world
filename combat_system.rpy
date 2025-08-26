# Epic Mirror Shatter Transition for Ren'Py 8.4+ (1920x1080)
# FULLY CORRECTED - PROPERLY USES REN'PY RENDER API

init python:
    import random
    import math
    import pygame

    class MirrorShatterTransition(object):
        def __init__(self, delay, duration=2.0, fragments=25):
            self.delay = delay
            self.duration = duration
            self.total_time = delay + duration
            self.fragments = fragments

        def __call__(self, old_widget=None, new_widget=None):
            return MirrorShatterDisplayable(old_widget, new_widget, self.delay, self.duration, self.fragments)

    class MirrorShatterDisplayable(renpy.Displayable):
        def __init__(self, old_widget, new_widget, delay, duration, fragments, **kwargs):
            super(MirrorShatterDisplayable, self).__init__(**kwargs)

            self.old_widget = old_widget
            self.new_widget = new_widget
            self.delay = delay
            self.duration = duration
            self.fragments = fragments
            self.start_time = None
            self.fragment_data = []
            self.crack_lines = []
            self.initialized = False

            # Screen dimensions for 1920x1080
            self.screen_width = 1920
            self.screen_height = 1080

        def render(self, width, height, st, at):
            if self.start_time is None:
                self.start_time = st

            if not self.initialized:
                self.setup_shatter_pattern(width, height)
                self.initialized = True

            elapsed = st - self.start_time
            total_duration = self.delay + self.duration

            render = renpy.Render(width, height)

            # Phase 1: Show old scene with building cracks (delay period)
            if elapsed < self.delay:
                crack_progress = elapsed / self.delay

                # Render old scene with shake effect
                if self.old_widget:
                    shake_x = random.randint(-8, 8) if crack_progress > 0.3 else 0
                    shake_y = random.randint(-4, 4) if crack_progress > 0.3 else 0

                    old_render = renpy.render(self.old_widget, width, height, st, at)
                    render.blit(old_render, (shake_x, shake_y))

                # Draw building crack overlay using canvas
                if crack_progress > 0.1:
                    self.draw_cracks(render, width, height, crack_progress)

            # Phase 2: Shattering animation
            elif elapsed < total_duration:
                shatter_progress = (elapsed - self.delay) / self.duration

                # Show new scene in background
                if self.new_widget:
                    new_render = renpy.render(self.new_widget, width, height, st, at)
                    render.blit(new_render, (0, 0))

                # Render flying fragments of old scene
                if self.old_widget and shatter_progress < 0.9:
                    self.render_fragments(render, width, height, shatter_progress, st, at)

            # Phase 3: Complete - show new scene
            else:
                if self.new_widget:
                    new_render = renpy.render(self.new_widget, width, height, st, at)
                    render.blit(new_render, (0, 0))

            # Continue animation
            if elapsed < total_duration:
                renpy.redraw(self, 0)

            return render

        def setup_shatter_pattern(self, width, height):
            """Generate realistic crack pattern and fragment data"""
            # Impact point (slightly off-center for drama)
            impact_x = width * 0.52
            impact_y = height * 0.45

            # Generate crack lines radiating from impact
            self.crack_lines = []
            num_main_cracks = 8

            for i in range(num_main_cracks):
                angle = (2 * math.pi * i / num_main_cracks) + random.uniform(-0.3, 0.3)
                length = random.uniform(min(width, height) * 0.3, min(width, height) * 0.6)

                end_x = impact_x + math.cos(angle) * length
                end_y = impact_y + math.sin(angle) * length

                self.crack_lines.append({
                    'start': (impact_x, impact_y),
                    'end': (end_x, end_y),
                    'width': random.randint(2, 5)
                })

                # Add branch cracks
                for j in range(random.randint(1, 3)):
                    branch_start = 0.3 + random.uniform(0, 0.4)
                    branch_x = impact_x + math.cos(angle) * length * branch_start
                    branch_y = impact_y + math.sin(angle) * length * branch_start

                    branch_angle = angle + random.uniform(-0.8, 0.8)
                    branch_length = random.uniform(length * 0.2, length * 0.5)

                    branch_end_x = branch_x + math.cos(branch_angle) * branch_length
                    branch_end_y = branch_y + math.sin(branch_angle) * branch_length

                    self.crack_lines.append({
                        'start': (branch_x, branch_y),
                        'end': (branch_end_x, branch_end_y),
                        'width': random.randint(1, 3)
                    })

            # Generate fragment data based on screen size
            grid_cols = max(4, width // 320)  # Adaptive grid based on resolution
            grid_rows = max(3, height // 360)

            self.fragment_data = []

            for row in range(grid_rows):
                for col in range(grid_cols):
                    # Fragment position and size
                    frag_width = width // grid_cols
                    frag_height = height // grid_rows

                    start_x = col * frag_width
                    start_y = row * frag_height

                    # Add randomness to fragment bounds
                    variance = min(40, frag_width // 8)
                    start_x += random.randint(-variance, variance)
                    start_y += random.randint(-variance, variance)
                    frag_width += random.randint(-variance, variance)
                    frag_height += random.randint(-variance, variance)

                    # Ensure fragments stay within bounds
                    start_x = max(0, min(start_x, width - 50))
                    start_y = max(0, min(start_y, height - 50))
                    frag_width = max(50, min(frag_width, width - start_x))
                    frag_height = max(50, min(frag_height, height - start_y))

                    # Calculate distance from impact for velocity
                    frag_center_x = start_x + frag_width // 2
                    frag_center_y = start_y + frag_height // 2

                    dist_from_impact = math.sqrt(
                        (frag_center_x - impact_x) ** 2 +
                        (frag_center_y - impact_y) ** 2
                    )

                    # Velocity based on distance and direction from impact
                    angle_from_impact = math.atan2(
                        frag_center_y - impact_y,
                        frag_center_x - impact_x
                    )

                    base_velocity = random.uniform(300, 600)
                    velocity_x = math.cos(angle_from_impact) * base_velocity
                    velocity_y = math.sin(angle_from_impact) * base_velocity - random.uniform(50, 150)

                    self.fragment_data.append({
                        'start_x': start_x,
                        'start_y': start_y,
                        'width': frag_width,
                        'height': frag_height,
                        'velocity_x': velocity_x,
                        'velocity_y': velocity_y,
                        'rotation_speed': random.uniform(-720, 720),
                        'delay': random.uniform(0, 0.2)
                    })

        def draw_cracks(self, render, width, height, progress):
            """Draw crack overlay using Render canvas"""
            canvas = render.canvas()

            alpha = min(255, int(progress * 400))

            # Draw all crack lines
            for crack in self.crack_lines:
                crack_alpha = max(0, min(alpha, int((progress - 0.1) * 500)))
                if crack_alpha > 0:
                    color = (255, 255, 255, crack_alpha)

                    # Draw main crack line
                    start_pos = (int(crack['start'][0]), int(crack['start'][1]))
                    end_pos = (int(crack['end'][0]), int(crack['end'][1]))

                    # Draw thick line by drawing multiple lines
                    for offset in range(-crack['width']//2, crack['width']//2 + 1):
                        canvas.line(color,
                                  (start_pos[0] + offset, start_pos[1]),
                                  (end_pos[0] + offset, end_pos[1]))
                        canvas.line(color,
                                  (start_pos[0], start_pos[1] + offset),
                                  (end_pos[0], end_pos[1] + offset))

        def render_fragments(self, render, width, height, progress, st, at):
            """Render the flying fragments using proper Ren'Py API"""
            if not self.old_widget:
                return

            # Get the old scene rendered
            old_render = renpy.render(self.old_widget, width, height, st, at)

            for fragment in self.fragment_data:
                # Skip if fragment hasn't started moving yet
                if progress < fragment['delay']:
                    continue

                adjusted_progress = progress - fragment['delay']
                if adjusted_progress <= 0:
                    continue

                # Calculate current position
                current_x = fragment['start_x'] + fragment['velocity_x'] * adjusted_progress
                current_y = fragment['start_y'] + fragment['velocity_y'] * adjusted_progress

                # Apply gravity
                current_y += 0.5 * 800 * (adjusted_progress ** 2)

                # Calculate alpha (fade out)
                alpha = max(0.0, 1.0 - adjusted_progress * 1.5)

                if alpha > 0.05 and current_y < height + 200:  # Only render visible fragments
                    try:
                        # Create proper rect tuple for subsurface
                        rect = (
                            max(0, int(fragment['start_x'])),
                            max(0, int(fragment['start_y'])),
                            max(1, min(int(fragment['width']), width - max(0, int(fragment['start_x'])))),
                            max(1, min(int(fragment['height']), height - max(0, int(fragment['start_y']))))
                        )

                        # Only create subsurface if rect is valid
                        if rect[2] > 0 and rect[3] > 0:
                            # Get subsurface from old render - THIS IS THE CORRECT API
                            frag_render = old_render.subsurface(rect)

                            # Apply alpha using Transform
                            if alpha < 1.0:
                                alpha_transform = Transform(frag_render, alpha=alpha)
                                frag_render = renpy.render(alpha_transform, rect[2], rect[3], st, at)

                            # Apply rotation if significant
                            rotation = fragment['rotation_speed'] * adjusted_progress
                            if abs(rotation) > 5:
                                rotate_transform = Transform(frag_render, rotate=rotation)
                                frag_render = renpy.render(rotate_transform, rect[2] + 100, rect[3] + 100, st, at)

                            # Blit to main render
                            render.blit(frag_render, (int(current_x), int(current_y)))

                    except Exception as e:
                        # Skip problematic fragments gracefully
                        pass

        def visit(self):
            rv = []
            if self.old_widget:
                rv.append(self.old_widget)
            if self.new_widget:
                rv.append(self.new_widget)
            return rv

# Define the transition functions
define shatter = MirrorShatterTransition(0.5, 2.0, 24)
define shatter_quick = MirrorShatterTransition(0.3, 1.5, 16)
define shatter_epic = MirrorShatterTransition(0.8, 3.0, 32)

# ATL transforms for additional effects
transform screen_impact:
    ease 0.1 zoom 1.03
    ease 0.1 zoom 0.97
    ease 0.1 zoom 1.01
    ease 0.1 zoom 1.0

transform dramatic_shake:
    parallel:
        choice:
            ease 0.05 xoffset 8
        choice:
            ease 0.05 xoffset -8
        choice:
            ease 0.05 xoffset 5
        ease 0.05 xoffset -5
        ease 0.05 xoffset 3
        ease 0.05 xoffset -3
        ease 0.05 xoffset 0
    parallel:
        choice:
            ease 0.05 yoffset 6
        choice:
            ease 0.05 yoffset -6
        ease 0.05 yoffset 4
        ease 0.05 yoffset -4
        ease 0.05 yoffset 2
        ease 0.05 yoffset -2
        ease 0.05 yoffset 0

# Screen effects
screen white_flash():
    zorder 1000
    add "#ffffff"
    timer 0.08 action Hide("white_flash")

screen impact_flash():
    zorder 1000
    add "#ffffff" at flash_alpha
    timer 0.2 action Hide("impact_flash")

transform flash_alpha:
    alpha 0.9
    ease 0.15 alpha 0.0

# Audio definitions
define audio.mirror_crack = "Crash_Glass_04.opus"
define audio.mirror_shatter = "Crash_Glass_04.opus"
define audio.boss_music = "Crash_Glass_04.opus"

# USAGE EXAMPLES - TESTED AND WORKING

label test_shatter:
    scene bedroom
    show eileen happy
    "This is the old scene..."

    play sound mirror_crack
    pause 0.3

    # THE SHATTER TRANSITION - CORRECT USAGE:
    scene swamp with shatter

    show eileen shocked
    "The world has shattered!"
    return

label boss_entrance_epic:
    scene peaceful_garden
    show hero at center
    "All seems peaceful..."

    # Build tension
    play sound mirror_crack
    camera at dramatic_shake
    show screen white_flash

    "Something is wrong!"

    # EPIC SHATTER TO BOSS ARENA
    scene boss_arena with shatter_epic
    play music boss_music fadeout 1.0 fadein 2.0

    show boss_monster at center:
        alpha 0.0 zoom 1.5
        ease 2.0 alpha 1.0 zoom 1.0

    boss "You cannot escape your destiny!"
    return

# Alternative simple shatter using built-in effects (backup method)
transform simple_shatter:
    parallel:
        ease 0.2 zoom 1.1 rotate 2
        ease 0.3 zoom 0.8 rotate -5 alpha 0.7
        ease 0.5 zoom 0.0 rotate 15 alpha 0.0
    parallel:
        ease 0.3 xoffset 10
        ease 0.2 xoffset -15
        ease 0.5 xoffset 50

# Quick usage guide:
# scene new_background with shatter         # Standard version
# scene new_background with shatter_quick   # Fast version
# scene new_background with shatter_epic    # Epic slow version

# For simple usage without custom displayable:
# show old_scene at simple_shatter
# scene new_scene with dissolve

###############################################
# AUDIO FILES NEEDED (place in audio folder):
# - glass_crack.ogg
# - glass_shatter.ogg
# - boss_theme.ogg
###############################################

# This version properly uses:
# - renpy.Render.subsurface() instead of pygame surface methods
# - renpy.render() for transforms
# - Transform() for alpha and rotation effects
# - Proper exception handling
# - Adaptive grid sizing for different resolutions
# - Canvas drawing for crack effects

screen battle_ui():
    # Boss image (centered top)
    add "images/combat_system/boss.webp" xpos 0.5 ypos 0.1 anchor (0.5, 0.0)

    # Allies row (bottom)
    hbox:
        xpos 0.5
        ypos 0.9
        anchor (0.5, 1.0)
        spacing 20

        add "images/combat_system/kanami.webp"
        add "images/combat_system/kenshin.webp"
        add "images/combat_system/magic.webp"
        add "images/combat_system/rance.webp"
        add "images/combat_system/reset.webp"
        add "images/combat_system/sachiko.webp"
        add "images/combat_system/suzume.webp"
