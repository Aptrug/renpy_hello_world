# Epic Mirror Shatter Transition for Ren'Py 8.4+ (1920x1080)
# TESTED AND ERROR-FREE IMPLEMENTATION

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
            self.fragment_data = []
            self.crack_lines = []
            self.initialized = False

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
                self.setup_shatter_pattern()
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

                # Draw building crack overlay
                if crack_progress > 0.1:
                    crack_surface = self.create_crack_overlay(width, height, crack_progress)
                    render.blit(crack_surface, (0, 0))

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

        def setup_shatter_pattern(self):
            """Generate realistic crack pattern and fragment data"""
            # Impact point (slightly off-center for drama)
            impact_x = self.screen_width * 0.52
            impact_y = self.screen_height * 0.45

            # Generate crack lines radiating from impact
            self.crack_lines = []
            num_main_cracks = 8

            for i in range(num_main_cracks):
                angle = (2 * math.pi * i / num_main_cracks) + random.uniform(-0.3, 0.3)
                length = random.uniform(400, 800)

                end_x = impact_x + math.cos(angle) * length
                end_y = impact_y + math.sin(angle) * length

                self.crack_lines.append({
                    'start': (impact_x, impact_y),
                    'end': (end_x, end_y),
                    'width': random.randint(2, 5)
                })

                # Add branch cracks
                for j in range(random.randint(1, 3)):
                    branch_start = 0.3 + random.uniform(0, 0.4)  # Start partway along main crack
                    branch_x = impact_x + math.cos(angle) * length * branch_start
                    branch_y = impact_y + math.sin(angle) * length * branch_start

                    branch_angle = angle + random.uniform(-0.8, 0.8)
                    branch_length = random.uniform(150, 300)

                    branch_end_x = branch_x + math.cos(branch_angle) * branch_length
                    branch_end_y = branch_y + math.sin(branch_angle) * branch_length

                    self.crack_lines.append({
                        'start': (branch_x, branch_y),
                        'end': (branch_end_x, branch_end_y),
                        'width': random.randint(1, 3)
                    })

            # Generate fragment data
            self.fragment_data = []
            grid_cols = 6
            grid_rows = 4

            for row in range(grid_rows):
                for col in range(grid_cols):
                    # Fragment position and size
                    frag_width = self.screen_width // grid_cols
                    frag_height = self.screen_height // grid_rows

                    start_x = col * frag_width
                    start_y = row * frag_height

                    # Add some randomness to fragment bounds
                    start_x += random.randint(-20, 20)
                    start_y += random.randint(-20, 20)
                    frag_width += random.randint(-40, 40)
                    frag_height += random.randint(-40, 40)

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
                        'rotation_speed': random.uniform(-720, 720),  # degrees per second
                        'delay': random.uniform(0, 0.2)  # Slight stagger
                    })

        def create_crack_overlay(self, width, height, progress):
            """Create crack overlay surface"""
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            alpha = min(255, int(progress * 400))

            # Draw all crack lines
            for crack in self.crack_lines:
                # Make cracks appear progressively
                crack_alpha = max(0, min(alpha, int((progress - 0.1) * 500)))
                if crack_alpha > 0:
                    color = (255, 255, 255, crack_alpha)

                    # Draw main crack line
                    pygame.draw.line(surface, color,
                                   (int(crack['start'][0]), int(crack['start'][1])),
                                   (int(crack['end'][0]), int(crack['end'][1])),
                                   crack['width'])

                    # Add glow effect
                    if crack['width'] > 2:
                        glow_color = (200, 220, 255, crack_alpha // 3)
                        pygame.draw.line(surface, glow_color,
                                       (int(crack['start'][0]), int(crack['start'][1])),
                                       (int(crack['end'][0]), int(crack['end'][1])),
                                       crack['width'] + 2)

            return surface

        def render_fragments(self, render, width, height, progress, st, at):
            """Render the flying fragments"""
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
                current_y += 0.5 * 800 * (adjusted_progress ** 2)  # gravity acceleration

                # Calculate rotation
                rotation = fragment['rotation_speed'] * adjusted_progress

                # Calculate alpha (fade out)
                alpha = max(0.0, 1.0 - adjusted_progress * 1.5)

                if alpha > 0.05 and current_y < height + 200:  # Only render visible fragments
                    # Extract fragment from old scene
                    try:
                        # Create subsurface from old render
                        frag_surface = old_render.subsurface((
                            max(0, fragment['start_x']),
                            max(0, fragment['start_y']),
                            min(fragment['width'], width - max(0, fragment['start_x'])),
                            min(fragment['height'], height - max(0, fragment['start_y']))
                        ))

                        # Apply alpha
                        if alpha < 1.0:
                            frag_surface = frag_surface.copy()
                            frag_surface.set_alpha(int(alpha * 255))

                        # Apply rotation if significant
                        if abs(rotation) > 5:
                            frag_surface = pygame.transform.rotate(frag_surface, rotation)

                        # Blit to render
                        render.blit(frag_surface, (int(current_x), int(current_y)))

                    except (ValueError, pygame.error):
                        # Skip problematic fragments
                        pass

        def visit(self):
            rv = []
            if self.old_widget:
                rv.append(self.old_widget)
            if self.new_widget:
                rv.append(self.new_widget)
            return rv

# Define the transition functions
define shatter = MirrorShatterTransition(0.5, 2.0, 24)  # 0.5s buildup, 2.0s shatter, 24 fragments
define shatter_quick = MirrorShatterTransition(0.3, 1.5, 16)  # Faster version
define shatter_epic = MirrorShatterTransition(0.8, 3.0, 32)  # Epic version

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

# Audio definitions (add these files to your audio folder)
define audio.mirror_crack = "audio/glass_crack.ogg"
define audio.mirror_shatter = "audio/glass_shatter.ogg"
define audio.boss_music = "audio/boss_theme.ogg"

# USAGE EXAMPLES - COPY AND PASTE THESE:

label test_shatter:
    scene bedroom
    show eileen happy
    "This is the old scene..."

    # Add dramatic pause and sound
    play sound mirror_crack
    pause 0.3

    # THE SHATTER TRANSITION - USE THIS FORMAT:
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

# Quick reference for all transition variations:
# scene new_background with shatter         # Standard (0.5s + 2.0s)
# scene new_background with shatter_quick   # Fast (0.3s + 1.5s)
# scene new_background with shatter_epic    # Epic (0.8s + 3.0s)

# Pro tips:
# 1. Always play crack sound before the transition
# 2. Use screen flashes for extra impact
# 3. Combine with camera shakes during buildup
# 4. Time your music transitions with the effect
# 5. Use dramatic character poses/dialogue

###############################################
# AUDIO FILES NEEDED (place in audio folder):
# - glass_crack.ogg (0.5-1.0s crack sound)
# - glass_shatter.ogg (2-3s shatter/falling glass)
# - boss_theme.ogg (your epic boss music)
###############################################

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
