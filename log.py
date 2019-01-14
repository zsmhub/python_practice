'''
日志系统

Author: Michael
Date: 2019-01-14
Language: 3.7.1
'''

import logging
import os
import time

# 当前项目路径
cur_path = os.getcwd() + '/'

# 默认日志保存路径
log_path = cur_path + 'logs/'


class Log:
    '''
    日志类

    Attribute:
        logpath: 日志保存路径
    '''

    def __init__(self, logpath=log_path):
        self.mkdir(logpath)
        self.logpath = logpath

    def write_log(self, logtext, *, logname='', loglevel=2):
        '''
        写日志

        Args:
            logtext: 日志内容
            logname: 日志文件名称，默认以年月作为文件名
            loglevel: 日志级别
        '''
        # 日志文件名判断
        if logname == '':
            logname = self.get_time('%Y%m')

        # 文件路径
        logname = self.logpath + logname + '.log'

        # 创建一个logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname, mode='a', encoding='UTF-8')

        # 再创建一个handler，用于输出到控制台
        sh = logging.StreamHandler()

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(sh)

        # 根据日志级别输出日志
        if loglevel == 1:
            logger.debug(logtext)
        elif loglevel == 3:
            logger.warning(logtext)
        elif loglevel == 4:
            logger.error(logtext)
        elif loglevel == 5:
            logger.critical(logtext)
        else:
            logger.info(logtext)

    def mkdir(self, path):
        '''
        创建文件夹

        Args:
            path: 目录路径
        '''
        if not os.path.exists(path):
            os.mkdir(path)

    def get_time(self, format="%Y-%m-%d %H:%M:%S"):
        '''
        返回当前时间点

        Args:
            format: 日期格式化方式
        '''
        timestamp = time.time()
        time_local = time.localtime(timestamp)
        datetime = time.strftime(format, time_local)
        return datetime


if __name__ == '__main__':
    log = Log()
    log.write_log('test')
