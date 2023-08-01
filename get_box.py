
import base64
import urllib
import requests
from aip import AipOcr
from PIL import Image
import re
import os

# Image=Image.open(r'image.jpg')
# text = pytesseract.image_to_string(Image)
# file = open('output.txt', encoding='utf-8' , mode='w')
# file.writelines(text)
# print(text)
# file.close() 一坨，中英文混杂不能识别



#调用百度api
# from aip import AipOcr
#
# """ API """
# API_ID = ''
# API_KEY = ''
# SECRET_KEY = ''
#
# # 初始化AipFace对象
# client = AipOcr(API_ID, API_KEY, SECRET_KEY)    #到这里都是固定用法
# with open('image.jpg', 'rb') as f:
#     img = f.read()
# text = client.basicGeneral(img)
# #通用文字识别方式识别图片内容，一天50000次，像什么高精度版就是basicAccurate，具体参考下方aipocr模块文档
# for each in text.get('words_result'):
#     print(each.get('words'))

# python 3.5
# 百度tesseract-ocr使用


max_size = (4096, 4096) # 设置最大分辨率
APP_ID = '你的id'
API_KEY = '你的api_key'
SECRET_KEY = '你的secret_key'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
with open('image.jpg', 'rb') as f:
    img = Image.open(f)
    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.LANCZOS) # 缩小图像以适应最大分辨率
        img.save('resized_image.jpg')
        img = Image.open('resized_image.jpg')

#百度api最大支持分辨率为1096*1096


def main():
    #从鉴权人证获取access_token
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=24.3f706a72816331197ecd7cf6be756bfa.2592000.1693467775.282335-37015144"
    img=get_file_content_as_base64('resized_image.jpg')
    payload = {"image":img}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    # obj_temp = json.loads(response.content)
    #print(obj_temp['words_result'])
    text=response.text
    my_list = re.findall('[\u4e00-\u9fff]+', text)#只含中文符

    my_list = [char for char in my_list if '精' and '精炼' not in char]
    my_list = [char for char in my_list if '阶' not in char]
    print(my_list)
    with open('output.txt', 'w', encoding='utf-8') as f:
        for item in my_list:
            f.write(item + '\n')
    f.close()

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode('utf-8')
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


if __name__ == '__main__':
    main()
