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

def collect_ally_treasure():
    recalibrate()
    tap_on_template("Home.Pet", sleep=1)
    tap_on_template("Home.Pet.BeastCage", sleep=1)
    tap_on_template("Home.Pet.BeastCage.Adventure", sleep=1)
    tap_on_template("Home.Pet.BeastCage.Adventure.AllyTreasure", sleep=1)
    tap_on_template("Home.Pet.BeastCage.Adventure.AllyTreasure.ClaimAll", sleep=1)
    tap_on_text("Tap anywhere to exit", sleep=1)
    return True

def start_pet_exploration():
    recalibrate()
    tap_on_template("Home.Pet", sleep=1)
    tap_on_template("Home.Pet.BeastCage", sleep=1)
    tap_on_template("Home.Pet.BeastCage.Adventure", sleep=1)
    #some more logic
    return True

def activate_reward_pet_skill():
    return

def activate_war_pet_skill():
    return