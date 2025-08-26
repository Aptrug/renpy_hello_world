# Got a problem, main_menu screen text doesn't change outline when changing persistent.text_outline_size from settings, requires restart for changes to take effect instead of being instantaneous

I want persistent.text_outline_size to affect all text in the game (including menu text etc) and not apply only to game dialogue text

default persistent.quickmenu = True

default persistent.iconic_quickmenu = False

default persistent.text_outline_size = 3
define gui.text_outlines = [(persistent.text_outline_size, "#000", 0, 0)]

default persistent.dialogue_box_opacity = 0.0

default persistent.save_naming = False

default persistent.game_menu_opacity = 0.75

##############################################################################
# style quick_button_text:
#     outlines [(persistent.text_outline_size, "#000", 0, 0)]

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if persistent.quickmenu:
        if persistent.iconic_quickmenu:
            hbox:
                spacing 16
                style_prefix "quick"
                style "quick_menu"

                imagebutton:
                    auto "ui_elements/prefs/hide_quickmenu_%s.webp"
                    action HideInterface()

                imagebutton:
                    auto "ui_elements/prefs/rollback_%s.webp"
                    action Rollback()

                imagebutton:
                    auto "ui_elements/prefs/skip_%s.webp"
                    action Skip() alternate Skip(fast=True, confirm=True)

                imagebutton:
                    auto "ui_elements/prefs/auto_forward_%s.webp"
                    action Preference("auto-forward", "toggle")
                    # selected Preference("auto-forward", "disable")

                imagebutton:
                    auto "ui_elements/prefs/save_%s.webp"
                    action ShowMenu('save')

                imagebutton:
                    auto "ui_elements/prefs/screenshot_%s.webp"
                    action Screenshot()
        else:
            hbox:
                style_prefix "quick"
                # style_prefix "outlined_button"
                style "quick_menu"

                # adding text_outlines to every entry is tedious, but it works
                # persistent.text_outline_size won't update if done from styles
                textbutton _("Hide"):
                    action HideInterface()
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Back"):
                    action Rollback()
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("History"):
                    action ShowMenu('history')
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Skip"):
                    action Skip() alternate Skip(fast=True, confirm=True)
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Auto"):
                    action Preference("auto-forward", "toggle")
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Save"):
                    action ShowMenu('save')
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Q.Save"):
                    action QuickSave()
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Q.Load"):
                    action QuickLoad()
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Prefs"):
                    action ShowMenu('preferences')
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]
                textbutton _("Screenshot"):
                    action Screenshot()
                    text_outlines [(persistent.text_outline_size, "#000", 0, 0)]

##############################################################################

screen say(who, what):
    window:
        id "window"

        background Transform(style.window.background, alpha=persistent.dialogue_box_opacity)

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who:
                    id "who"
                    outlines [(persistent.text_outline_size, "#000", 0, 0)]

        text what:
            id "what"
            outlines [(persistent.text_outline_size, "#000", 0, 0)]


    ## If there's a side image, display it above the text. Do not display on
    ## the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

##############################################################################
screen main_menu():
    tag menu

    # Music
    on "show" action Play("music", "music/ave_maria.opus", loop=True)

    ## Animated background
    # add Movie(play="movies/snow_sky.webm", loop=True)

    add "deutsches_reich.webp"

    ## Menu container
    frame:
        background None
        xalign 0.05
        yalign 0.4

        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5

            textbutton _("Start"):
                action Start()
                style "hl2_button"
                hover_sound "sounds/hover.opus"
                activate_sound "sounds/bell.opus"

            textbutton _("Load"):
                action ShowMenu("load")
                style "hl2_button"
                hover_sound "sounds/hover.opus"
                activate_sound "sounds/click.opus"

            textbutton _("Preferences"):
                action ShowMenu("preferences")
                style "hl2_button"
                hover_sound "sounds/hover.opus"
                activate_sound "sounds/click.opus"

            textbutton _("Quit"):
                action Quit(confirm=not main_menu)
                style "hl2_button"
                hover_sound "sounds/hover.opus"
                activate_sound "sounds/click.opus"

# Rebundant
# style hl2_button:
#     background None
#     xalign 0.5
#     hover_background None

style hl2_button_text:
    color "#ffffff"  # White text
    hover_color "#ff9900"  # Orange on hover
    # outlines [(persistent.text_outline_size, "#000", 0, 0)]
    # hover_outlines [(persistent.text_outline_size, "#000", 0, 0)]
    size 36

