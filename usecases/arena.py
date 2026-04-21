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




def arena():
    attempt = 0
    recalibrate()
    print("Starting the fight in Arena of Glory...")

    print("Swiping down the screen to find arena")
    for i in range(5):
        swipe_screen(1000, 1200, 100, 1200)
        time.sleep(0.3)
    for i in range(6):
        swipe_screen(540, 2000, 540, 1000)
        time.sleep(0.3)
    for i in range(2):
        swipe_screen(540, 1000, 450, 1900)
        time.sleep(0.3)

    time.sleep(2)
    available = tap_on_template("Home.Arena", threshold=0.6, sleep=1)
    if not available:
        print("Arena challenge is not availabe, Ending the task")
        return
    tap_on_text("Home.Arena.Challenge", sleep=1)

    res = req_ocr(rois=[[300, 1725, 665, 1830]])

    try:
        attempt = int(res[0]['text'].split(":")[1])
    except Exception as e:
        print(f"Attempt Reading error -{e}")

    while(attempt > 0):
        res = req_ocr(rois=[[300, 1725, 665, 1830]])
        try:
            attempt = int(res[0]['text'].split(":")[1])-1
            print(f"Remainng Challenge {attempt}")
        except Exception as e:
            print(f"Attempt counting error -{e}")

        tap_on_template("Home.Arena.Challenge.Challenge", sleep=1)
        tap_on_text("Home.Arena.Challenge.Challenge.QuickDeploy")
        tap_on_text("Home.Arena.Challenge.Challenge.Fight", sleep=4)
        tap_on_template("Home.Arena.Challenge.Challenge.Fight.Pause", sleep=1)
        tap_on_template("Home.Arena.Challenge.Challenge.Fight.Pause.Retreat")
        res = tap_on_text("Home.Arena.Challenge.Challenge.Fight.End.TapAnywhereToExit", wait=5, sleep=1)
        
    print("Finished the task - Arena Of Glory, Returning to homepage...")
    recalibrate()





arena()