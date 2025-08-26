# transitions_shatter.rpy — mirror-shatter transition
# Works on Ren'Py 7.x/8.x. Paste anywhere (init time).
# You only need to add a mask image (see section 2) and, optionally, a shatter SFX.

init -2 python:
    # For safe image scaling to your game's base resolution.
    from renpy.display import im

    def make_mirror_shatter(
        mask="fx/mirror_shatter_mask.png",
        seconds=0.65,
        ramplen=32,
        hit=True,
        reverse=False,
        ease=_warper.easein,   # feels like accelerating shards
    ):
        """
        Returns a transition that looks like the screen shattering like a mirror.

        mask     : grayscale (or alpha) control image. White = breaks first, black = last.
        seconds  : duration of the actual dissolve (not counting the impact punch).
        ramplen  : power-of-two ramp; higher = smoother edge (16–64 recommended).
        hit      : if True, prefaces the dissolve with a quick vpunch (impact).
        reverse  : flip black/white priority if your mask is inverted.
        ease     : time warp for the dissolve curve (from _warper).
        """
        # Use the mask if available; otherwise fall back to a plain dissolve (no crashes).
        if renpy.loadable(mask):
            ctrl = im.Scale(mask, config.screen_width, config.screen_height)
            base = ImageDissolve(
                ctrl, seconds, ramplen=ramplen, reverse=reverse, time_warp=ease
            )
        else:
            base = Dissolve(seconds, time_warp=ease)

        if hit:
            # Sequence: impact punch → tiny pause → shatter dissolve.
            return MultipleTransition([
                False, vpunch, False,          # punch the *old* scene quickly
                False, Pause(0.05), False,     # tiny beat helps the SFX land
                False, base, True,             # dissolve from old → new using the shatter mask
            ])
        else:
            return base

# Ready-made variants you can call with "with ..."
define mirror_shatter       = make_mirror_shatter()
define mirror_shatter_fast  = make_mirror_shatter(seconds=0.45, ramplen=16)
define mirror_shatter_big   = make_mirror_shatter(seconds=0.90, ramplen=64)

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
