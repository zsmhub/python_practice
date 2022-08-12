# -*- coding: utf-8 -*-

'''
任一个英文的纯文本文件，统计其中的单词出现的个数

Author: Insomnia
Version: 0.0.1
Date: 2017-10-25
Language: Python 3.6.2
Editor: Sublime Text 3
'''

import re

# 读文件内容
file_path = './test.txt'
with open(file_path, 'r') as f:
    content= f.read()

# 正则匹配单词
regex = re.compile('[a-zA-Z]+')
list_word = re.findall(regex, content)

# 单词数量
print(len(list_word))