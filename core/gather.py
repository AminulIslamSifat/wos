from core.core import (
    req_ocr,
    req_temp_match,
    tap_on_template,
    tap_on_templates_batch,
    tap_on_text
)
import time
from core.recalibrate import recalibrate
from cmd_program.screen_action import swipe_screen, tap_screen



def gather():
    search_box = [[0, 1830, 1080,2030]]
    gathering_nodes = ["meat", "wood", "coal", "iron"]
    recalibrate()
    tap_on_text("world", sleep=2)
    
    
    for node in gathering_nodes:
        tap_on_template("search", sleep=1)
        found = tap_on_text(node, rois=search_box, sleep=1)
        if found is None:
            swipe_screen(1000, 1920, 0, 1920)
        found = tap_on_text(node, rois=search_box, sleep=1)
        
        #from here its needs to be optimized
        tap_on_text("search", sleep=3)
        tap_on_text("gather", sleep=1)
        tap_screen(357, 593) #removing hero
        tap_on_text("deploy", sleep=1)



gather()