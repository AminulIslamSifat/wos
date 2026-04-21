import time
from core.recalibrate import recalibrate

from core.core import (
    req_ocr,
    req_text,
    tap_on_text,
    req_temp_match,
    tap_on_template,
    tap_on_templates_batch
)
from cmd_program.screen_action import(
    tap_screen,
    swipe_screen,
    input_text
)




def collect_mail_rewards():
    title = req_text("Home.Alliance.Title")
    try:
        title = title[0].lower()
    except Exception as e:
        print(f"Title Reading Error, Ignoring the read...")
    if title != "mail":
        recalibrate()
        tap_on_template("Home.Mail", sleep=1)
    
    tap_on_text("Home.Mail.System", sleep=1)
    tap_on_text("Home.Mail.ReadAndClaim", sleep=1)
    tap_on_text("Home.Mail.Reports", sleep=1)
    tap_on_text("Home.Mail.ReadAndClaim", sleep=1)
    tap_on_text("Home.Mail.Alliance", sleep=1)
    tap_on_text("Home.Mail.ReadAndClaim", sleep=1)
    return True