##############################################################################
style game_menu_outer_frame:
    # bottom_padding 45
    # Change to reduce empty top space
    # top_padding 125
    # background "gui/overlay/game_menu.png"
    # background Solid("#000")
    background None

style game_menu_navigation_frame:
    # Change to make left side smaller
    # xsize 420
    xsize 350
    # yfill True

style game_menu_content_frame:
    # Was 60
    left_margin 40
    # right_margin 30
    # top_margin 15

#### #########################################################################

define get_save_notify_action = lambda slot: Show(
    "save_notify",
    message=_("Stored the savefile as ") + renpy.config.savedir + "/" + str(persistent._file_page) + "-" + str(slot) + ".save"
)

define SaveWithNameNotification = lambda slot: [
    FileSave(slot, confirm=False),
    get_save_notify_action(slot),
    Hide("screen_save_name")
]

define SaveWithNotification = lambda slot: [
    FileSave(slot, action=get_save_notify_action(slot))
]

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## Aptrug's code Start (first section)
            hbox:
                style_prefix "check"
                align (0.9, -0.15) #adjust this as required for positioning

                hbox:
                    if persistent.save_naming:
                        textbutton _("Description Enabled") action ToggleField(persistent,"save_naming")
                    else:
                        textbutton _("Description Disabled") action ToggleField(persistent,"save_naming")
            ## Aptrug's code End (first section)

            ## This ensures the input will get the enter event before any of
            ## the buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            # button:
            #     style "page_label"
            #
            #     key_events True
            #     xalign 0.5
            #     action page_name_value.Toggle()
            #
            #     input:
            #         style "page_label_text"
            #         value page_name_value
            hbox:
                align (0.2, -0.15) #adjust this as required for positioning
                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                # xalign 0.5
                # # change this to move file slots vertical location
                # yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        ## Aptrug's code Start (second section)
                        if renpy.current_screen().screen_name[0] == "load":
                            action FileLoad(slot)
                        else:
                            # selected (str(persistent._file_page) + "-" + str(slot) == renpy.newest_slot("[0-9]"))
                            # if persistent.save_naming:
                            #     action SetVariable("save_name", FileSaveName(slot)), Show("screen_save_name", slot=slot)
                            # else:
                            #     action SetVariable("save_name", FileSaveName(slot)), FileAction(slot)
                            if persistent.save_naming:
                                action SetVariable("save_name", FileSaveName(slot)), Show("screen_save_name", slot=slot)
                            else:
                                action SaveWithNotification(slot)

                        # if persistent.save_naming:
                        #    action [
                        #      Function(SetSaveName, slot),
                        #      If(renpy.get_screen("save"), true=Show("screen_save_name", accept=FileSave(slot)), false=FileLoad(slot))
                        #    ]
                        # else:
                        #    action [
                        #      Function(SetSaveName, slot),
                        #      FileAction(slot)
                        #     ]

                        vbox:
                            add FileScreenshot(slot) xalign 0.5
                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"

                            text FileSaveName(slot) or "":
                                style "slot_name_text"
                                xalign 0.5


                            # if FileLoadable(slot):
                            #     imagebutton:
                            #         idle "ui_elements/prefs/delete.webp"
                            #         action FileDelete(slot)
                            #         # xalign 0.5
                            #         # yoffset 10
                            #         xalign 1.04
                            #         yoffset -106


                            if FileLoadable(slot):
                                imagebutton:
                                    auto "ui_elements/prefs/delete_%s.webp"
                                    action FileDelete(slot)
                                    xalign 1.045
                                    yoffset -131

                            # if FileLoadable(slot):
                            #     textbutton _("{font=MaterialIcons-Regular.ttf}\ue92b{/font}"):
                            #         action FileDelete(slot)
                            #         text_style "save_delete_icon"
                            #         style "empty_button"
                            #         xalign 1.08
                            #         yoffset -120
                            #         # text_style "save_delete_icon"
                                # imagebutton:
                                #     auto "ui_elements/prefs/delete_%s.webp"
                                #     action FileDelete(slot)
                                #     xalign 1.0
                                #     yoffset -84
                        ## Aptrug's code End (second section)
                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 20):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()

                    # No more wheel scrolling
                    # key "save_page_prev" action FilePagePrevious()
                    # key "save_page_next" action FilePageNext()


