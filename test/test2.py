import os
import cv2
import time
from pathlib import Path



t1 = time.time()
root_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets")))
for file_path in root_dir.rglob("*"):
    if file_path.is_file():
        print(file_path.name)
t2 = time.time()
print(f"Time required to load all the image in cache is {t2 - t1} seconds")




# t1 = time.time()
# path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
# for dirpath, dirname, filenames in os.walk(path):
#     for filename in filenames:
#         #print(os.path.join(dirpath, filename))
#         continue
# t2 = time.time()
# tl2 = t2 - t1
# print(f"Time required for ---- is {t2-t1} seconds")



# print(tl1/tl2)














# t1 = time.time()
# _template_cache = {}
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "arena"))

# for file in os.listdir(path):
#     if file.lower().endswith(".jpg") or file.lower().endswith(".png"):
#         fn = os.path.splitext(file)[0]
#         img = cv2.imread(os.path.join(path, file))

#         if img is not None:
#             _template_cache[fn] = img
# t2 = time.time()
# print(f"Time required to load all the image in cache is {t2 - t1} seconds")




# t1 = time.time()
# img = cv2.imread("assets/arena/arena.jpg")
# t2 = time.time()
# tl1 = t2 - t1
# print(f"Time required for to a image directly from file is {tl1} seconds")



# t1 = time.time()
# img = _template_cache["arena"]
# t2 = time.time()
# tl2 = t2 - t1
# print(f"Time required for loading image from cache  is {tl2} seconds")


# print(f"Caching is {tl1/tl2} times faster")