import requests
from PIL import Image
import pytesseract

url = 'https://50.tsinghua.edu.cn/Kaptcha.jpg?9'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

respose = requests.get(url, headers=headers,verify=False)
print(respose.content.decode())
# 识别图片中的文字
#text = pytesseract.image_to_string(picture_response.text)
#print("识别结果：", text)

