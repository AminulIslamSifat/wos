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



def claim_exploration_idle_income():
    status = tap_on_text("Home.Exploration")
    if not status:
        recalibrate()
        tap_on_text("Home.Exploration")

    tap_on_text("Home.Exploration.Claim")
    status = tap_on_text("Home.Exploration.Claim.Claim")
    if status:
        tap_on_text("Home.Exploration.Claim.Claim.TapAnywhereToExit")

    recalibrate()


    



def continue_exploring(stopping_level=None):
    print("Started Exploration...")

    def ensure_open_exploration():
        status = tap_on_text("Home.Exploration")
        if not status:
            recalibrate()
            tap_on_text("Home.Exploration", sleep=1)

    
    def setup_exploration():
        tap_on_text("Home.Exploration.Explore", sleep=1)
        tap_on_text("Home.Exploration.Explore.QuickDeploy")

    # --- start ---
    ensure_open_exploration()
    setup_exploration()


    is_auto = True

    while True:
        if stopping_level:
            try:
                level = int(req_text("Home.Exploration.CurrentLevel")[0][0])
            except Exception as e:
                print(f"Level Reading Failed - {e}, Ending the task...")
                recalibrate()
                return

            print(f"Current level - {level}, Will stop at {stopping_level}")
            if level > stopping_level:
                print("Exploration Completed...")
                recalibrate()
                break

        tap_on_text("Home.Exploration.Explore.Fight", sleep=1)

        s = tap_on_text("Home.Exploration.Explore.Fight.ReturnToCity", wait=30, tap=False)
        if s:
            v = tap_on_text("Home.Exploration.Explore.Fight.Victory.Continue", sleep=1)
            if v:
                print("Challenging next stage...")
            else:
                v = tap_on_text("Home.Exploration.Explore.Fight.ReturnToCity", sleep=3)
                print("Failed the stage, Returning to the Homepage")
                recalibrate()
                break



