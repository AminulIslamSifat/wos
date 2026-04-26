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
    swipe_screen
)







def tech_contribution():
    title = req_text("Home.Alliance.Title")
    try:
        title = title[0][0].lower()
    except Exception as e:
        print(f"Title Reading Error, Ignoring the read...")
    if title != "alliance":
        recalibrate()
        tap_on_text("Home.Alliance", sleep=1)
    tap_on_text("Home.Alliance.Tech", sleep=1)
    tap_on_template("Home.Alliance.Tech.Recommended", sleep=1)
    tap_on_text("Home.Alliance.Tech.Contribute.FreeContribute", hold=7000, sleep=1)
    tap_on_template("Global.Close", sleep=1)
    tap_on_template("Global.Back", sleep=1)
    return True

def auto_join():
    title = req_text("Home.Alliance.Title")
    try:
        title = title[0][0].lower()
    except Exception as e:
        print(f"Title Reading Error, Ignoring the read...")
    if title != "alliance":
        recalibrate()
        tap_on_text("Home.Alliance", sleep=1)
    tap_on_text("Home.Alliance.War", sleep=1)
    status = tap_on_text("Home.Alliance.War.AutoJoin", sleep=1)
    if not status:
        tap_on_text("Home.Alliance.War.AutoJoining", sleep=1)
    status = tap_on_text("Home.Alliance.War.AutoJoin.Enable", sleep=1)
    if not status:
        tap_on_text("Home.Alliance.War.AutoJoin.Restart", sleep=1)
    tap_on_template("Global.Close", sleep=1)
    tap_on_template("Global.Back", sleep=1)
    return True

def collect_chests():
    title = req_text("Home.Alliance.Title")
    try:
        title = title[0][0].lower()
    except Exception as e:
        print(f"Title Reading Error, Ignoring the read...")
    if title != "alliance":
        recalibrate()
        tap_on_text("Home.Alliance", sleep=1)
    tap_on_text("Home.Alliance.Chests", sleep=1)
    tap_on_text("Home.Alliance.Chests.LootChest",sleep=1)
    status = tap_on_text("Home.Alliance.Chests.LootChest.ClaimAll", sleep=1)
    if status:
        tap_on_text("Home.Alliance.Chests.LootChest.ClaimAll.TapAnywhereToExit", sleep=1)
    tap_on_template("Global.Back", sleep=1)
    return True

def help():
    title = req_text("Home.Alliance.Title")
    try:
        title = title[0][0].lower()
    except Exception as e:
        print(f"Title Reading Error, Ignoring the read...")
    if title != "alliance":
        recalibrate()
        tap_on_text("Home.Alliance", sleep=1)
    tap_on_text("Home.Alliance.Help", sleep=1)
    tap_on_text("Home.Alliance.Help.HelpAll", sleep=1)
    tap_on_template("Global.Back", sleep=1)
    return True

def shop():
    return




