#coming soon
import time
from core.core import (
    tap_on_template,
    tap_on_text,
    req_text,
    tap_on_templates_batch
)
from cmd_program.screen_action import(
    tap_screen,
    swipe_screen
)
from core.recalibrate import recalibrate









def change_account(next_email):
    recalibrate()
    tap_screen(100, 170)
    time.sleep(2)
    tap_on_text("ChiefProfile.Settings",sleep=1)
    tap_on_text("ChiefProfile.Settings.Account", sleep=1)
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount", sleep=1)
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount.SignInWithGoogle", sleep=5)
    status = tap_on_text(next_email, sleep=5)
    if not status:
        swipe_screen(550, 1800, 550, 400)
        status = tap_on_text(next_email, sleep=6)
        if not status:
            print("Email not found, Exiting...")
            return None
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount.SignInWithGoogle.Continue", sleep=10)
    recalibrate()
    return True




def change_character(next_name):
    recalibrate()
    tap_screen(100, 170)
    time.sleep(2)
    text = req_text("ChiefProfile.Title")[0]
    if text.lower() != "chief profile":
        print("Chief Profile not found, Exiting...")
        return None
    tap_on_text("ChiefProfile.Settings",sleep=1)
    tap_on_text("ChiefProfile.Settings.Characters", sleep=1)
    players = req_text(
        ["ChiefProfile.Settings.Characters.FirstCharacterName",
        "ChiefProfile.Settings.Characters.SecondCharacterName"]
    )
    names = [player.split(']')[1].lower() for player in players]
    if next_name.lower() not in names:
        print("Character not found, Exiting...")
        return None
    index = names.index(next_name.lower())
    status = tap_on_text(players[index], rois=[0, 1000, 1080, 1450])
    
    if not status:
        print("Finding player failed")
        return None

    tap_on_text("ChiefProfile.Settings.Characters.Login.Confirm")
    time.sleep(10)
    recalibrate()
    return True




