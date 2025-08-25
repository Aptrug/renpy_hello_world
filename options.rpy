## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.

## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("HelloWorld")


# define config.menu_include_disabled = True


## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = True


## The version of the game.

define config.version = "1.0"


## Text that is placed on the game's about screen. Place the text between the
## triple-quotes, and leave a blank line between paragraphs.

define gui.about = _p("""
""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "HelloWorld"


## Sounds and music ############################################################

## These three variables control, among other things, which mixers are shown
## to the player by default. Setting one of these to False will hide the
## appropriate mixer.

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

# define config.main_menu_music = "main-menu-theme.ogg"


## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## Between screens of the game menu.

define config.intra_transition = dissolve


## A transition that is used after a game has been loaded.

define config.after_load_transition = None


## Used when entering the main menu after the game has ended.

define config.end_game_transition = None


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "auto"


## Transitions used to show and hide the dialogue window

# define config.window_show_transition = Dissolve(.2)
# define config.window_hide_transition = Dissolve(.2)


## Preference defaults #########################################################

## Controls the default text speed. The default, 0, is infinite, while any
## other number is the number of characters per second to type out.

default preferences.text_cps = 0

default preferences.fullscreen = True

# default preferences.text_cps = 60


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


## Save directory ##############################################################
##
## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "HelloWorld-1753816742"


## Icon ########################################################################
##
## The icon displayed on the taskbar or dock.

define config.window_icon = "gui/window_icon.png"


## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:
    # Store the original menu function
    _original_renpy_menu = renpy.exports.menu

    def enhanced_menu(items, set_expr, args=None, kwargs=None, item_arguments=None):
        """
        Enhanced menu function that supports the exact syntax you want:
        "Text" if condition explanation "reason"
        """
        import re

        if item_arguments is None:
            item_arguments = [((), {})] * len(items)

        processed_items = []
        processed_item_arguments = []

        for (label, condition, value), (item_args, item_kwargs) in zip(items, item_arguments):

            # Check if the condition string contains "explanation"
            explanation = None
            actual_condition = condition

            if condition and " explanation " in condition:
                # Split condition and explanation
                parts = condition.split(" explanation ", 1)
                actual_condition = parts[0].strip()
                explanation_text = parts[1].strip()

                # Remove quotes from explanation if present
                if explanation_text.startswith('"') and explanation_text.endswith('"'):
                    explanation = explanation_text[1:-1]
                elif explanation_text.startswith("'") and explanation_text.endswith("'"):
                    explanation = explanation_text[1:-1]
                else:
                    explanation = explanation_text

            # Evaluate the actual condition
            try:
                condition_result = renpy.python.py_eval(actual_condition) if actual_condition else True
            except:
                condition_result = False

            if condition_result:
                # Active choice - show normally
                processed_items.append((label, actual_condition, value))
            elif explanation is not None:
                # Disabled choice with explanation - show grayed out
                disabled_label = label + " " + explanation
                processed_items.append((disabled_label, "True", None))
            # If condition is false and no explanation, hide completely

            processed_item_arguments.append((item_args, item_kwargs))

        # Call the original menu function with processed items
        return _original_renpy_menu(processed_items, set_expr, args, kwargs, processed_item_arguments)

    # Replace the menu function everywhere it might be called
    renpy.exports.menu = enhanced_menu

    # Import the menuexports module and replace there too
    import renpy.exports.menuexports
    renpy.exports.menuexports.menu = enhanced_menu

    # Ensure disabled menu items are shown
    config.menu_include_disabled = True


init python:
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


    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base directory,
    ## with and without a leading /. If multiple patterns match, the first is
    ## used.
    ##
    ## In a pattern:
    ##
    ## / is the directory separator.
    ##
    ## * matches all characters, except the directory separator.
    ##
    ## ** matches all characters, including the directory separator.
    ##
    ## For example, "*.txt" matches txt files in the base directory,
    ## "game/**.ogg" matches ogg files in the game directory or any of its
    ## subdirectories, and "**.psd" matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app build,
    ## so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')


## A Google Play license key is required to perform in-app purchases. It can be
## found in the Google Play developer console, under "Monetize" > "Monetization
## Setup" > "Licensing".

# define build.google_play_key = "..."


## The username and project name associated with an itch.io project, separated
## by a slash.

# define build.itch_project = "renpytom/test-project"
