import time
import requests
from core.core import req_ocr, tap_on_template, tap_on_text, tap_on_templates_batch, req_text
from cmd_program.screen_action import tap_screen



def recalibrate():
    is_home = False
    retry = 0
    
    while(not is_home) and retry<7:
        retry += 1
        found = False
        text = req_text("Home.World")

        try:
            text = text[0][0].lower()
        except Exception as e:
            print("Finding The Homepage...")

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
            [
                "Global.Back",
                "Global.Close", 
                "FirstPurchase.Close",
                
            ],
            sleep = 1,
            parallel = True
        )
        # found = tap_on_template("Global.Back", sleep=1)
        # if not found:
        #     found = tap_on_template("Global.Close", sleep=1)
        # if not found:
        #     found = tap_on_template("FirstPurchase.Close", sleep=1)

        rois = [[0, 1900, 1080, 2460]]
        if not found:
            found = tap_on_text("Tap anywhere to exit", rois=rois, sleep=1)
        if not found:
            found = tap_on_text("Click to continue", rois=rois, sleep=1)
        if not found:
            text = req_text("Home.World")
            try:
                text = text[0][0]
            except Exception as e:
                print(f"Error... {e}")
            if text:
                found = True
                if text.lower() != "city" and text.lower() != "world":
                    tap_screen(540, 1230)
            else:
                found = False

        if not found:
            tap_screen(70, 170)
            time.sleep(1)
    if not is_home:
        raise RuntimeError("Homepage Not found, Runtime Error. Stopping the Bot...")

