import os
from PIL import Image
import base64
import requests
import json
import time

def download():
    url = "https://hytwechat.cd120.com/hyt/wechat/captcha"
    param = {
        "hisCode":"HID0101",
        "captchaType":"REQ_APPOINTMENT"
    }
    headers = {
      "Host": "hytwechat.cd120.com",
      "Connection": "keep-alive",
      "Accept": "application/json, text/javascript, */*; q=0.01",
      "Origin": "https://hytwechat.cd120.com",
      "X-Requested-With": "XMLHttpRequest",
      "User-Agent": "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Pro Build/PKQ1.181203.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/45016 Mobile Safari/537.36 MMWEBID/3452 MicroMessenger/7.0.10.1580(0x27000A55) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
      "Content-Type": "application/json",
      "Referer": "https://hytwechat.cd120.com/hyt/wechat/appointmentRequest/57280%7C%7C166?today=0&hisCode=HID0101",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "zh-CN,en-US;q=0.9",
      "Cookie": "JSESSIONID=7892E47D95241A827048E071E4647974; _ga=GA1.2.666627702.1577684907",
    }
    param = json.dumps(param)
    r = requests.post(url, param, headers=headers)
    data = r.content.decode()
    # print(data)
    data = json.loads(data)
    # print(data)
    baseimg = data["data"]["captchaImg"]
    timetext = str(time.time()).replace(".","") + ".jpg"
    rootpath = "../sample/huaxi_captcha/"
    if not os.path.exists(rootpath):
        os.makedirs(rootpath)
    imgpath = rootpath + timetext
    base64toimg(baseimg, imgpath)
    # imgpath =

def base64toimg(b64imgstr,savepath):
    img_byte = base64.b64decode(b64imgstr)
    with open(savepath,"bw") as f:
        f.write(img_byte)
    # img = Image.frombytes(img_byte)

if __name__ == '__main__':
    # b64imgstr = "/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a\nHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIy\nMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAoAHgDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD064uY\nbSFpp5FjjXqzVzp8VmXUbeKGDbbPIFMj9WGcZHpXQXdnBfQiK4TegYNjPcVzni+CNLa1eLYhhbbt\nXAwD04/4CauTsa01FuzOqpskkcKF5XVEHVmOAKzor28u7W2lgiSMS7fmkXfnjk4U4A75J7YxyKgi\nhZp1uLuF5LtJwsAknAwNvorbScMxOFGdo+9tViNmTaT1K2q+Lraw8yNIm3pwXm/doMjqc8/gcVk3\nGratb3kFzfRyxhZMiPc0auMZ24zggZBzgnIwT1Fb0drJZXEjzSlU84SG4aRYVb5SOgzuOM7t2Bnl\nQO3PahqNvd2bW0NuY5j+8fE6qgI42/KQrYVECk9sdCDU6vZm9N+R1NjcRz29tdQGZwyBBCs2/Kht\n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"
    # savepath = "./a.jpg"
    # base64toimg(b64imgstr, savepath)
    # img = Image.open("../sample/origin/0001_15785383976714654.png")
    # print(img.size)
    for i in range(0, 1000):
        download()
        time.sleep(0.5)
        print(f"下载第{i+1}张图片")