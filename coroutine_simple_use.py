# -*- coding: utf-8 -*-
'''
实现协程的简单使用

Author: Insomnia
Version: 0.0.2
Date: 2017-10-20
Language: Python3.6.2
Editor: Sublime Text3
'''

import asyncio
import time

now = lambda: time.time()

# async定义一个协程对象,协程不能直接运行，需要把协程加入到事件循环（loop），由后者在适当的时候调用协程
async def do_some_work(x):
    print('waiting: %s' % x)
    await asyncio.sleep(x) # await用于挂起阻塞的异步调用接口
    return 'Done after %s s' % x

start =  now()

loop = asyncio.get_event_loop() # 事件循环
tasks = [asyncio.ensure_future(do_some_work(var)) for var in (1, 2, 4)] # asyncio.ensure_future()获取协程对象返回值
loop.run_until_complete(asyncio.wait(tasks)) # 将协程注册到事件循环，并启动事件循环
loop.close()

for task in tasks:
    print('Task ret: %s' % task.result())

print('Time: ', now()-start)