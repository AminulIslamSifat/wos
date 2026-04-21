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




def collect_vip_rewards():
    title = req_text("Home.VIP.Title")
    try:
        title = title[0]
    except Exception as e:
        print(f"Error while reading page title - {e}, Continuing...")
    
    if title.lower() != "vip":
        recalibrate()
        tap_on_text("Home.VIPLevel", sleep=1)

    tap_on_template("Home.VIP.CollectChest", sleep=1)
    tap_on_text("Home.VIP.CollectChest.ClickToContinue", sleep=1)
    tap_on_text("Home.VIP.Claim",sleep=1)
    tap_on_text("Home.VIP.Claim.TapAnywhereToExit", sleep=1)
    recalibrate()
    return True

    

def buy_vip_time(day=30):
    title = req_text("Home.VIP.Title")
    try:
        title = title[0]
    except Exception as e:
        print(f"Error while reading page title - {e}, Continuing...")
    
    if title.lower != "vip":
        recalibrate()
        tap_on_text("Home.VIPLevel", sleep=1)

    
