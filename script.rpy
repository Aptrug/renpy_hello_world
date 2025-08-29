# ========================
# Python: Circle + Orb Positions
# ========================
init python:
    import math

    class Circle(renpy.Displayable):
        def __init__(self, radius, color, border_color=None, border_width=2, **kwargs):
            super().__init__(**kwargs)
            self.radius = radius
            self.color = color
            self.border_color = border_color
            self.border_width = border_width

        def render(self, width, height, st, at):
            render = renpy.Render(self.radius*2, self.radius*2)
            canvas = render.canvas()
            canvas.circle(self.color, (self.radius, self.radius), self.radius)
            if self.border_color:
                canvas.circle(self.border_color, (self.radius, self.radius), self.radius, self.border_width)
            return render

    def get_orb_positions(num_orbs, orb_radius=ORB_RADIUS, distance=ORB_DISTANCE, center=ROUND_RADIUS):
        return [
            (
                int(center + distance * math.cos(2*math.pi*i/num_orbs - math.pi/2) - orb_radius),
                int(center + distance * math.sin(2*math.pi*i/num_orbs - math.pi/2) - orb_radius)
            )
            for i in range(num_orbs)
        ]

    def get_orb_display(i, available_ap):
        return (orb_active, orb_glow) if i < available_ap else (orb_inactive_img, orb_inactive)

# ========================
# Main UI Screen
# ========================
screen round_ui():
    fixed:
        xalign 0.5
        yalign 0.75
        xsize ROUND_RADIUS*2
        ysize ROUND_RADIUS*2

        # Round circle background with breathing animation
        add round_bg at round_breathe xpos 0 ypos 0

        # Round number in the center
        vbox:
            xalign 0.5
            yalign 0.5
            spacing -5

            text "Round":
                size 22
                color "#FFFFFF"
                xalign 0.45
                outlines [(2, "#000000", 0, 0)]

            text "[current_round]":
                size 56
                color "#FFFFFF"
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

        # Orbs arranged around the circle
        $ orb_positions = get_orb_positions(max_ap)
        for i, (x, y) in enumerate(orb_positions):
            $ orb_img, orb_tr = get_orb_display(i, available_ap)
            add orb_img at orb_tr xpos x ypos y
