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


def gather(remove_hero=False, equalize=True):
    print("Started Gathering...")
    search_box = [[0, 1940, 1080,1980]]
    gathering_nodes = ["meat", "wood", "coal", "iron", "coal"]

    recalibrate()
    time.sleep(2)

    tap_on_text("Home.World", sleep=2)

    try:
        data = req_text('World.MarchQueue')[0].split('/')
        remaining_march = int(data[1]) - int(data[0])
        occupied_march = int(data[0])
    except Exception as e:
        print(f"Reading Error - {e}")
        remaining_march = 4
        occupied_march = 0
    i = 0
    
    while remaining_march>0 and occupied_march < 5:
        print(f"Remaining march queue: {remaining_march} ----- Occupied March: {occupied_march}")
        tap_on_template("World.Search", sleep=1, threshold=0.6)
        found = tap_on_text(gathering_nodes[i], rois=search_box, sleep=1)
        if found is None:
            swipe_screen(1000, 1920, 0, 1920)
            time.sleep(1)
            tap_on_text(gathering_nodes[i], rois=search_box, sleep=1)
        
        level = req_text("World.Search.ItemLevel")
        try:
            level = level[0]
            if level != "8":
                tap_screen(910, 2120)
                time.sleep(1)
                input_text("8")
        except Exception as e:
            print(f"Level reading Error, Continuing without reading the level...")

        #from here its needs to be optimized
        tap_on_text("World.Search.Search", sleep=3)
        tap_on_text("World.Search.Gather", sleep=1)
        if remove_hero:
            tap_on_template("World.Deploy.RemoveHero", threshold=0.6, rois=[[300, 500, 400, 650]]) #removing hero
        if equalize:
            tap_on_text("World.Deploy.Equalize", sleep=2)
        tap_on_text("World.Deploy.Deploy", sleep=1)

        i = i+1

        try:
            data = req_text('World.MarchQueue')[0].split('/')
            remaining_march = int(data[1]) - int(data[0])
            occupied_march = int(data[0])
        except Exception as e:
            print(f"Reading Error - {e}")
            remaining_march = remaining_march - 1
    
    text = req_text("World.City")
    try:
        text = text[0]
    except Exception as e:
        print("The search tab may still opened, Trying to recover...")
    if text.lower() != "city":
        tap_screen(540, 1230)
    print("Completed the gathering task, Returning to homepage...")
    recalibrate()




def recall_current_gathering(lowest_time=240):
    return