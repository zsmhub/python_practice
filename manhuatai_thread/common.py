# -*- coding: utf-8 -*-

import os, time

class Common(object):
    '''
    一些通用函数
    '''

    def __init__(self):
        pass

    def mkdir(self, path):
        '''
        创建文件夹

        Args:
            path: 目录路径
        '''
        if not os.path.exists(path):
            os.mkdir(path)

    def removedirs(sef, path):
        '''
        递归删除文件夹

        Args:
            path: 目录路径
        '''
        if os.path.exists(path):
            os.removedirs(path)

    def get_time(self):
        '''
        获取当前时间并返回
        '''
        timestamp = time.time()
        time_local = time.localtime(timestamp)
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return datetime