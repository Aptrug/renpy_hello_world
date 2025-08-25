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


python early:
    def parse_mymenu(lex):
        """Parse mymenu statement with reason support"""
        # Get prompt if present
        if not lex.eol():
            prompt = lex.rest()
            lex.advance()
        else:
            lex.advance()

        choices = []
        while not lex.eol():
            # Parse choice text
            text = lex.require(lex.string)

            # Default values
            condition = "True"
            reason = None

            # Check for condition
            if lex.keyword("if"):
                condition = lex.require(lex.python_expression)

            # Check for reason (new syntax: "reason" "text")
            if lex.keyword("reason"):
                reason = lex.require(lex.string)

            lex.expect(':')
            lex.expect_eol()
            lex.advance()

            # Parse choice block
            block = lex.subblock_lexer().renpy_block()
            choices.append((text, condition, reason, block))

        return choices

    def execute_mymenu(choices):
        """Execute mymenu with grayed out reasons"""
        # Build menu items with reasons for disabled choices
        menu_items = []
        choice_blocks = {}

        for i, (text, condition, reason, block) in enumerate(choices):
            choice_id = f"choice_{i}"
            is_available = renpy.python.py_eval(condition)

            # Add reason to disabled choices
            if not is_available and reason:
                display_text = f"{text} ({reason})"
            else:
                display_text = text

            menu_items.append((display_text, condition, choice_id))
            choice_blocks[choice_id] = block

        # Use regular Ren'Py menu
        result = renpy.store.menu(menu_items)

        # Execute selected choice block
        if result in choice_blocks:
            renpy.ast.execute_block(choice_blocks[result])

    # Register the mymenu statement
    renpy.register_statement("mymenu", parse_mymenu, execute_mymenu)

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
