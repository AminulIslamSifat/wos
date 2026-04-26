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


side_panel = [0, 690, 670, 1650]


def collect_missions_reward():
    recalibrate()
    tap_on_template("Home.Missions", sleep=1)
    status = tap_on_text("Home.Missions.GrowthMissions", sleep=1)
    while status:
        status = tap_on_text("Home.Missions.GrowthMissions.Claim", sleep=1)
    tap_on_text("Home.Missions.DailyMissions", sleep=1)
    tap_on_text("Home.Missions.DailyMissions.ClaimAll", sleep=1)
    tap_on_text("Home.Missions.TapAnywhereToExit", sleep=1)



def collect_life_essence():
    recalibrate()
    tap_on_template("Global.SidePanel", sleep=1)
    for i in range(2):
        swipe_screen(350, 1600, 350, 800)
        time.sleep(0.3)
    tap_on_text("Tree of Life", rois=[side_panel], sleep=4)
    tap_screen(550, 1240)           #to remove instructor hand
    time.sleep(0.3)
    for i in range(2):
        swipe_screen(110, 950, 940, 1450, duration=750)
        time.sleep(0.3)
        status = tap_on_template("Global.Island.TimberMill.EssenceOfLife", sleep=1)
        if status:
            break
    



def collect_from_events():
    box = [60, 355, 1050, 400]
    recalibrate()
    tap_on_template("Home.Store", sleep=1)
    
    status = True
    while(status):
        status = tap_on_text("claimable", rois=[[0, 0, 1080, 1080]], sleep=1, align=[0, -50])
        if not status:
            status = tap_on_text("free", rois = [0, 0, 1080, 1080], sleep=1)
            if status:
                tap_on_text("Tap anywhere to exit", sleep=1, align=[0, 50])
        if status:
            tap_on_template("Global.Back", threshold=0.6, sleep=1)
            tap_on_template("Home.Store", sleep=1)
        else:
            tap_on_template("Global.Back", threshold=0.6, sleep=1)
    



