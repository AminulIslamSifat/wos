from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import time

ocr = PaddleOCR(use_angle_cls=True, lang='en')

t1 = time.time()

result = ocr.ocr('cache/wos.png', cls=True)

# Load image
image = Image.open('cache/wos.png').convert('RGB')

# Extract boxes, texts, scores
boxes = [line[0] for line in result[0]]
txts = [line[1][0] for line in result[0]]
scores = [line[1][1] for line in result[0]]

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Draw result
im_show = draw_ocr(image, boxes, txts, scores, font_path=font_path)



# Convert to PIL Image and save
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

t2 = time.time()
print(t2 - t1)