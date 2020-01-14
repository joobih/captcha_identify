import os
from random import choice, randint, uniform
import json
import time
from PIL.ImageDraw import Draw
"""
sudo pip3 install PIL
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter



class VerifyCode(object):
    """生成验证码模块"""
    # 去掉易混淆字符'i' 'I' 'l' 'L' 'o' 'O' 'z' 'Z'
    DEFAULT_CHARS = "0123456789abcdefghjkmnpqrstuvwxyABCDEFGHJKMNPQSTUVWXY"

    # 默认字体
    DEFAULT_FONTS = ("./fonts/Arial.ttf", "./fonts/DeeDee.ttf")

    # 默认字体大小
    DEFAULT_FONTS_SIZE = (34, 37, 40, 43, 46)

    # 默认长宽
    DEFAULT_WIDTH, DEFAULT_HEIGHT = 160, 40

    # 默认字符长度
    DEFAULT_LENGHT = 6

    # 默认间隔距离倍数
    DEFAULT_INTERVAL = 0.8

    def __init__(self,  length=DEFAULT_LENGHT,
                 width=DEFAULT_WIDTH,
                 height=DEFAULT_HEIGHT,
                 fonts=DEFAULT_FONTS,
                 fonts_size=DEFAULT_FONTS_SIZE,
                 characters=DEFAULT_CHARS,
                 char_color = None,
                 background_color = None,
                 interval = DEFAULT_INTERVAL,
                 is_guss = False
                 ):
        """
        验证码初始化方法
        :param length: 验证码长度 默认length=6
        :param width: 验证码图片宽度 默认width=160
        :param height: 验证码图片高度 默认height=50
        :param fonts_size: 字体大小 默认font_size=[40, 42, 44, 46]
        :param char_color: 验证码字体颜色，默认随机
        :param interval: 每个字符之间的距离倍数设置，默认为0.8
        :param is_guss: 是否进行高斯模糊，默认为否
        :param background_color: 背景图，默认随机浅色范围
        """
        self._verify_code_image = None  # PIL图片Image对象
        self._length = length  # 验证码长度
        self._width = width  # 图片宽度
        self._height = height  # 图片高度
        self._fonts = fonts
        self._font_size = fonts_size  # 字体大小
        self._characters = characters
        self._char_color = char_color
        self._interval = interval
        self._is_guss = is_guss
        self._background_color = background_color

    def get_random_code(self):
        """
        随机生成验证码字符
        """
        code = ''  # 生成的验证码
        for _ in range(self._length):  # 循环随机取一个字符
            code += choice(self._characters)
        return code

    @staticmethod
    def random_color(s=0, e=255):
        """
        随机生成RGB颜色
        :param s: 开始范围
        :param e: 结束范围
        :return: Tuple (r, g, b)
        """
        s = s if 0 <= s <= 255 else 0  # 限定范围 0 - 255
        e = e if 0 <= e <= 255 else 255  # 限定范围 0 - 255
        s, e = (s, e) if s < e else (e, s)  # 限定大小 s 必须小于 e
        return randint(s, e), randint(s, e), randint(s, e)

    def set_image(self, random_code):
        """
        生成验证码图片
        :return: None
        """
        # 创建一个Image对象, 全黑的画布
        image = Image.new('RGB', (self._width, self._height), (0, 0, 0))
        # 创建一个字体对象
        # table = []
        # for i in range(256):
        #     table.append(i * 1.97)
        # font = ImageFont.truetype('fonts/Arial.ttf', self._font_size)
        # 创建一个画图对象
        draw = ImageDraw.Draw(image)
        # for循环随机生成噪点
        for x in range(self._width):
            for y in range(self._height):
                temp = x + y + randint(0, 10)
                if temp % 10 == 0:
                    draw.point((x, y), fill=self.random_color(0, 255))
        # for循环将字符添加到图中
        for t in range(self._length):
            dev_x = randint(0, 5)  # 随机左右浮动
            dev_y = randint(0, 5)  # 睡觉上下浮动
            # print(self._font_size)
            rand_font_size = choice(list(self._font_size))
            # print(rand_font_size, type(rand_font_size))
            x, y = rand_font_size * self._interval * t + dev_x, dev_y
            print(x, y, rand_font_size)
            # 将字符通过随机颜色画到图片中
            rand_font_size = choice(list(self._font_size))
            rand_font = choice(self._fonts)
            font = ImageFont.truetype(rand_font, rand_font_size)
            if not self._char_color:
                char_color = self.random_color()
            else:
                char_color = self._char_color
            # im = Image.new('RGBA', (0,0,0,0))
            # Draw(im).text((x, y), random_code[t],
            #      font=font, fill=char_color)
            # imdraw =
            draw.text((x, y), random_code[t],
                      font=font, fill=char_color)
            # mask = im.convert('L').point(table)
            # image.paste(im, (0, int((self._height - h) / 2)), mask)
            draw.text((x, y), random_code[t],
                      font=font, fill=char_color)
            # im = im.rotate(uniform(-30, 30), Image.BILINEAR, expand=1)
        # 进行高斯模糊
        if self._is_guss:
            image = image.filter(ImageFilter.GaussianBlur)
        # image = image.filter(ImageFilter.SMOOTH)
        # 将图片对象赋值给当前对象的verify_code_image属性
        return image

def get_one():
    with open("../conf/captcha_config.json", "r") as f:
        config = json.load(f)
    # 配置参数
    root_dir = "./"
    image_suffix = config["image_suffix"]  # 图片储存后缀
    characters = config["characters"]  # 图片上显示的字符集 # characters = "0123456789abcdefghijklmnopqrstuvwxyz"
    count = 1  # 生成多少张样本
    char_count = config["char_count"]  # 图片上的字符数量

    # 设置图片高度和宽度
    width = config["width"]
    height = config["height"]
    vcode = VerifyCode(length=char_count, width=width, height=height,
                       characters=characters,
                       fonts=("fonts/Arial.ttf",),
                       fonts_size=(36,),
                       char_color=(1,3,200))
    for i in range(count):
        text = vcode.get_random_code()
        img = vcode.set_image(text)
        timec = str(time.time()).replace(".", "")
        p = os.path.join(root_dir, f"{text}_{timec}.{image_suffix}")
        img.save(p)
        print("Generate captcha image",text,i)

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
    vcode = VerifyCode(length=char_count, width=width, height=height, fonts_size=(30,),
                       characters=characters, char_color=(1,3,200))
    for i in range(count):
        text = vcode.get_random_code()
        img = vcode.set_image(text)
        timec = str(time.time()).replace(".", "")
        p = os.path.join(root_dir, f"{text}_{timec}.{image_suffix}")
        img.save(p)
        print("Generate captcha image",text,i)

if __name__ == '__main__':
    # vcode = VerifyCode()
    # str_code = vcode.verify_code
    # image_code = vcode.verify_image
    # image_code.save("rand2.jpg")
    # main()
    get_one()
