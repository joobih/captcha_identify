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

    # 默认扰动角度范围
    DEFAULT_ROTATE_INTERVAL = (-30, 30)

    def __init__(self,  length=DEFAULT_LENGHT,
                 width=DEFAULT_WIDTH,
                 height=DEFAULT_HEIGHT,
                 fonts=DEFAULT_FONTS,
                 fonts_size=DEFAULT_FONTS_SIZE,
                 characters=DEFAULT_CHARS,
                 char_color = None,
                 background_color = None,
                 interval = DEFAULT_INTERVAL,
                 is_guss = False,
                 rotate_interval = DEFAULT_ROTATE_INTERVAL
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
        :param rotate_interval: 扰动范围参数，不扰动(0, 0)
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
        self._rotate_interval = rotate_interval

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
        if not self._background_color:
            self._background_color = self.random_color()
        image = Image.new('RGB', (self._width, self._height), self._background_color)
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
                if temp % 5 == 0:
                    draw.point((x, y), fill=self.random_color(100, 200))
        # for循环将字符添加到图中
        for t in range(self._length):
            dev_x = randint(0, 4)  # 随机左右浮动
            dev_y = randint(0, 2)  # 睡觉上下浮动
            # print(self._font_size)
            rand_font_size = choice(list(self._font_size))
            # print(rand_font_size, type(rand_font_size))
            x, y = rand_font_size * self._interval * t + dev_x, dev_y
            # print(x, y, rand_font_size)
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
            # mask = im.convert('L').point(table)
            # image.paste(im, (0, int((self._height - h) / 2)), mask)
            w, h = draw.textsize("2", font=font)
            dx = randint(0, 4)
            dy = randint(0, 3)
            im = Image.new('RGBA', (w + dx, h + dy))
            Draw(im).text((dx, dy), random_code[t], font=font, fill=char_color)
            im = im.rotate(uniform(self._rotate_interval[0], self._rotate_interval[1]), Image.BILINEAR, expand=1)
            r, g, b, a = im.split()
            image.paste(im, (int(x), y), mask=a)

            # draw.text((x, y), random_code[t],
            #           font=font, fill=char_color)
            # im = im.rotate(uniform(-30, 30), Image.BILINEAR, expand=1)

        # for x in range(self._width):
        #     for y in range(self._height):
        #         temp = x + y + randint(0, 10)
        #         if temp % 5 == 0:
        #             draw.point((x, y), fill=self.random_color(100, 200))
        # 进行高斯模糊
        if self._is_guss:
            image = image.filter(ImageFilter.GaussianBlur)
        # image = image.filter(ImageFilter.SMOOTH)
        # 将图片对象赋值给当前对象的verify_code_image属性
        return image

def test_img():
    import random
    s_width, s_height = 120, 4
    image = Image.new("RGB", (120, 40), (255,255,255))
    draw = Draw(image)
    # image.show()
    # im = Image.new("RGB", )
    fontpath = "./fonts/Arial.ttf"
    font = ImageFont.truetype(fontpath, 35)
    draw.text((0,0),"1", font=font, fill=(0, 0, 0))

    w, h = draw.textsize("2", font=font)

    dx = random.randint(0, 4)
    dy = random.randint(0, 6)
    im = Image.new('RGBA', (w + dx, h + dy))
    Draw(im).text((dx, dy), "2", font=font, fill=(56, 90, 0))
    im = im.rotate(random.uniform(-90, 90), Image.BILINEAR, expand=1)
    r, g, b, a = im.split()
    image.paste(im, (10, int((s_height - h) / 2)), mask=a)
    # im.show()
    image.show()
    # def _draw_character(c):
    #     font = "./fonts/Arial.ttf"
    #     fonts = ImageFont.truetype(font, 35)
    #     w, h = draw.textsize(c, font=fonts)
    #
    #     dx = random.randint(0, 4)
    #     dy = random.randint(0, 6)
    #     im = Image.new('RGBA', (w + dx, h + dy))
    #     color = (0,0,0,10)
    #     Draw(im).text((dx, dy), c, font=font, fill=color)
    #
    #     # rotate
    #     im = im.crop(im.getbbox())
    #     im = im.rotate(random.uniform(-30, 30), Image.BILINEAR, expand=1)
    #
    #     # warp
    #     dx = w * random.uniform(0.1, 0.3)
    #     dy = h * random.uniform(0.2, 0.3)
    #     x1 = int(random.uniform(-dx, dx))
    #     y1 = int(random.uniform(-dy, dy))
    #     x2 = int(random.uniform(-dx, dx))
    #     y2 = int(random.uniform(-dy, dy))
    #     w2 = w + abs(x1) + abs(x2)
    #     h2 = h + abs(y1) + abs(y2)
    #     data = (
    #         x1, y1,
    #         -x1, h2 - y2,
    #         w2 + x2, h2 + y2,
    #         w2 - x2, -y1,
    #     )
    #     im = im.resize((w2, h2))
    #     im = im.transform((w, h), Image.QUAD, data)
    #     return im
    #
    # images = []
    # chars = "1234"
    # for c in chars:
    #     if random.random() > 0.5:
    #         images.append(_draw_character(" "))
    #     images.append(_draw_character(c))
    #
    # text_width = sum([im.size[0] for im in images])
    #
    #
    # width = max(text_width, s_width)
    # image = image.resize((width, s_height))
    #
    # average = int(text_width / len(chars))
    # rand = int(0.25 * average)
    # offset = int(average * 0.1)
    # table = []
    # for i in range(256):
    #     table.append(i * 1.97)
    # for im in images:
    #     w, h = im.size
    #     mask = im.convert('L').point(table)
    #     image.paste(im, (offset, int((s_height - h) / 2)), mask)
    #     offset = offset + w + random.randint(-rand, 0)
    #
    # if width > s_width:
    #     image = image.resize((s_width, s_height))
    # image.show()


def get_one():
    with open("../conf/captcha_config.json", "r") as f:
        config = json.load(f)
    # 配置参数
    root_dir = "./test_img/"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    image_suffix = config["image_suffix"]  # 图片储存后缀
    characters = config["characters"]  # 图片上显示的字符集 # characters = "0123456789abcdefghijklmnopqrstuvwxyz"
    count = 1  # 生成多少张样本
    char_count = config["char_count"]  # 图片上的字符数量

    # 设置图片高度和宽度
    width = config["width"]
    height = config["height"]
    rand_color = VerifyCode.random_color(100,150)
    rand_back = VerifyCode.random_color(150, 200)
    vcode = VerifyCode(length=char_count, width=width, height=height,
                       characters=characters,
                       fonts=("fonts/Arial.ttf",),
                       fonts_size=(36,),
                       # char_color=(1,3,200),
                       background_color=rand_back,
                       char_color=rand_color,
                       rotate_interval=(-60, 60))
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
    for i in range(count):
        rand_color = VerifyCode.random_color(100, 150)
        rand_back = VerifyCode.random_color(150, 200)
        vcode = VerifyCode(length=char_count, width=width, height=height,
                           characters=characters,
                           fonts=("fonts/Arial.ttf",),
                           fonts_size=(36,),
                           # char_color=(1,3,200),
                           background_color=rand_back,
                           char_color=rand_color,
                           rotate_interval=(-60, 60))
    # for i in range(count):
        text = vcode.get_random_code()
        img = vcode.set_image(text)
        timec = str(time.time()).replace(".", "")
        p = os.path.join(root_dir, f"{text}_{timec}.{image_suffix}")
        img.save(p)
        print("Generate captcha image",text,i)

def get_px_color():
    import cv2
    imgpath = "../sample/huaxi_captcha/0023_157855692296774.jpg"
    r,g,b = 0, 0, 0
    rm,gm,bm = 255, 255, 255
    img = cv2.imread(imgpath)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            px = img[x, y]
            print(px)
            if px[0]>r:
                r=px[0]
            if px[1]>g:
                g= px[1]
            if px[2]>b:
                b = px[2]
            if px[0]<rm:
                rm=px[0]
            if px[1]<gm:
                gm= px[1]
            if px[2]<bm:
                bm = px[2]
    print(r,g,b)
    print(rm,gm,bm)

if __name__ == '__main__':
    # vcode = VerifyCode()
    # str_code = vcode.verify_code
    # image_code = vcode.verify_image
    # image_code.save("rand2.jpg")
    main()
    # for i in range(0, 10):
    #     get_one()
    # test_img()
    # get_px_color()