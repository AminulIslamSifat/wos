import time
import requests
from core.core import req_ocr, tap_on_template, tap_on_text, tap_on_templates_batch
from cmd_program.screen_action import tap_screen



def recalibrate():
    rois = [917, 2402, 1030, 2442]
    is_home = False

    while(not is_home):
        found = False
        loc_data = req_ocr(rois=[rois])

        for data in loc_data:
            text = data["text"].lower()
            if text == "world":
                is_home = True
                break
            elif text == "city":
                box = data["box"]
                coord = ((box[0]+box[2])//2, (box[1]+box[3])//2)
                tap_screen(coord)
                is_home = True
                time.sleep(2)
                break
            
        if is_home:
            print("On homepage")
            time.sleep(1)
            break

        # found = tap_on_templates_batch(
        #     ["Global.Back", "Global.Close", "FirstPurchase.Close"],
        #     sleep = 1
        # )

        found = tap_on_template("Global.Back", sleep=1)
        if not found:
            found = tap_on_template("Global.Close", sleep=1)
        if not found:
            found = tap_on_template("FirstPurchase.Close", sleep=1)
        if not found:
            found = tap_on_text("Tap anywhere to exit", sleep=1)


    

#recalibrate()