## Aptrug's code Start (third section)
screen screen_save_name(slot):
    modal True
    # zorder 200
    style_prefix "confirm"
    add Solid("#000000") alpha 0.8

    # add "gui/overlay/confirm.png"

    frame:
        vbox:
            spacing 25
            xsize 650

            label _("Enter a description for your save file: ") style "confirm_prompt"
            # if FileLoadable(slot):
            #     label _("Save name ({color=#f00}overwrite{/color}):") style "confirm_prompt"
            # else:
            #     label _("Save name ({color=#00ff00}new{/color}):") style "confirm_prompt"

            input:
                value VariableInputValue('save_name')
                length 15
                xalign 0.5
                exclude "\\[{"

            hbox:
                xfill True
                # textbutton _("Yes") action FileAction(slot, confirm=False), Hide("screen_save_name") xalign 0.5
                textbutton _("Yes") action SaveWithNameNotification(slot) xalign 0.5
                textbutton _("No") action Hide("screen_save_name") xalign 0.5

    ## Right-click and escape answer "no".
    key "game_menu" action Hide("screen_save_name")

    ## Return of Enter answer "yes".
    # key "K_RETURN" action FileAction(slot, confirm=False), Hide("screen_save_name")
    # key "K_KP_ENTER" action FileAction(slot, confirm=False), Hide("screen_save_name")
    key "K_RETURN" action SaveWithNameNotification(slot)
    key "K_KP_ENTER" action SaveWithNameNotification(slot)

##############################################################################

screen language_picker():

    modal True
    frame:
        style "menu_frame"
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 15
            label _("Choose Language"):
                style "menu_label"

            grid 3 3 spacing 10:
                textbutton _("English") action [Language(None), Hide("language_picker")]
                textbutton _("Spanish") action [Language("spanish"), Hide("language_picker")]
                textbutton _("French") action [Language("french"), Hide("language_picker")]
                textbutton _("German") action [Language("german"), Hide("language_picker")]
                textbutton _("Italian") action [Language("italian"), Hide("language_picker")]
                textbutton _("Portuguese") action [Language("portuguese"), Hide("language_picker")]
                textbutton _("Russian") action [Language("russian"), Hide("language_picker")]
                textbutton _("Chinese") action [Language("chinese"), Hide("language_picker")]
                textbutton _("Japanese") action [Language("japanese"), Hide("language_picker")]

            textbutton _("Cancel") action Hide("language_picker") xalign 0.5

