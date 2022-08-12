# -*- coding: utf-8 -*-
'''
你有一个目录，装了很多照片，把它们的尺寸变成都不大于iPhone5分辨率的大小。

Author: Insomnia
Version: 0.0.1
Date: 2017-10-26
Language: Python 3.6.2
Editor: Sublime Text 3
'''

import os
from PIL import Image

# iphone5的分辨率
iphone_w = 640
iphone_h = 1136

def mkdir(path):
    '''
    创建文件夹

    Args:
        path: 目录路径
    '''
    if not os.path.exists(path):
        os.mkdir(path)

def resize_img(path, new_path):
    '''
    修改图片大小并保存
    '''
    im = Image.open(path)
    w, h = im.size

    if(w > iphone_w and h > iphone_h):
        w, h = iphone_w, iphone_h
    elif(w > iphone_w):
        h = int(w * iphone_h / iphone_w)
        w = iphone_w
    elif(h > iphone_h):
        w = int(h * iphone_w / iphone_h)
        h = iphone_h

    im_resized = im.resize((w, h), Image.ANTIALIAS)
    im_resized.save(new_path)

def main(path):
    '''
    遍历图片文件并进行修改大小
    '''
    # 修改大小后的图片保存路径
    img_save_path = os.path.join(path, 'resize')
    mkdir(img_save_path)

    # 遍历文件
    files = os.listdir(path)
    for file_name in files:
        if file_name.endswith('jpg') or file_name.endswith('png'):
            img_path = os.path.join(path, file_name) # 图片路径
            img_new_path = os.path.join(img_save_path, file_name)
            resize_img(img_path, img_new_path)

if __name__ == '__main__':
    main('./images/')