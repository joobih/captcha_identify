import os
"""
sudo pip3 install opencv-python
"""
import cv2
import numpy as np
import json
import time
import random


def randcolor():
    return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))


def randchar(characters):
    return random.choice(characters)


def randpos(x_start, x_end, y_start, y_end):
    return (np.random.randint(x_start, x_end),
            np.random.randint(y_start, y_end))

def gen_captcha(root_dir, image_suffix, characters, count, char_count, width, height, line_num):
    for j in range(count):
        img_name = ""
        # 生成一个随机矩阵，randint(low[, high, size, dtype])
        img = np.random.randint(np.random.randint(50, 100), np.random.randint(100, 150), (height, width, 3), np.uint8)
        # 显示图像
        # cv2.imshow("ranImg",img)
        x_pos = 0
        y_pos = 20
        for _ in range(char_count):
            char = randchar(characters)
            img_name += char
            #各参数依次是：图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细
            cv2.putText(img, char,
                        (np.random.randint(x_pos, x_pos + 12), np.random.randint(y_pos, y_pos + 10)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        randcolor(),
                        3,
                        cv2.LINE_AA)
            x_pos += 25

        # 添加线段
        for _ in range(line_num):
            img = cv2.line(img,
                           randpos(0, width, 0, height),
                           randpos(0, width, 0, height),
                           randcolor(),
                           np.random.randint(1, 2))

        # cv2.imshow("line",img)
        # input("")
        timec = str(time.time()).replace(".", "")
        a =cv2.imwrite(root_dir + img_name + f"_{timec}.{image_suffix}", img)
        print("Generate captcha image", a, j)

def get_one():
    with open("../conf/captcha_config.json", "r") as f:
        config = json.load(f)
    # 配置参数
    root_dir = "./"  # 图片储存路径
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    image_suffix = config["image_suffix"]  # 图片储存后缀
    characters = config["characters"]  # 图片上显示的字符集 # characters = "0123456789abcdefghijklmnopqrstuvwxyz"
    count = 1  # 生成多少张样本
    char_count = config["char_count"]  # 图片上的字符数量

    # 设置图片高度和宽度
    width = config["width"]
    height = config["height"]
    line_num = config["line_num"]

    gen_captcha(root_dir,image_suffix,characters,count,char_count,width,height,line_num)

def main():
    with open("../conf/captcha_config.json", "r") as f:
        config = json.load(f)
    # 配置参数
    root_dir = config["root_dir"]  # 图片储存路径
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    image_suffix = config["image_suffix"]  # 图片储存后缀
    characters = config["characters"]  # 图片上显示的字符集 # characters = "0123456789abcdefghijklmnopqrstuvwxyz"
    count = config["count"]  # 生成多少张样本
    char_count = config["char_count"]  # 图片上的字符数量

    # 设置图片高度和宽度
    width = config["width"]
    height = config["height"]
    line_num = config["line_num"]

    gen_captcha(root_dir,image_suffix,characters,count,char_count,width,height,line_num)


if __name__ == '__main__':
    # main()
    get_one()