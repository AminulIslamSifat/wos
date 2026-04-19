import time
import json

from core.recalibrate import(
    recalibrate
)
from cmd_program.screen_action import(
    tap_screen
)
from core.core import(
    req_ocr,
    req_temp_match,
    tap_on_template,
    tap_on_text
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
            texts = req_ocr(rois=[[480, 270, 600, 400]])
            texts = [t["text"] for t in texts if t["score"] > 0.9]
            level = int(texts[0])
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

