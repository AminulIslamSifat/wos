import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import json
import time
import uvicorn
import numpy as np
from pathlib import Path
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from paddleocr import PaddleOCR
from concurrent.futures import ThreadPoolExecutor
from cmd_program.screen_action import take_screenshot
import paddleocr


import paddle
print(paddleocr.__version__)
print(paddle.__version__)




#------------------- Data Models ---------------------------------#

#input schema for fastapi
class OCRRequest(BaseModel):
    img_path: Optional[str] = None
    save_result: Optional[bool] = False
    rois: Optional[list[list[int]]] = None


class TemplateMatchRequest(BaseModel):
    name: str
    threshold: Optional[float] = None
    save_result: Optional[bool] = False


#------------------- Configuration ------------------------------#
SCREENSHOT_TTL = 0.1
CPU_THREADS = os.cpu_count() or 1
TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))


#---------------------- Globals ---------------------------------#
app = FastAPI()
_template_cache = {}


#----------------------- Functions -------------------------------#
def init_services():
    global ocr, _template_cache, ui_element
    #initializeng the ocr once for all
    # ocr = PaddleOCR(
    #         use_doc_orientation_classify=False,
    #         use_doc_unwarping=False,
    #         use_textline_orientation=False,
    #     )
    
    paddle.set_device("cpu")
    ocr = PaddleOCR(
        use_angle_cls=False,
        lang='en',
        use_gpu=False,
        det_limit_side_len=1024,
        cpu_threads=CPU_THREADS,
        ir_optim=True,
        layout=False,
        table=False,
        formula=False,
    )

    root_dir = Path(TEMPLATE_PATH)
    for file_path in root_dir.rglob("*.png | *.jpg"):
        if file_path.is_file:
            fn = os.path.splitext(file_path.name)[0]
            img = cv2.imread(file_path)
            if img is not None:
                _template_cache[fn] = img
    


def clamp_roi(roi, width, height):
    x1, y1, x2, y2 = roi

    # clamp values inside image bounds
    x1 = max(0, min(x1, width - 1))
    y1 = max(0, min(y1, height - 1))
    x2 = max(0, min(x2, width))
    y2 = max(0, min(y2, height))

    # ensure valid rectangle
    if x2 <= x1 or y2 <= y1:
        return None

    return [x1, y1, x2, y2]


def match_template(name, threshold=None, save_result=None, get_all=False):
    #checking if the element data exist or not
    if name not in ui_element:
        template = cv2.imread(name)
    else:
        temp = ui_element[name]
        template = cv2.imread(temp["image"])
        if threshold == None:
            threshold  = temp["threshold"]
        
    if threshold is None:
        threshold = 0.8
        
    #loading threshold if not passed
    try:
        img = take_screenshot()
    except Exception as e:
        raise RuntimeError(f"Error loading image - {e}")
    

    if template is None:
        return None

    if len(img.shape) != len(template.shape):
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #getting the maximum matched result. when threshold is less than 1 there could be multiple result.
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_value, _, max_loc = cv2.minMaxLoc(result)
    print(max_value, max_loc)

    if (max_value < threshold):
        if save_result:
            cv2.imwrite(f"test/debug/{time.time()}.png", img)
        return None

    #result returns the top-left location of the match. 
    h, w = template.shape[:2]
    #pointing to the middle of the matched box
    x = max_loc[0] + w//2
    y = max_loc[1] + h//2

    #saving the result for future debugging
    if save_result:
        debug_img = img.copy()
        cv2.rectangle(debug_img, max_loc, (max_loc[0]+w, max_loc[1]+h), (0,0,255), 2)
        cv2.imwrite(f"test/debug/{time.time()}.png", debug_img)

    return {"x" : x, "y" : y}


# def run_ocr(img_path=None, save_result=False, rois=None):
#     # Adding padding to process small rois better
#     # 👉 Modified to return the pad value so we can subtract it later
#     def add_padding(img, pad=50):
#         h, w, k = img.shape
#         avg_color = img.mean(axis=(0,1))

#         new_img = np.full((h + 2*pad, w + 2*pad, k), avg_color, dtype=img.dtype)
#         new_img[pad:pad+h, pad:pad+w] = img

#         return new_img, pad

#     if img_path:
#         img = cv2.imread(img_path)
#     else:
#         img = take_screenshot()

#     all_results =[]

#     # 👉 If ROI is provided
#     if rois:
#         h, w = img.shape[:2]
#         for roi in rois:
#             roi = clamp_roi(roi, w, h)
            
#             if not roi:
#                 continue
            
#             x1, y1, x2, y2 = roi
#             cropped = img[y1:y2, x1:x2]
            
#             # Unpack the padded image and the padding amount used
#             cropped, pad_val = add_padding(cropped, pad=50)
            
#             output = ocr.predict(cropped)[0]

