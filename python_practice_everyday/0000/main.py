#!/usr/bin/python
# _*_ coding: utf-8 _*_

' 第 0000 题：将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。 类似于图中效果 '

__author__ = 'Insomnia'

from PIL import Image, ImageDraw, ImageFont

# 项目路径
base_dir = '/usr/src/myapp/python_practice_everyday/0000/';

# 设置所使用的字体，注意设置字体文件拥有可执行权限
font = ImageFont.truetype(base_dir + "Arial.ttf", 24)

# 打开图片
imageFile = base_dir + "qq.jpeg"
im = Image.open(imageFile)
width, height = im.size #获取图片宽高

# 画图
draw = ImageDraw.Draw(im)
draw.text((width-30, 0), "4", (255, 0, 0), font=font) #设置文字位置/内容/颜色
draw = ImageDraw.Draw(im)

# 另存图片
im.save(base_dir + "target.jpg")