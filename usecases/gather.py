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




def wait_till_return(lowest_time=14400):
    recalling = recall_current_gathering(lowest_time=lowest_time)
    while(recalling):
        return_times = req_text(
                [
                "World.FirstMarchTime",
                "World.SecondMarchTime",
                "World.ThirdMarchTime", 
                "World.FourthMarchTime", 
                "World.FifthMarchTime"
            ]
        )
        times = []
        for i, return_time in enumerate(return_times):
            try:
                return_time = return_time[0].split(':')
                return_time = [int(t) for t in return_time]
                return_time = return_time[0]*3600 + return_time[1]*60 + return_time[2]
                times.append(return_time)
            except Exception as e:
                print(f"Couldn't read the time properly - {e}")

        if len(times) <= 1:
            break

        waiting_time = max(times) if len(times)>0 else 0
        if waiting_time > 600:
            recalling = recall_current_gathering(lowest_time=lowest_time)
        elif waiting_time == 0:
            recalling = False
            break
        print(f"Waiting for {waiting_time} seconds for the troops to return home...")
        time.sleep(waiting_time)



def gather(remove_hero=False, equalize=True, lowest_time=14400):
    print("Started Gathering...")
    search_box = [[0, 1940, 1080,1980]]
    gathering_nodes = ["meat", "wood", "coal", "iron", "coal"]

    title = req_text("World.City")
    try:
        title = title[0][0].lower()
    except Exception as e:
        print(f"Reading Error - {e}")
    if title != "city":
        recalibrate()
        tap_on_text("Home.World", sleep=2)

    wait_till_return(lowest_time=lowest_time)

    try:
        data = req_text('World.MarchQueue')[0][0].split('/')
        remaining_march = int(data[1]) - int(data[0])
        occupied_march = int(data[0])
    except Exception as e:
        print(f"Reading Error - {e}")
        remaining_march = 4
        occupied_march = 0
    i = 0
    
    while remaining_march>0 and occupied_march < 5:
        print(f"Remaining march queue: {remaining_march} ----- Occupied March: {occupied_march}")
        status = tap_on_template("World.Search", sleep=1, threshold=0.6)
        if not status:
            print("Seach Icon not found, Exiting the task...")
            return
        found = tap_on_text(gathering_nodes[i], rois=search_box, sleep=1)
        if found is None:
            swipe_screen(1000, 1920, 0, 1920)
            time.sleep(1)
            tap_on_text(gathering_nodes[i], rois=search_box, sleep=1)
        
        level = req_text("World.Search.ItemLevel")
        try:
            level = level[0][0]
            if level != "8":
                tap_screen(910, 2120)
                time.sleep(1)
                input_text("8")
        except Exception as e:
            print(f"Level reading Error, Continuing without reading the level...")

        #from here its needs to be optimized
        status = tap_on_text("World.Search.Search", sleep=3)
        if status:
            status = tap_on_text("World.Search.Gather", sleep=1)
        if not status:
            print("Gather button is not found, Exiting the task...")
            return
        if remove_hero:
            tap_on_template("World.Deploy.RemoveHero", threshold=0.6, rois=[[300, 500, 400, 650]]) #removing hero
        if equalize:
            tap_on_text("World.Deploy.Equalize", sleep=2)
        tap_on_text("World.Deploy.Deploy", sleep=1)

        i = i+1

        try:
            data = req_text('World.MarchQueue')[0][0].split('/')
            remaining_march = int(data[1]) - int(data[0])
            occupied_march = int(data[0])
        except Exception as e:
            print(f"Reading Error - {e}")
            remaining_march = remaining_march - 1
    
    text = req_text("World.City")
    try:
        text = text[0][0]
    except Exception as e:
        print("The search tab may still opened, Trying to recover...")
    if text.lower() != "city":
        tap_screen(540, 1230)
    print("Completed the gathering task, Returning to homepage...")
    recalibrate()




def recall_current_gathering(lowest_time=14400):
    title = req_text("World.City")
    recalling = False
    try:
        title = title[0][0].lower()
    except Exception as e:
        print(f"Reading Error - {e}")
    if title != "city":
        recalibrate()
        tap_on_text("Home.World", sleep=2)
    
    time = req_text("World.FirstMarchTime")
    try:
        time = time[0][0].split(':')
        time = [int(t) for t in time]
        time = time[0]*3600 + time[1]*60 + time[2]
    except Exception as e:
        print(f"Couldn't read the time properly - {e}")
    
    if not isinstance(time, int) or time < lowest_time:
        found = tap_on_template("World.Recall", threshold=0.9, sleep=1)
        recalling = True
        while found:
            tap_on_text("World.Recall.Confirm", sleep=1)
            found = tap_on_template("World.Recall", threshold = 0.9, sleep=1)
    
    return recalling
            