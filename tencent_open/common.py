# -*- coding: utf-8 -*-
'''
通用函数模块

Author: Michael
Date: 2019-01-14
Language: 3.7.2
'''

import os
import time
import datetime
import yaml
import shutil

# 当前脚本目录
cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'

# 配置文件目录
yaml_path = cur_path + 'yaml/'


class Common(object):
    '''
    通用方法类
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

    def removedirs(self, path):
        '''
        递归删除文件夹

        Args:
            path: 目录路径
        '''
        if os.path.exists(path):
            # os.removedirs(path)  # 递归删除空文件夹
            shutil.rmtree(path)  # 递归删除非空文件夹

    def get_time(self, format="%Y-%m-%d %H:%M:%S"):
        '''
        返回当前时间点

        Args:
            format: 日期格式化方式
        Returns:
            返回日
        '''
        timestamp = time.time()
        time_local = time.localtime(timestamp)
        return time.strftime(format, time_local)

    def get_timestamp(self, time_input='', format='%Y-%m-%d'):
        '''
        获取当前时间戳或日期转为时间戳

        Args:
            time_input: 需转换为时间戳的时间
            format: time变量的时间格式
        Returns:
            返回时间戳
        '''
        if time_input == '':
            return time.time()
        ts = time.strptime(time_input, format)
        return time.mktime(ts)

    def get_day(self, days=0, format='%Y-%m-%d'):
        '''
        获取相比当前日期间隔时间差的某一天日期，如今天、昨天、明天

        Args:
            days: 间隔天数
            format: 返回的日期格式
        Returns:
            返回日期
        '''
        today = datetime.date.today()
        diff_day = datetime.timedelta(days=days)
        ret = str(today + diff_day)
        if format == '%Y-%m':
            return ret[:7]
        elif format == '%Y':
            return ret[:4]
        return ret

    def is_valid_date(self, date):
        '''
        判断字符串日期是否有效

        Args:
            date: 字符串日期
        Returns:
            返回bool
        '''
        try:
            if ':' in date:
                time.strptime(date, '%Y-%m-%d %H:%M:%S')
            else:
                time.strptime(date, '%Y-%m-%d')
            return True
        except:
            return False

    def get_yaml(self, key='', p='config'):
        '''
        获取配置参数

        Args:
            key: 获取参数key值
        Returns:
            返回dict或string
        '''
        config_path = yaml_path + p + '.yaml'
        with open(config_path, 'r') as f:
            cfg = yaml.load(f)
            if key != '':
                return cfg[key]
            return cfg

    def edit_yaml(self, k='', v='', p='config'):
        '''
        编辑配置参数
        '''
        config_path = yaml_path + p + '.yaml'
        cfg = self.get_yaml('', p)
        cfg[k] = v
        with open(config_path, 'w') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)


if __name__ == "__main__":
    co = Common()
    pass
