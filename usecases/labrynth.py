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



def labrynth():
    recalibrate()
    tap_on_template("Home.Labrynth", sleep=1)
    status = tap_on_template("Home.Labrynth.Available", sleep=1)
    while status:
        tap_on_text("Home.Labrynth.Raid.Claim", sleep=1)
        tap_on_text("Home.Labrynth.Raid", sleep=1)

    return True