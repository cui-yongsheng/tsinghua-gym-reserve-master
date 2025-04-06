import easyocr
import cv2

img = cv2.imread("../yzm.png")
print(img.shape)
cropped = img[0:30, 30:100]  # 裁剪坐标为[y0:y1, x0:x1]
cv2.imwrite("../yzm.png", cropped)

# 创建OCR对象
reader = easyocr.Reader(['en'])

# 识别文字
result = reader.readtext('yzm.png')
print(result)
# 处理识别结果
text, bbox, confidence = result[0]

print(confidence)