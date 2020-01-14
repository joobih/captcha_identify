## 本项目总共有三大模块

### 一，验证码网页素材收集 collect_captcha_by_hand

- 该模块可以让你将需要识别的验证码在网页上面显示。手动输入生成验证码素材库。可以方便快速的收集
- 该模块使用tornado搭建，结合templae模板简单实现了前端的网页。

1. 启动项目:

```bash
python3 collect_hand_web_server.py
```

2. 访问地址:

[网页手动收集](http://127.0.0.1:9000/get?one_page=10)

3. 可以自己设置one_page参数每一页显示的图片数量。

4. 该模块配置文件路径 conf/identify_config.json

    source_path --图片素材库(待手动识别)
    count --验证码字符数量

### 二，验证码随机生成模块 gen_captcha

> 该模块为随机生成验证码的模块，可以自己配置背景颜色，字符颜色，是否扰动，是否增加
> 高斯干扰，随机噪点等。也可以自己配置字体，字符大小，字符范围等。

1. fonts/

    存放一些字体
   
2. gen_sample_base.py

    生成验证码文件
    
例1：使用默认参数生成验证码
    
 ```python
import os
import time
from gen_sample_base import VerifyCode

root_dir = "./"
image_suffix = "jpg"

vcode = VerifyCode()
text = vcode.get_random_code()
img = vcode.set_image(text)
timec = str(time.time()).replace(".", "")
p = os.path.join(root_dir, f"{text}_{timec}.{image_suffix}")
img.save(p)

```

例2：使用指定背景图，字体fonts/Arial.ttf，字体大小36，字符颜色，增加扰动角度范围(rotate_interval)，指定字符数量4来生成验证码
图片size= (120, 40), 字符范围0123456789abcdefghjkmnpqrstuvwxyABCDEFGHJKMNPQRSTUVWXY(去除干扰字符iIlLoOzZ)
其中字体大小可以指定多个，生成时随机选择, 如(36, 38, 40, 43)
```python
import os
import time
from gen_sample_base import VerifyCode

root_dir = "./"
image_suffix = "jpg"

characters = "0123456789abcdefghjkmnpqrstuvwxyABCDEFGHJKMNPQRSTUVWXY"
rand_color = VerifyCode.random_color(100, 150)
rand_back = VerifyCode.random_color(150, 200)
vcode = VerifyCode(length=4, width=120, height=40,
                           characters=characters,
                           fonts=("fonts/Arial.ttf",),
                           fonts_size=(36,),
                           background_color=rand_back,
                           char_color=rand_color,
                           rotate_interval=(-60, 60))

text = vcode.get_random_code()
img = vcode.set_image(text)
timec = str(time.time()).replace(".", "")
p = os.path.join(root_dir, f"{text}_{timec}.{image_suffix}")
img.save(p)
```

### 三，卷积神经网络学习

该项目作者:nickliqian

项目地址:https://github.com/nickliqian/cnn_captcha


