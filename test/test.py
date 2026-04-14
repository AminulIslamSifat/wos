import os
import sys
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cmd_program.screen_action import take_screenshot

img = take_screenshot(save=True)