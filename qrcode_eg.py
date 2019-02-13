# -*- coding: utf-8 -*-
'''
生成二维码&识别二维码案例

Author: Michael
Date: 2019-02-13
Language: 3.7.2
'''

import os
import qrcode
import zxing
'''
生成二维码
'''
# 当前脚本目录
cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'

# 二维码内容
data = "Flora老婆，情人节快乐!\n陪你度过的第4个情人节!\n♡I love you!♡\n-- Michael ^_^\n2019-02-14"

# 生成二维码
img = qrcode.make(data=data)

# 直接显示二维码
# img.show()

# 保存二维码
img_path = cur_path + "qrcode.jpg"
img.save(img_path)
'''
识别二维码(zxing包依赖JDK环境，需要先安装JDK环境)
eg: brew cask install java
'''
reader = zxing.BarCodeReader()
barcode = reader.decode(img_path)
print(barcode.parsed)
