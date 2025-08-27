# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

# define e = Character("Eileen")

# define mc = Character("[mc_name]", image="rance", color="#c6f53b", xpos=0)
# define mc = Character("[mc_name]", image="rance", color="#c6f53b",
#     show_transform=Transform(fit="contain", size=(1280, 720)))
# default persistent.naming_toggle = True

# image my_bg = im.Scale("bg.png", 1920, 1080)
# image my_bg = "maison_1920x1080.jpg"
# image mr_rance = im.FactorScale("rance.webp", 2)

# The game starts here.

# define left = Position(xpos=0.1, xanchor=0.0)

label start:
    scene maison_1920x1080 with fade

    "HAHAHAHAHAHA!"
    "CHAAAAAAARGE!"

    # show screen battle_ui
    with flash_white

    "URAAAAAAA!"

    "HAHAHAHAHA!"

    scene swamp with flash_black

    "Good!"

    return

    play music "music/rancex.opus" volume 0.8
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    show expression im.Blur("maison_1920x1080.webp", 1.5)

    $mc_name = renpy.input("Enter your name (max 16 characters):",
                       length = 16).strip() or "Rance"

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    # show rance neutral at left

    mc "Hey!"

    # $renpy.notify("Hello!")

    scene maison_1920x1080 with fade

    show rance neutral with dissolve

    mc "Greetings!"

    mc "Oh!"

    mc bored "You again? This game will never be finished at this rate."

    play sound "sounds/punch.opus"

    mc angry "Unacceptable!" with vpunch

    mc angry "What do you mean you need \"more time\"!" with vpunch

    mc "Be faster!"

    # I don't like the syntax of my custom menu
    menu:
        "Tell me, are you an idiot?"
        "Yes." if mc_name != "Rance"\
            "{i}(Nah, you're cool){/i}":
            mc "I thought so."
        "Maybe." if mc_name == "Vance":
            mc "I thought so."
        "No.":
            mc "Yes, you are!"

    mc bored "Wait, I feel something..."

    scene forest with flash_white
    "One"
    scene swamp with flash_black
    "Two"

    show rance startled with move

    play sound "sounds/teleport.opus"

    mc startled "Eeh!"

    mc "Who changed the scenery?"

    mc neutral "Anyway."

    mc "Doesn't matter."

    mc smiling "At least it runs without errors this time."

    mc "That's an improvement."

    mc "Keep at it."

    mc "And remember."

    mc @ laughing "I am the greatest in the world!"

    mc "Later."

    mc scheming "I must return to Sill."

    menu first_choices:
        set menuset
        "What to press?"

        "One.":
            pass
        "Two.":
            pass

    # For resetting
    # $menuset = set()

    menu second_choices:
        set menuset

        "One.":
            "Already went."
        "Two.":
            "Already went."
        "I'm a coward." if mc_name != "Rance"\
            "(You can't be a coward, you're Rance dammit)":
            "New option."
        "Hello there, how are you doing? Great weather we're having eh. Have a Totally Joyful Day.":
            jump second_choices

    return
