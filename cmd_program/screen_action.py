import os
import cv2
import time
import subprocess
import numpy as np




def run_adb_command(cmd, device_id):
    #running the adb command and chekcing if the adb is available or not
    try:
        subprocess.run(["adb", "-s", str(device_id)] + cmd, check = True)
    except Exception as e:
        raise RuntimeError(f"adb command failed - {e}")



def tap_screen(*args, device_id="131393852O003802"):
    # Handling both tuple and normal x,y coordination and converting them to string
    # Used default device_id so that it won't cause problem when multiple device is connected
    if len(args) == 1:
        if args[0] == None:
            raise RuntimeError("Coordination not found")
        x, y = args[0]
    elif len(args)==2:
        x, y = args
    else:
        raise ValueError
    
    adb_command = ["shell", "input", "tap", str(x), str(y)]
    run_adb_command(adb_command, device_id)



def swipe_screen(*args, duration=300, device_id="131393852O003802"):
    if len(args) == 2:
        (x1, y1), (x2, y2) = args
    elif len(args) == 4:
        x1, y1, x2, y2 = args
    else:
        raise ValueError
    
    duration = str(duration)

    adb_command = ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)]
    run_adb_command(adb_command, device_id)



def long_press(*args, duration=300, device_id="131393852O003802"):
    # in case of long press, its similar to swipe while the starting and ending location is the same
    if len(args) == 1:
        x, y = args[0]
    elif len(args)==2:
        x, y = args
    else:
        raise ValueError
    
    duration = str(duration)

    adb_command = ["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration)]
    run_adb_command(adb_command, device_id)





def take_screenshot(device_id="131393852O003802", save=False):
    adb_command = ["adb", "-s", str(device_id), "exec-out", "screencap", "-p"]
    raw = subprocess.check_output(adb_command)

    img_array = np.frombuffer(raw, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        raise RuntimeError("Failed to decode the image")
    elif save:
        os.makedirs("cache", exist_ok=True)
        cv2.imwrite(f"cache/wos-{int(time.time())}.png", img)
    
    return img




def clear_input(count=6, device_id="13139385O0003802"):
    run_adb_command(["shell", "input", "keyevent", "123"], device_id)

    for i in range(count):
        run_adb_command(["shell", "input", "keyevent", "67"], device_id)



def input_text(text, device_id="131393852O003802", backspace=6):
    text = text.replace(" ", "%s")

    adb_command = ["shell", "input", "text", text]
    clear_input(count=backspace, device_id=device_id)
    run_adb_command(adb_command, device_id)
    run_adb_command(["shell", "input", "keyevent", "66"], device_id=device_id)
    print(f"Text Input: {text}")