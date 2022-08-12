# -*- coding: utf-8 -*-
'''
第 0003 题：将 0001 题生成的 200 个激活码（或者优惠券）保存到 Redis 非关系型数据库中。

Author: Michael
Date: 2019-01-28
Language: 3.7.2
'''

import random
import string
from redis import StrictRedis

redis = StrictRedis(
    host='127.0.0.1',
    port=6379,
    db=0,
    password='foobared',
    decode_responses=True)


def rand_str(num, length=7):
    chars = string.ascii_letters + string.digits  # 所有字母和数字
    for i in range(num):
        code = ''  # 激活码/优惠券
        for j in range(length):
            code += random.choice(chars)
        redis.rpush('list', code)


if __name__ == '__main__':
    rand_str(10)
    num = redis.llen('list')
    print(num)
    codes = redis.lrange('list', 0, num - 1)
    print(codes)
    redis.delete('list')
