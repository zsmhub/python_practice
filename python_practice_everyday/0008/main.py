# -*- coding: utf-8 -*-
'''
一个HTML文件，找出里面的正文

Author: Michael
Date: 2019-02-27
Language: 3.7.2
'''

import os
from bs4 import BeautifulSoup

# 当前脚本目录
cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'

html_path = cur_path + 'test.html'
with open(html_path, 'r') as f:
    c = f.read()

soup = BeautifulSoup(c, 'html.parser')
body = soup.find('body').get_text()

print('html正文:', body)
