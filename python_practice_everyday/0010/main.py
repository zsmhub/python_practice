# -*- coding: utf-8 -*-
'''
使用 Python 生成类似于下图中的字母验证码图片

Author: Michael
Date: 2019-03-07
Language: 3.7.2
'''

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import string
import random
import os

cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'

font_path = '/Library/Fonts/Arial Bold.ttf'


# 获取随机四个字母
def get_random_char():
    return [random.choice(string.ascii_letters) for _ in range(4)]


# 获取颜色
def get_random_color():
    return (random.randint(30, 100), random.randint(30, 100),
            random.randint(30, 100))


# 获取验证码图片
def get_code_pic():
    w = 240
    h = 60
    # 创建画布
    image = Image.new('RGB', (w, h), (180, 180, 180))
    font = ImageFont.truetype(font_path, 40)
    draw = ImageDraw.Draw(image)
    # 创建验证码对象
    code = get_random_char()
    # 把验证码放在画布上
    for t in range(4):
        draw.text((60 * t + 10, 0),
                  code[t],
                  font=font,
                  fill=get_random_color())
    # 填充噪点
    for _ in range(random.randint(1500, 3000)):
        draw.point((random.randint(0, w), random.randint(0, h)),
                   fill=get_random_color())
    # 模糊处理
    image = image.filter(ImageFilter.BLUR)
    # 保存图片
    image.save(cur_path + ''.join(code) + '.jpeg', 'jpeg')


if __name__ == '__main__':
    get_code_pic()
