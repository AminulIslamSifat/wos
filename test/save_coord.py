import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import json
import time
import uvicorn
import numpy as np
from typing import Optional
from fastapi import FastAPI
from paddleocr import PaddleOCR
from pydantic import BaseModel

from core.core import req_ocr, req_temp_match

from cmd_program.screen_action import take_screenshot





data_dict = {}

data = req_ocr()
for i,d in enumerate(data):
    data_dict[f"World.Intel{i}"] = d

print(data_dict)
with open("db/World.Intel", "w") as file:
    json.dump(data_dict, file, indent=4)