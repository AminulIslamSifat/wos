from core.core import req_ocr, req_temp_match, create_box, tap_on_template
from cmd_program.screen_action import tap_screen
from core.recalibrate import recalibrate
import json
import time


with open("config/ui_config.json") as file:
    ui_element = json.load(file)


def claim_exploration_idle_income():
    coord = req_temp_match("exploration")
    if coord is None:
        recalibrate()
    tap_on_template("exploration")
    tap_on_template("exploration_claim")
    coord = tap_on_template("exploration_final_claim")
    if not coord:
        recalibrate()
        return
    
    time.sleep(2)
    for i in range(2):
        tap_screen(540, 1750)

    recalibrate()


    



def continue_exploring(stopping_level=None):
    coord = tap_on_template("exploration")
    if not coord:
        recalibrate()
        tap_on_template("exploration")
    tap_on_template("exploration_explore")
    tap_on_template("exploration_quick_deploy")

    if not stopping_level:
        failed = False
        while not failed:
            tap_on_template("exploration_fight")
            found = tap_on_template("exploration_continue", wait=30)

            #here will be the logic for continuing exploration


            if not found:
                found = tap_on_template("exploration_return_to_city")
                if found:
                    failed = True
            if not found:
                failed = True
    
    else:
        #here will be the logic with a stopping level
        print("Coming soon")


t1 = time.time()
continue_exploring()
t2 = time.time()
print(t2 - t1)