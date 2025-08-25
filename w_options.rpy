# define config.menu_include_disabled = True

default preferences.fullscreen = True

# default preferences.text_cps = 60

init python:
    # For overriding menu
    def enhanced_menu(items, set_expr, args=None, kwargs=None, item_arguments=None):
        """Enhanced menu with explanation syntax"""
        processed_items = []
        for label, condition, value in items:
            if condition and " explanation " in condition:
                cond, explanation = condition.split(" explanation ", 1)
                explanation = explanation.strip('"\'')
                if renpy.python.py_eval(cond or "True"):
                    # Condition true - show normally
                    processed_items.append((label, cond, value))
                else:
                    # Condition false - show as disabled caption with explanation
                    processed_items.append((label + explanation, "True", None))
            else:
                # No explanation - only add if condition is true or no condition
                if not condition or renpy.python.py_eval(condition):
                    processed_items.append((label, condition, value))
                # If condition is false and no explanation, skip entirely

        return renpy.store._original_menu(processed_items, set_expr, args, kwargs, item_arguments)
    # Replace menu function
    renpy.store._original_menu = renpy.exports.menu
    renpy.exports.menu = enhanced_menu
    config.menu_include_disabled = True

    # import renpy.exports as renpy_exports
        # import time
        # for slot in renpy.list_slots():
        #     if slot.startswith("auto-"):
        #         mtime = renpy.slot_mtime(slot)
        #         print(f"{slot}: {time.ctime(mtime)}")

    # 4 * 3 + 1 = 13
    config.autosave_slots = 13
    config.quicksave_slots = 13

    def save_notify():
        savedir = renpy.config.savedir
        latest_save = renpy.newest_slot("")
        savefile = savedir + "/" + latest_save
        renpy.notify(_("Stored the savefile as ") + savefile)

    config.autosave_callback = save_notify

    config.hw_video = False

    # show disabled stuff as well
    # menu_include_disabled = True

    # config.save_directory = "saves"

    # config.screenshot_callback = lambda filename: renpy.notify("Saved at " + filename)

    config.mouse = {
            "default": [ ("misc/volantes_cursors/default.webp", 0, 0) ],
            "button": [ ("misc/volantes_cursors/pointer.webp", 0, 0) ],
            "prompt": [ ("misc/volantes_cursors/text.webp", 0, 0) ],
            'pause': [
                ("misc/volantes_cursors/progress-01.webp", 0, 0),
                ("misc/volantes_cursors/progress-02.webp", 0, 0),
                ("misc/volantes_cursors/progress-03.webp", 0, 0),
                ("misc/volantes_cursors/progress-04.webp", 0, 0),
                ("misc/volantes_cursors/progress-05.webp", 0, 0),
                ("misc/volantes_cursors/progress-06.webp", 0, 0),
                ("misc/volantes_cursors/progress-07.webp", 0, 0),
                ("misc/volantes_cursors/progress-08.webp", 0, 0),
                ("misc/volantes_cursors/progress-09.webp", 0, 0),
                ("misc/volantes_cursors/progress-10.webp", 0, 0),
                ("misc/volantes_cursors/progress-11.webp", 0, 0),
                ("misc/volantes_cursors/progress-12.webp", 0, 0)
            ]
    }

    config.say_attribute_transition = Dissolve(0.5) # 0.3 might be better

    # config.window_show_transition = Fade(0.25, 0.0, 0.25)
    # config.window_hide_transition = Fade(0.25, 0.0, 0.25)
    config.window_show_transition = Dissolve(0.2)
    config.window_hide_transition = Dissolve(0.2)

    # define config.window_hide_transition = { "screens" : Dissolve(1.0) } = fade(1.0)

    # config.default_text_cps = 25

    # config.developer = True

    # Auto name handling
    # config.automatic_images = ['_']
    # config.automatic_images_strip = ['_']
    # define config.automatic_images_strip = ['_', ' ', '/']
