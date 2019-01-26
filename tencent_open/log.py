# -*- coding: utf-8 -*-
'''
日志模块

Author: Michael
Date: 2019-01-14
Language: 3.7.2
'''

import os
import logging
from common import Common
from email_send import Email

# 当前脚本目录
cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'

# 默认日志保存路径
log_path = cur_path + 'logs/'

common = Common()
el = Email()


class Log:
    '''
    日志类

    Attribute:
        logpath: 日志保存路径
    '''

    def __init__(self, logpath=log_path):
        common.mkdir(logpath)
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
            logname = common.get_time('%Y%m')

        # 文件路径
        logname = self.logpath + str(logname) + '.log'

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

        # 记录日志之后移除句柄
        logger.removeHandler(fh)
        logger.removeHandler(sh)

        # 每天只发一封首次报错日志邮件
        if loglevel >= 3:
            yaml = common.get_yaml('', 'flag')
            log_date = yaml['log_date']
            cur_date = common.get_day()
            if log_date != cur_date:
                common.edit_yaml('log_date', cur_date, 'flag')
                el.send_email(logtext)


if __name__ == '__main__':
    log = Log()
    log.write_log('test')
