#coming soon
import time
from core.core import (
    tap_on_template,
    tap_on_text
)
from cmd_program.screen_action import(
    tap_screen,
    swipe_screen
)
from core.recalibrate import recalibrate









def change_account(current_account, next_account):
    recalibrate()
    time.sleep(2)
    tap_screen(100, 170)
    tap_on_text("ChiefProfile.Settings",sleep=1)
    tap_on_text("ChiefProfile.Settings.Account", sleep=1)
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount", sleep=1) 



change_account(1,2)
#tap_screen(100, 170)
