# Epic Mirror Shatter Transition for Ren'Py Boss Fight
# Place this code in a .rpy file in your game directory

# Initialize the shatter effect components
init python:
    import random
    import math

    class ShatterFragment:
        def __init__(self, x, y, width, height, velocity_x, velocity_y, rotation_speed):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y
            self.rotation = 0
            self.rotation_speed = rotation_speed
            self.alpha = 1.0

        def update(self, dt):
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
            self.velocity_y += 800 * dt  # Gravity
            self.rotation += self.rotation_speed * dt
            self.alpha = max(0, self.alpha - dt * 2)

    class ShatterEffect(renpy.Displayable):
        def __init__(self, child, duration=2.0, fragments=20, **kwargs):
            super(ShatterEffect, self).__init__(**kwargs)
            self.child = child
            self.duration = duration
            self.fragments = fragments
            self.start_time = None
            self.fragment_list = []
            self.initialized = False

        def render(self, width, height, st, at):
            if not self.initialized:
                self.setup_fragments(width, height)
                self.initialized = True
                self.start_time = st

            render = renpy.Render(width, height)

            if self.start_time is None:
                self.start_time = st

            elapsed = st - self.start_time

            # Pre-shatter phase (first 0.3 seconds)
            if elapsed < 0.3:
                # Screen shake and crack overlay
                shake_x = random.randint(-10, 10) if elapsed > 0.1 else 0
                shake_y = random.randint(-5, 5) if elapsed > 0.1 else 0

                child_render = renpy.render(self.child, width, height, st, at)
                render.blit(child_render, (shake_x, shake_y))

                # Add crack overlay that gets more intense
                crack_alpha = min(255, elapsed * 850)
                if crack_alpha > 0:
                    crack_surface = self.create_crack_overlay(width, height, crack_alpha)
                    render.blit(crack_surface, (0, 0))

            # Shatter phase
            elif elapsed < self.duration:
                # Update and render fragments
                dt = 0.016  # Assume 60fps
                for fragment in self.fragment_list:
                    fragment.update(dt)

                    if fragment.alpha > 0:
                        fragment_render = self.render_fragment(fragment, st, at)
                        render.blit(fragment_render, (int(fragment.x), int(fragment.y)))

            # Request redraw if animation is ongoing
            if elapsed < self.duration:
                renpy.redraw(self, 0.01)

            return render

        def setup_fragments(self, width, height):
            """Create fragments in a realistic crack pattern"""
            self.fragment_list = []

            # Create center impact point
            center_x = width * 0.5
            center_y = height * 0.4  # Slightly above center for dramatic effect

            # Generate fragments in a radial pattern from impact
            for i in range(self.fragments):
                angle = (2 * math.pi * i) / self.fragments + random.uniform(-0.5, 0.5)
                distance = random.uniform(50, 200)

                # Fragment position
                frag_x = center_x + math.cos(angle) * distance
                frag_y = center_y + math.sin(angle) * distance

                # Fragment size (larger near center, smaller at edges)
                size_factor = max(0.3, 1.0 - distance / 300)
                frag_width = random.randint(30, 80) * size_factor
                frag_height = random.randint(30, 80) * size_factor

                # Velocity based on distance from center (explosion effect)
                vel_x = math.cos(angle) * random.uniform(200, 400)
                vel_y = math.sin(angle) * random.uniform(200, 400) - 100  # Slight upward bias

                rotation_speed = random.uniform(-360, 360)  # Degrees per second

                fragment = ShatterFragment(frag_x, frag_y, frag_width, frag_height, vel_x, vel_y, rotation_speed)
                self.fragment_list.append(fragment)

        def create_crack_overlay(self, width, height, alpha):
            """Create a crack pattern overlay"""
            surf = renpy.display.pgrender.surface((width, height), True)
            surf.fill((0, 0, 0, 0))

            # Draw crack lines radiating from center
            center_x, center_y = width // 2, height // 2

            import pygame
            for i in range(8):
                angle = (2 * math.pi * i) / 8
                end_x = center_x + math.cos(angle) * width
                end_y = center_y + math.sin(angle) * height

                # Main crack line
                pygame.draw.line(surf, (255, 255, 255, min(255, alpha)),
                               (center_x, center_y), (int(end_x), int(end_y)), 3)

                # Secondary cracks
                for j in range(2):
                    branch_angle = angle + random.uniform(-0.3, 0.3)
                    branch_length = random.uniform(100, 300)
                    branch_x = center_x + math.cos(branch_angle) * branch_length
                    branch_y = center_y + math.sin(branch_angle) * branch_length
                    pygame.draw.line(surf, (200, 200, 200, min(200, alpha // 2)),
                                   (center_x, center_y), (int(branch_x), int(branch_y)), 2)

            return surf

        def render_fragment(self, fragment, st, at):
            """Render individual fragment with rotation and fading"""
            # Create a small render for the fragment
            frag_render = renpy.Render(int(fragment.width), int(fragment.height))

            # For simplicity, we'll use colored rectangles as fragments
            # In a real implementation, you'd use pieces of the original image
            surf = renpy.display.pgrender.surface((int(fragment.width), int(fragment.height)), True)

            import pygame
            color_intensity = int(fragment.alpha * 255)
            # Glass-like colors
            colors = [(200, 220, 255), (180, 200, 240), (220, 230, 255)]
            color = random.choice(colors)
            color = (min(255, color[0]), min(255, color[1]), min(255, color[2]), color_intensity)

            surf.fill(color)

            # Add some edge highlights to make it look like glass
            if fragment.alpha > 0.5:
                pygame.draw.rect(surf, (255, 255, 255, color_intensity // 2),
                               (0, 0, int(fragment.width), int(fragment.height)), 2)

            frag_render.blit(surf, (0, 0))
            return frag_render

        def visit(self):
            return [self.child]

# Custom shader for glass distortion effect (if using renpy-shader)
init python:
    # Glass shatter shader code
    glass_shatter_vertex = """
    #version 110
    attribute vec2 a_position;
    attribute vec2 a_tex_coord;
    varying vec2 v_tex_coord;
    uniform float u_time;
    uniform vec2 u_impact_point;

    void main() {
        v_tex_coord = a_tex_coord;
        vec2 pos = a_position;

        // Calculate distance from impact point
        float dist = distance(pos, u_impact_point);
        float wave = sin(dist * 10.0 - u_time * 20.0) * 0.02;

        // Apply distortion based on time and distance
        if (u_time > 0.1) {
            pos += normalize(pos - u_impact_point) * wave * (1.0 - u_time);
        }

        gl_Position = vec4(pos, 0.0, 1.0);
    }
    """

    glass_shatter_fragment = """
    #version 110
    varying vec2 v_tex_coord;
    uniform sampler2D tex0;
    uniform float u_time;
    uniform vec2 u_resolution;
    uniform vec2 u_impact_point;

    void main() {
        vec2 uv = v_tex_coord;
        vec4 color = texture2D(tex0, uv);

        // Calculate distance from impact point
        float dist = distance(uv * u_resolution, u_impact_point);

        // Create crack pattern
        float crack = 0.0;
        for (int i = 0; i < 8; i++) {
            float angle = float(i) * 0.785398; // 45 degrees in radians
            vec2 crack_dir = vec2(cos(angle), sin(angle));
            vec2 to_point = (uv * u_resolution - u_impact_point);
            float line_dist = abs(dot(to_point, vec2(-crack_dir.y, crack_dir.x)));
            crack += 1.0 / (1.0 + line_dist * 0.1);
        }

        // Apply shatter effect based on time
        if (u_time > 0.3) {
            float shatter_intensity = (u_time - 0.3) * 5.0;
            color.rgb += crack * 0.3;
            color.a *= max(0.0, 1.0 - shatter_intensity);
        } else {
            // Pre-shatter cracks
            color.rgb += crack * u_time * 3.0;
        }

        gl_FragColor = color;
    }
    """

# ATL Transforms for the shatter effect
transform mirror_impact:
    ease 0.1 zoom 1.02
    ease 0.1 zoom 0.98
    ease 0.1 zoom 1.01
    ease 0.1 zoom 1.0

transform screen_shake:
    parallel:
        ease 0.05 xoffset 5
        ease 0.05 xoffset -5
        ease 0.05 xoffset 3
        ease 0.05 xoffset -3
        ease 0.05 xoffset 0
    parallel:
        ease 0.05 yoffset -3
        ease 0.05 yoffset 3
        ease 0.05 yoffset -2
        ease 0.05 yoffset 2
        ease 0.05 yoffset 0

transform dramatic_zoom_out:
    ease 2.0 zoom 0.0 alpha 0.0

# Audio cue definitions
define audio.glass_crack = "Crash_Glass_04.opus"  # You'll need this sound file
define audio.glass_shatter = "Crash_Glass_04.opus"  # You'll need this sound file
define audio.boss_theme = "Crash_Glass_04.opus"  # Your boss battle music

# Screen overlay for additional effects
screen shatter_overlay():
    modal True
    zorder 200

    # Flash effect
    add "#ffffff" at flash_effect

    # Particle effects (if you have them)
    # add "particles/glass_particles.png" at particle_effect

transform flash_effect:
    alpha 0.8
    ease 0.1 alpha 0.0

# The main shatter transition function
init python:
    def shatter_transition(old_scene, new_scene, duration=2.5):
        """
        Create an epic mirror shatter transition between scenes
        """
        return MultipleTransition([
            # Phase 1: Impact and cracking (0.3 seconds)
            Fade(0.05, 0.05, 0.05),
            # Phase 2: Shatter effect (2.0 seconds)
            ShatterEffect(old_scene, duration=duration),
            # Phase 3: Reveal new scene (0.2 seconds)
            Dissolve(0.2)
        ])

# Usage examples and the main transition
label demo_shatter_transition:
    scene black
    "Preparing for epic boss battle..."

    # Set up the scene before shattering
    scene peaceful_meadow
    show protagonist happy
    "Everything seems calm..."

    # THE EPIC SHATTER MOMENT
    play sound glass_crack
    show protagonist shocked at mirror_impact
    "What's that sound?!"

    # Build tension with screen shake
    camera at screen_shake
    play sound glass_shatter

    # Show the shatter overlay for visual impact
    show screen shatter_overlay
    pause 0.3
    hide screen shatter_overlay

    # THE MAIN SHATTER TRANSITION
    scene boss_arena with shatter_transition(2.5)
    play music boss_theme fadeout 1.0 fadein 2.0

    # Boss appears dramatically
    show boss_final_form at dramatic_zoom_out
    boss "You thought you could escape me?!"

    # Continue with your boss fight...
    return

# Alternative: Simple version using built-in transitions with effects
transform shatter_simple:
    # Quick version using standard Ren'Py transitions
    parallel:
        ease 0.2 zoom 1.1 rotate 2
        ease 0.3 zoom 0.8 rotate -5 alpha 0.7
        ease 0.5 zoom 0.0 rotate 15 alpha 0.0
    parallel:
        ease 0.3 xoffset 10
        ease 0.2 xoffset -15
        ease 0.5 xoffset 50

# Quick usage for the simple version:
# scene new_background with Dissolve(1.0):
#     at shatter_simple

# Screen flash effect for dramatic impact
screen impact_flash():
    modal True
    zorder 1000
    add "#ffffff"
    timer 0.1 action Hide("impact_flash")

# Complete example scene
label boss_fight_entrance:
    scene throne_room
    show hero determined at center

    hero "I've finally found your lair!"

    # Build suspense
    play sound "audio/rumble.ogg"
    camera at vpunch

    "The ground begins to shake..."

    # The mirror shatters revealing the boss
    play sound glass_crack
    show screen impact_flash

    # Use the epic shatter transition
    scene boss_dimension with shatter_transition(3.0)
    play music boss_theme volume 0.8

    show boss_shadow at truecenter:
        alpha 0.0
        ease 2.0 alpha 1.0 zoom 1.2

    "Reality itself seems to crack and break apart!"

    show boss_final_form at center:
        alpha 0.0 zoom 2.0
        ease 1.5 alpha 1.0 zoom 1.0

    boss "Welcome to your nightmare, mortal!"

    # Your boss fight continues here...
    return

# Pro tip: Create custom displayables for even more control
init python:
    class GlassShardParticle(renpy.Displayable):
        def __init__(self, **kwargs):
            super(GlassShardParticle, self).__init__(**kwargs)
            self.particles = []
            for i in range(50):
                self.particles.append({
                    'x': random.randint(0, config.screen_width),
                    'y': random.randint(0, config.screen_height),
                    'vx': random.uniform(-200, 200),
                    'vy': random.uniform(-300, -50),
                    'size': random.uniform(2, 8),
                    'alpha': 1.0,
                    'rotation': random.uniform(0, 360)
                })

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)

            import pygame
            surf = pygame.Surface((width, height), pygame.SRCALPHA)

            for particle in self.particles:
                # Update particle
                particle['x'] += particle['vx'] * 0.016
                particle['y'] += particle['vy'] * 0.016
                particle['vy'] += 500 * 0.016  # gravity
                particle['alpha'] -= 0.016 * 2
                particle['rotation'] += random.uniform(-5, 5)

                if particle['alpha'] > 0:
                    # Draw particle as small white square (glass shard)
                    rect = pygame.Rect(int(particle['x']), int(particle['y']),
                                     int(particle['size']), int(particle['size']))
                    color = (255, 255, 255, int(particle['alpha'] * 255))
                    pygame.draw.rect(surf, color, rect)

            render.blit(surf, (0, 0))

            if st < 3.0:  # Animate for 3 seconds
                renpy.redraw(self, 0.016)

            return render

# Remember to add these files to your project:
# - audio/glass_crack.ogg (crack sound effect)
# - audio/glass_shatter.ogg (shatter sound effect)
# - audio/boss_battle.ogg (epic boss music)

# For best results, also create these image assets:
# - A cracked glass overlay PNG with transparency
# - Particle textures for glass shards
# - Boss arena background image
# - Boss character sprites

###############################################
# USAGE INSTRUCTIONS:
###############################################
# 1. Add the sound files mentioned above
# 2. Use "with shatter_transition(duration)" after scene statements
# 3. For quick usage: "scene new_bg at shatter_simple"
# 4. Call "show screen shatter_overlay" for extra visual impact
# 5. Combine with screen shake and flash effects for maximum drama
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
