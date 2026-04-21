import time
import requests
from core.core import req_ocr, tap_on_template, tap_on_text, tap_on_templates_batch, req_text
from cmd_program.screen_action import tap_screen



def recalibrate():
    rois = [917, 2402, 1030, 2442]
    is_home = False

    while(not is_home):
        found = False
        text = req_text("Home.World")

        try:
            text = text[0].lower()
        except Exception as e:
            print(f"No text found. Error - {e}")

        if text == "world":
            is_home = True
        elif text == "city":
            tap_on_text("World.City", sleep=2)
            is_home = True
            
        if is_home:
            print("On homepage")
            time.sleep(1)
            break

        found = tap_on_templates_batch(
            ["Global.Back", "Global.Close", "FirstPurchase.Close"]
        )
        if any(found):
            found = True

        # found = tap_on_template("Global.Back", sleep=1)
        # if not found:
        #     found = tap_on_template("Global.Close", sleep=1)
        # if not found:
        #     found = tap_on_template("FirstPurchase.Close", sleep=1)
        if not found:
            found = tap_on_text("Tap anywhere to exit", sleep=1)
        if not found:
            found = tap_on_text("Tap to continue", sleep=1)
        if not found:
            text = req_text("Home.World")
            try:
                text = text[0]
            except Exception as e:
                print(f"Error... {e}")
            if text.lower() != "city" or text.lower() != "world":
                tap_screen(540, 1230)


    

recalibrate()