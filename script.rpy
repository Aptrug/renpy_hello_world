default current_round = 59
default max_ap = 9
default available_ap = 3

init python:
    import math

    renpy.register_shader("custom.radial_gradient", variables="""
        uniform vec4 u_center_color;
        uniform vec4 u_edge_color;
        uniform vec2 u_model_size;
        varying float v_done;
        attribute vec4 a_position;
    """, vertex_300="""
        vec2 center = u_model_size / 2.0;
        vec2 pixel = vec2(a_position.xy) - center;
        v_done = length(pixel) / length(center);
    """, fragment_300="""
        float radius_factor = 1.0 / sqrt(2.0);
        float done = v_done / radius_factor;
        if (done > 1.0) {
            discard;
        }
        gl_FragColor *= mix(u_center_color, u_edge_color, done);
    """)

transform radial_bg_gradient(center_color=(0.502, 0.502, 0.502, 1.0), edge_color=(0.314, 0.314, 0.314, 1.0)):
    shader "custom.radial_gradient"
    u_center_color center_color
    u_edge_color edge_color

transform radial_orb_gradient(center_color=(1.0, 0.843, 0.0, 1.0), edge_color=(0.854, 0.647, 0.125, 1.0)):
    shader "custom.radial_gradient"
    u_center_color center_color
    u_edge_color edge_color

transform orb_glow:
    zoom 1.2
    blur 15
    alpha 0.5

define round_bg_base = Solid("#ffffff", xsize=250, ysize=250)
define orb_base = Solid("#ffffff", xsize=50, ysize=50)

screen round_indicator():
    fixed:
        xysize (250, 250)

        add round_bg_base at radial_bg_gradient xalign 0.5 yalign 0.5

        text "Round" xalign 0.5 ypos 60 size 36 color "#ffffff" outlines [(absolute(2), "#00000080", absolute(2), absolute(2))] text_align 0.5

        text "[current_round]" xalign 0.5 ypos 100 size 90 color "#ffffff" outlines [(absolute(2), "#00000080", absolute(2), absolute(2))] text_align 0.5

        for i in range(max_ap):
            $ angle = (float(i) / max_ap) * 2 * math.pi - math.pi / 2
            $ x = int(125 + 125 * math.cos(angle))
            $ y = int(125 + 125 * math.sin(angle))

            if i < available_ap:
                add orb_base at [radial_orb_gradient, orb_glow] xpos x ypos y anchor (0.5, 0.5)

            add orb_base at radial_orb_gradient xpos x ypos y anchor (0.5, 0.5)
