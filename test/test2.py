from paddleocr import PaddleOCR
import os
import time


ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False) 




for i in range(10):
    t1 = time.time()
    result = ocr.predict("cache/wos.png")
    for res in result:
        res.print()
        t2 = time.time()
        print(f"Time required {(t2-t1)} seconds")
        res.save_to_img("output")
        res.save_to_json("output")
        


