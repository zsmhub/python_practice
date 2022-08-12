# -*- coding: utf-8 -*-
'''
一个HTML文件，找出里面的链接

Author: Michael
Date: 2019-02-27
Language: 3.7.2
'''

import os
from bs4 import BeautifulSoup

cur_path = os.path.split(os.path.realpath(__file__))[0]

html_path = cur_path + '/test.html'
with open(html_path, 'r') as f:
    c = f.read()

soup = BeautifulSoup(c, 'html.parser')
a = soup.find('body').find_all('a')
arr = list(map(lambda x: x['href'], a))

print(arr)
