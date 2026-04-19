import requests
from core.core import req_ocr, tap_on_template, tap_on_text
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
                break
            
        if is_home:
            print("On homepage")
            break
        
        found = tap_on_template("Global.Back")
        if found:
            continue
        if not found:
            found = tap_on_template("Global.Close")
        if not found:
            found = tap_on_text("Tap anywhere to exit")
        if not found:
            tap_screen(540, 1900)


    

#recalibrate()