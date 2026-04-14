import time
import requests
from cmd_program.screen_action import tap_screen

ocr_url = "http://127.0.0.1:8000/ocr"
template_matching_url = "http://127.0.0.1:8000/template"




def create_box(coord, radius):
    #This function will create searching region around an icon or text region to get better result
    if len(coord)==2:
        x1, y1, x2, y2 = (coord[0] - radius, coord[1]-radius, coord[0]+radius, coord[1]+radius)
        return [x1, y1, x2, y2]
    elif len(coord) == 4:
        x1, y1, x2, y2 = (coord[0] - radius, coord[1]-radius, coord[2]+radius, coord[3]+radius)
        return [x1, y1, x2, y2]
    else:
        raise RuntimeError("Wrong format in coordination")






def req_ocr(img_path=None, save_result=None, rois=None):
    payload = {
        "img_path": img_path,
        "save_result" : save_result,
        "rois": rois
    }

    response = requests.post(ocr_url, json=payload)
    data = response.json()

    if data["success"] != True:
        return None
    
    result = data["results"]
    return result



def req_temp_match(name, threshold=None, save_result=None):
    payload = {
        "name" : name,
        "threshold" : threshold,
        "save_result": save_result
    }

    response = requests.post(template_matching_url, json=payload)
    data = response.json()

    if data["success"] != True:
        return None
    
    results = data["results"]
    result = (results["x"], results["y"])
    return result



def tap_on_template(name, threshold=None, save_result=None, wait=None):
    if wait:
        t1 = time.time()
        t2 = time.time()
        while (t2-t1)<wait:
            coord = req_temp_match(name, threshold, save_result)
            if coord:
                tap_screen(coord)
                return True
            t2 = time.time()
            print(t2-t1)
        
        return None
    
    
    for i in range(3):
        coord = req_temp_match(name, threshold, save_result)
        if coord:
            tap_screen(coord)
            return True

    return None


