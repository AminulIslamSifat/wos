import requests
from core.core import req_ocr, req_temp_match, create_box
from cmd_program.screen_action import tap_screen



def recalibrate():
    rois = create_box([917, 2402, 1030, 2442], 100)
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
        
        back_button = "assets/global/back_button.jpg"
        close_button = "assets/global/close_button.jpg"

        loc_data = req_temp_match(back_button)
        if loc_data is not None:
            tap_screen(loc_data)
            found = True
        
        loc_data = req_temp_match(close_button)
        if loc_data is not None:
            tap_screen(loc_data)
            found = True

        if not found:
            tap_screen(540, 1900)


    

#recalibrate()