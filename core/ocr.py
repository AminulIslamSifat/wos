import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import json
import time
import paddle           #Important for paddleocr 2.10.0
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


#Printing the version of paddleocr
print(f"PaddleOCR Version: {paddleocr.__version__}")
print(f"PaddlePaddle Version: {paddle.__version__}")

#Disabling logging from the paddleocr
import logging
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.ERROR)


#------------------- Data Models ---------------------------------#

#input schema for fastapi
class OCRRequest(BaseModel):
    img_path: Optional[str] = None
    save_result: Optional[bool] = False
    rois: Optional[list[list[int]]] = None


class TemplateMatchRequest(BaseModel):
    name: str
    threshold: Optional[float] = None
    save_result: Optional[bool] = False,
    rois: Optional[list[list[int]]] = None


#------------------- Configuration ------------------------------#
SCREENSHOT_TTL = 0.1
CPU_THREADS = os.cpu_count() or 1
TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "references", "icon"))


#---------------------- Globals ---------------------------------#
app = FastAPI()
_template_cache = {}


#----------------------- Functions -------------------------------#
def init_services():
    global ocr, _template_cache
    #initializeng the ocr once for all
    # ocr = PaddleOCR(
    #         use_doc_orientation_classify=False,
    #         use_doc_unwarping=False,
    #         use_textline_orientation=False
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
    print(root_dir)
    for file_path in root_dir.rglob("*.png"):
        if file_path.is_file():
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



def match_template(name, threshold=0.8, save_result=None, rois=None):
    if name not in _template_cache:
        template = cv2.imread(name)
    else:
        template = _template_cache[name]

    try:
        img = take_screenshot()
    except Exception as e:
        raise RuntimeError(f"Error loading image - {e}")

    if template is None:
        return None

    if len(img.shape) != len(template.shape):
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = template.shape[:2]
    img_h, img_w = img.shape[:2]

    # If no ROI → use full image
    if not rois:
        rois = [[0, 0, img_w, img_h]]

    matches = []

    for roi in rois:
        roi = clamp_roi(roi, img_w, img_h)
        if roi is None:
            continue  # skip invalid ROI

        x1, y1, x2, y2 = roi
        roi_img = img[y1:y2, x1:x2]

        # skip empty regions
        if roi_img.size == 0:
            continue

        result = cv2.matchTemplate(roi_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_value, _, max_loc = cv2.minMaxLoc(result)
        print(f"Best Match: {max_loc} ------ Score: {max_value}")

        locations = np.where(result >= threshold)
        locations = list(zip(locations[1], locations[0]))  # (x, y)

        for pt in locations:
            score = result[pt[1], pt[0]]

            # 🔥 map back to original image coords
            x_center = int( x1 + pt[0] + w // 2 )
            y_center = int( y1 + pt[1] + h // 2 )
            x1_abs = int(x1 + pt[0])
            y1_abs = int(y1 + pt[1])
            x2_abs = int(x1_abs + w)
            y2_abs = int(y1_abs + h)


            too_close = False

            for m in matches:
                if abs(m["box"][0] - x_center) < w and abs(m["box"][1] - y_center) < h:
                    too_close = True
                    if score > m["score"]:
                        m["box"] = [x1_abs, y1_abs, x2_abs, y2_abs]
                        m["score"] = float(score)
                    break

            if not too_close:
                matches.append({
                    "box": [x1_abs, y1_abs, x2_abs, y2_abs],
                    "score": float(score)
                })

    # 🖼 debug
    if save_result:
        debug_img = img.copy()
        for m in matches:
            cx1, cy1, cx2, cy2 = m["box"]
            cv2.rectangle(debug_img,
                          (cx1, cy1),
                          (cx2, cy2),
                          (0, 0, 255), 2)
        cv2.imwrite(f"test/debug/{time.time()}.png", debug_img)

    return matches



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
    try:
        if img_path:
            img = cv2.imread(img_path)
        else:
            img = take_screenshot()
    except Exception as e:
        print(f"Error - {e}")

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
        print(f"{res['text']} ------- Box: {res['box']} ------- Score: {res['score']}")
        
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
    results = match_template(req.name, req.threshold, req.save_result, req.rois)

    if results is None:
        return{
            "success" : False,
            "results" : None
        }

    return {
        "success" : True,
        "results" : results
    }




init_services()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
