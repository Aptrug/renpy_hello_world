# transitions_shatter.rpy — mirror-shatter transition
# Works on Ren'Py 7.x/8.x. Paste anywhere (init time).

init -2 python:
    from renpy.display import im
    from renpy.display.transition import Pause   # <-- import the transition version

    def make_mirror_shatter(
        mask="mirror_shatter_mask.png",
        seconds=0.65,
        ramplen=32,
        hit=True,
        reverse=False,
        ease=_warper.easein,
    ):
        """
        Returns a transition that looks like the screen shattering like a mirror.
        """
        # Use the mask if available; otherwise fall back to a plain dissolve.
        if renpy.loadable(mask):
            ctrl = im.Scale(mask, config.screen_width, config.screen_height)
            base = ImageDissolve(
                ctrl, seconds, ramplen=ramplen, reverse=reverse, time_warp=ease
            )
        else:
            base = Dissolve(seconds, time_warp=ease)

        if hit:
            return MultipleTransition([
                False, vpunch, False,                 # punch
                False, Pause(0.05), False,            # tiny beat (transition pause, now correct)
                False, base, True,                    # dissolve with mask
            ])
        else:
            return base

    # Ready-made variants
    mirror_shatter       = make_mirror_shatter()
    mirror_shatter_fast  = make_mirror_shatter(seconds=0.45, ramplen=16)
    mirror_shatter_big   = make_mirror_shatter(seconds=0.90, ramplen=64)

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