screen preferences():
    tag menu
    default pref_page = "options"

    use game_menu(_("Preferences"), scroll="viewport"):

        if pref_page == "options":
            vbox:
                # Top row - Special menu buttons
                hbox:
                    spacing 100
                    vbox:
                        button:
                            action ShowMenu("_accessibility")
                            hbox:
                                spacing 20
                                imagebutton:
                                    idle "ui_elements/prefs/accessibility.webp"
                                    yalign 0.5
                                text _("Accessibility Menu"):
                                    yalign 0.5
                                    size 50
                                    idle_color gui.idle_small_color
                                    hover_color '#cccc00'
                    vbox:
                        button:
                            action Show("language_picker")
                            hbox:
                                spacing 20
                                imagebutton:
                                    idle "ui_elements/prefs/language.webp"
                                    yalign 0.5
                                text _("Language"):
                                    yalign 0.5
                                    size 50
                                    idle_color gui.idle_small_color
                                    hover_color '#cccc00'

                # Main options grid
                hbox:
                    spacing 50
                    # Display settings
                    if renpy.variant("pc") or renpy.variant("web"):
                        vbox:
                            style_prefix "radio"
                            label _("Display")
                            textbutton _("Window") action Preference("display", "window")
                            textbutton _("Fullscreen") action Preference("display", "fullscreen")
                    else:
                        vbox:
                            style_prefix "radio"
                            label _("Video HWA")
                            textbutton _("Enable") action SetVariable("config.hw_video", True)
                            textbutton _("Disable") action SetVariable("config.hw_video", False)
                            textbutton _("Automatic") action SetVariable("config.hw_video", "auto")

                    # Skip settings
                    vbox:
                        style_prefix "check"
                        label _("Skip")
                        textbutton _("Unseen Text") action Preference("skip", "toggle")
                        textbutton _("After Choices") action Preference("after choices", "toggle")
                        textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                    # Quick Menu settings
                    vbox:
                        style_prefix "check"
                        label _("Quick Menu")
                        textbutton _("Enable") action ToggleField(persistent, "quickmenu")
                        textbutton _("Iconic") action ToggleField(persistent, "iconic_quickmenu")

                # Second row
                hbox:
                    spacing 50
                    # Rollback settings
                    vbox:
                        style_prefix "radio"
                        label _("Rollback Side")
                        textbutton _("Disable") action Preference("rollback side", "disable")
                        textbutton _("Left") action Preference("rollback side", "left")
                        textbutton _("Right") action Preference("rollback side", "right")

                    # PowerSave settings
                    vbox:
                        style_prefix "radio"
                        label _("PowerSave")
                        textbutton _("Enable") action Preference("gl powersave", True)
                        textbutton _("Disable") action Preference("gl powersave", False)
                        textbutton _("Automatic") action Preference("gl powersave", "auto")

        elif pref_page == "sliders":
            vbox:
                hbox:
                    # Don't need this I think
                    # spacing 50
                    style_prefix "slider"
                    vbox:
                        label _("Music Volume (%d%%)") % (preferences.get_volume('music') * 100)
                        bar value Preference("music volume")

                        label _("Sound Volume (%d%%)") % (preferences.get_volume('sfx') * 100)
                        bar value Preference("sound volume")

                        label _("Main Volume (%d%%)") % (preferences.get_volume('main') * 100)
                        bar value Preference("main volume")

                        label _("Dialogue Box Opacity (%d%%)") % (persistent.dialogue_box_opacity * 100)
                        bar value FieldValue(persistent, "dialogue_box_opacity", range=1.0, style="slider")
                    vbox:
                        label _("Text Speed (%s)") % (_("instantaneous") if int(preferences.text_cps) == 0 else "%d cps" % int(preferences.text_cps))
                        bar value Preference("text speed")

                        label _("Auto-Forward Time (%d/30 cps)") % preferences.afm_time
                        bar value Preference("auto-forward time")

                        label _("Text Outline (%d/6)") % persistent.text_outline_size
                        bar value FieldValue(persistent, "text_outline_size", range=6, style="slider")


                        label _("Menu Opacity (%d%%)") % (persistent.game_menu_opacity * 100)
                        bar value FieldValue(persistent,
                                             "game_menu_opacity",
                                             style="slider", range=1.0)

    # Navigation buttons at bottom center
    hbox:
        style_prefix "pref_nav"
        xalign 0.5
        yalign 1.0
        yoffset -80
        spacing 100

        textbutton _("Options"):
            action SetScreenVariable("pref_page", "options")
            text_size 35
            if pref_page == "options":
                text_color gui.accent_color
            else:
                text_color gui.idle_color
                text_hover_color gui.accent_color

        textbutton _("Sliders"):
            action SetScreenVariable("pref_page", "sliders")
            text_size 35
            if pref_page == "sliders":
                text_color gui.accent_color
            else:
                text_color gui.idle_color
                text_hover_color gui.accent_color

    # Restore Defaults button
    hbox:
        align (0.90, 0.98)
        textbutton _("Restore\nDefaults"):
            action Show("confirm",
                message=_("Are you sure you want to restore all settings to their default values?"),
                yes_action=[
                    Preference("rollback side", "disable"),
                    Preference("main volume", 1.0),
                    Preference("music volume", 1.0),
                    Preference("sound volume", 1.0),
                    Preference("voice volume", 1.0),
                    Preference("all mute", "disable"),
                    Preference("skip", "seen"),
                    Preference("after choices", "stop"),
                    Preference("transitions", "all"),
                    Preference("text speed", 0),
                    Preference("auto-forward time", 15),
                    SetVariable("quickmenu", True),
                    SetVariable("config.hw_video", False),
                    Preference("gl powersave", True),
                    SetVariable("persistent.text_outline_size", 3),
                    SetVariable("persistent.game_menu_opacity", 0.75),
                    SetVariable("persistent.dialogue_box_opacity", 0.0),
                    SetVariable("persistent.iconic_quickmenu", False),
                    Preference("font transform", None),
                    Preference("high contrast text", "disable"),
                    Preference("self voicing", "disable"),
                    Preference("self voicing volume drop", 0.5),
                    Preference("mono audio", "disable"),
                    Preference("font size", 1.0),
                    Preference("font line spacing", 1.0),
                    Preference("font kerning", 0.0),
                    Hide("confirm")
                ],
                no_action=Hide("confirm")
            )
            text_color gui.idle_color
            text_hover_color gui.accent_color
            text_size 30

style pref_nav_button is navigation_button:
    xsize 200
    ysize 50

style pref_nav_button_text is navigation_button_text:
    size 30

##############################################################################
screen notify(message):
    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 1.25 action Hide('notify')

##############################################################################

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    # if main_menu:
    #     add gui.main_menu_background
    # else:
    #     add gui.game_menu_background

    if main_menu:
        add "deutsches_reich.webp"

    add Solid("#000000") alpha persistent.game_menu_opacity

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")
