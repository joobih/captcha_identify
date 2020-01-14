import os
from PIL import Image
import numpy as np

def dirpath():
    path = "../sample/test/"
    a = os.listdir(path)
    print(a)

def convert2gray(img):
    """
    图片转为灰度图，如果是3通道图则计算，单通道图则直接返回
    :param img:
    :return:
    """
    if len(img.shape) > 2:
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img


# 以第一个像素为准，相同色改为透明
def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = (255, 255, 255, 255)  # 要替换的颜色
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot, color_1)
    return img




def gen_captcha_text_image(img_path, img_name):
    """
    返回一个验证码的array形式和对应的字符串标签
    :return:tuple (str, numpy.array)
    """
    # 标签
    label = img_name.split("_")[0]
    # 文件
    img_file = os.path.join(img_path, img_name)
    captcha_image = Image.open(img_file)
    captcha_image.show()
    captcha_array = np.array(captcha_image)  # 向量化
    return label, captcha_array


if __name__ == '__main__':
    # dirpath()
    # img_path,img_name,  = "../sample/train/", "0aa6_1578464376631416.png"
    # a,b = gen_captcha_text_image(img_path, img_name)
    # print(a,b)
    # c = convert2gray(b)
    # print(c)
    # img = Image.fromarray(c)
    # img.show()
    # img_path = "../sample/7207_14974.jpg"
    # img = Image.open(img_path)
    # img = transparent_back(img)
    # img.save("2.png")
    img_path = "../sample/a.png"
    img_path2 = "../learn/2.png"
    img = Image.open(img_path)
    a = img.size
    img2 = Image.open(img_path2)
    print(a)
    b = img2.size
    print(b)
    img2 = img2.resize((100, 60))
    img2.save("3.png")