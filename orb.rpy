# Import math module
init python:
    import math

# Define variables for the UI state
default current_round = 59
default max_ap = 9
default available_ap = 3

# Define the screen for the round and AP indicator
# Alternative version using a custom displayable for more control
init python:
    import math

    class RoundAPIndicator(renpy.Displayable):
        def __init__(self, round_num, max_ap, available_ap, **kwargs):
            super(RoundAPIndicator, self).__init__(**kwargs)
            self.round_num = round_num
            self.max_ap = max_ap
            self.available_ap = available_ap

            # Load orb images
            self.orb_active = renpy.displayable("orb_active.png")
            self.orb_inactive = renpy.displayable("orb_inactive.png")

            # Try to load background, fallback to None
            try:
                self.round_bg = renpy.displayable("round_bg.png")
            except:
                self.round_bg = None

        def render(self, width, height, st, at):
            render = renpy.Render(250, 250)

            # Draw background
            if self.round_bg:
                bg_render = renpy.render(self.round_bg, 250, 250, st, at)
                render.blit(bg_render, (0, 0))
            else:
                # Create a simple circular background
                render.canvas().circle("#505050", (125, 125), 125)
                render.canvas().circle("#808080", (125, 125), 123, width=2)

            # Draw round text
            round_text = Text("Round", size=36, color="#FFFFFF", outlines=[(2, "#000000", 0, 0)])
            num_text = Text(str(self.round_num), size=90, color="#FFFFFF", outlines=[(2, "#000000", 0, 0)])

            round_render = renpy.render(round_text, width, height, st, at)
            num_render = renpy.render(num_text, width, height, st, at)

            # Center the text
            round_w, round_h = round_render.get_size()
            num_w, num_h = num_render.get_size()

            render.blit(round_render, (125 - round_w // 2, 125 - round_h // 2 - 30))
            render.blit(num_render, (125 - num_w // 2, 125 - num_h // 2 + 20))

            # Draw orbs in circle
            radius = 125
            orb_size = 32

            for i in range(self.max_ap):
                angle = (i / self.max_ap) * 2 * math.pi - math.pi / 2
                x_pos = int(radius + radius * math.cos(angle) - orb_size / 2)
                y_pos = int(radius + radius * math.sin(angle) - orb_size / 2)

                if i < self.available_ap:
                    orb_render = renpy.render(self.orb_active, orb_size, orb_size, st, at)
                else:
                    orb_render = renpy.render(self.orb_inactive, orb_size, orb_size, st, at)

                render.blit(orb_render, (x_pos, y_pos))

            return render

        def event(self, ev, x, y, st):
            return None

# Screen using the custom displayable
screen round_ap_indicator_custom():
    add RoundAPIndicator(current_round, max_ap, available_ap) xalign 0.5 yalign 0.5
