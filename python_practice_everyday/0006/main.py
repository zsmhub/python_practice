# -*- coding: utf-8 -*-
'''
你有一个目录，放了你一个月的日记，都是 txt，为了避免分词的问题，假设内容都是英文，请统计出你认为每篇日记最重要的词

Author: Insomina
Version: 0.0.1
Date: 2017-10-30
Language: python3.6.2
Editor: Sublime Text 3
'''

import os, string, re
from collections import Counter

def get_word(str):
    '''
    获取字符串中使用频率最高的一个单词

    Args:
        str: 字符串内容
    '''
    regex = re.compile('[0-9a-z]+')
    word = re.findall(regex, str)
    c = Counter(word)
    return c.most_common()[0][0]

def main(path='./txt/'):
    '''
    获取路径下所有txt文件

    Args:
        path: txt文件路径
    '''
    for file_name in os.listdir(path):
        txt_path = os.path.join(path, file_name)
        with open(txt_path) as f:
            content = f.read().lower()
        word_most = get_word(content)
        print(txt_path, ' -> the most important word is:', word_most)

if __name__ == '__main__':
    main()