#             results =[
#                 {
#                     "text": text,
#                     "score": float(score),
#                     # 👉 Fix: Subtract the padding amount, then add x1/y1
#                     "box": (box + np.array([x1 - pad_val, y1 - pad_val, x1 - pad_val, y1 - pad_val])).tolist()
#                 }
#                 for text, score, box in zip(
#                     output["rec_texts"],
#                     output["rec_scores"],
#                     output["rec_boxes"]
#                 )
#                 if score > 0.8
#             ]

#             all_results.extend(results)
#             print(all_results)

#             if save_result:
#                 cv2.imwrite(f"test/debug/roi-{time.time()}.png", cropped)

#     # 👉 If no ROI → normal full image OCR
#     else:
#         output = ocr.predict(img)[0]

#         all_results =[
#             {
#                 "text": text,
#                 "score": float(score),
#                 "box": box.tolist()
#             }
#             for text, score, box in zip(
#                 output["rec_texts"],
#                 output["rec_scores"],
#                 output["rec_boxes"]
#             ) if score > 0.8
#         ]

#         if save_result:
#             output.save_to_img("test/debug")
#     print(all_results)
#     return all_results




def run_ocr(img_path=None, save_result=False, rois=None):
    def add_padding(img, pad=50):
        h, w, k = img.shape
        avg_color = img.mean(axis=(0, 1))
        new_img = np.full((h + 2*pad, w + 2*pad, k), avg_color, dtype=img.dtype)
        new_img[pad:pad+h, pad:pad+w] = img
        return new_img, pad

    if img_path:
        img = cv2.imread(img_path)
    else:
        img = take_screenshot()

    if img is None:
        return []

    all_results = []
    h, w = img.shape[:2]
    
    # Ensure debug directory exists if saving
    if save_result and not os.path.exists("test/debug"):
        os.makedirs("test/debug", exist_ok=True)

    if rois:
        for i, roi in enumerate(rois):
            roi = clamp_roi(roi, w, h) 
            if not roi:
                continue

            x1, y1, x2, y2 = roi
            # Only pad if the crop actually has dimensions
            raw_crop = img[y1:y2, x1:x2]
            if raw_crop.size == 0:
                continue
                
            cropped, pad_val = add_padding(raw_crop, pad=50)

            output = ocr.ocr(cropped, cls=False)
            
            if not output or not output[0]:
                # If save_result is true, save the empty crop to see what OCR saw
                if save_result:
                    cv2.imwrite(f"test/debug/roi_empty_{int(time.time())}_{i}.png", cropped)
                continue
                
            lines = output[0]
            offset_x = x1 - pad_val
            offset_y = y1 - pad_val

            for line in lines:
                if not line or not isinstance(line, list) or len(line) < 2:
                    continue

                pts = np.array(line[0])
                text = line[1][0]
                score = float(line[1][1])

                if score > 0.8:
                    xmin = int(pts[:, 0].min())
                    ymin = int(pts[:, 1].min())
                    xmax = int(pts[:, 0].max())
                    ymax = int(pts[:, 1].max())

                    all_results.append({
                        "text": text,
                        "score": score,
                        "box": [
                            xmin + offset_x, 
                            ymin + offset_y, 
                            xmax + offset_x, 
                            ymax + offset_y
                        ]
                    })
            
            if save_result:
                # Save the specific crop being processed
                cv2.imwrite(f"test/debug/roi_crop_{int(time.time())}_{i}.png", cropped)

    else:
        output = ocr.ocr(img, cls=False)
        if output and output[0]:
            for line in output[0]:
                if not line: continue
                
                pts = np.array(line[0])
                text = line[1][0]
                score = float(line[1][1])

                if score > 0.8:
                    xmin = int(pts[:, 0].min())
                    ymin = int(pts[:, 1].min())
                    xmax = int(pts[:, 0].max())
                    ymax = int(pts[:, 1].max())

                    all_results.append({
                        "text": text,
                        "score": score,
                        "box": [xmin, ymin, xmax, ymax]
                    })

    # 👉 SAVE FULL RESULT IMAGE
    if save_result and all_results:
        debug_img = img.copy()
        for res in all_results:
            b = res["box"]
            # Draw rectangle: (xmin, ymin), (xmax, ymax)
            cv2.rectangle(debug_img, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
            cv2.putText(debug_img, res["text"], (int(b[0]), int(b[1]) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.imwrite(f"test/debug/full_res_{int(time.time())}.png", debug_img)

    for res in all_results:
        print(res["text"])
        
    return all_results


@app.post("/ocr")
def ocr_endpoint(req:OCRRequest):
    results = run_ocr(req.img_path, req.save_result, req.rois)

    if results is None:
        return{
            "success" : False,
            "results" : None
        }

    return {
        "success" : True,
        "count" : len(results),
        "results" : results
    }


@app.post("/template")
def template_matching(req:TemplateMatchRequest):
    results = match_template(req.name, req.threshold, req.save_result)

    if results is None:
        return{
            "success" : False,
            "results" : None
        }

    return {
        "success" : True,
        "results" : results
    }




@app.on_event("startup")
def on_startup():
    init_services()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
