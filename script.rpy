
# Label to demonstrate the UI
label start:
    # Show the round UI screen
    show screen round_ui

    "This is the round UI display. Round: [current_round], AP: [available_ap]/[max_ap]"

    menu:
        "Spend 1 AP":
            $ spend_ap(1)
            "AP spent! Now you have [available_ap]/[max_ap] AP remaining."

        "Gain 1 AP":
            $ gain_ap(1)
            "AP gained! Now you have [available_ap]/[max_ap] AP."

        "Next Round":
            $ update_round(current_round + 1)
            $ available_ap = max_ap  # Refresh AP for new round
            "Welcome to round [current_round]! AP refreshed to [available_ap]/[max_ap]."

        "Change AP Settings":
            menu:
                "Set Max AP to 6":
                    $ update_ap(min(available_ap, 6), 6)
                    "Max AP changed to 6. Current AP: [available_ap]/[max_ap]"

                "Set Max AP to 12":
                    $ update_ap(available_ap, 12)
                    "Max AP changed to 12. Current AP: [available_ap]/[max_ap]"

                "Reset to Default (9)":
                    $ update_ap(min(available_ap, 9), 9)
                    "Reset to default settings. AP: [available_ap]/[max_ap]"

    jump start
