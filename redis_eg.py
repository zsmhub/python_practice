# -*- coding: utf-8 -*-
'''
redis案例

Author: Michael
Date: 2019-01-28
Language: 3.7.2
'''

from redis import StrictRedis

redis = StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    password='foobared',
    decode_responses=True)
redis.set('name', 'Michael')
print(redis.get('name'))
print(redis.randomkey())
redis.delete('name')
