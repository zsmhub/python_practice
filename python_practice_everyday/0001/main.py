# _*_ coding: utf-8 _*_
'''
第0001题：做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？

Author: Michael
Date: 2019-01-28
Language: 3.7.2
'''

import random
import string
import os

# 项目路径
cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'


def rand_str(num, length=7):
    print('Begin!')
    with open(cur_path + 'random_code.txt', 'w') as f:
        chars = string.ascii_letters + string.digits  # 所有字母和数字
        for i in range(num):
            code = ''  # 激活码/优惠券
            for j in range(length):
                code += random.choice(chars)
            f.write(code + "\r\n")
    print('End!')


if __name__ == '__main__':
    rand_str(200)
