# -*- coding: utf-8 -*-
'''
mysql模块

Author: Michael
Date: 2019-01-19
Language: 3.7.2
'''

import sys
import pymysql
from common import Common
from log import Log

common = Common()
log = Log()


class Mysql(object):
    '''
    mysql常用操作方法类

    Attribute:
        active: 调用数据库配置名
        host: 数据库IP
        ue: 数据库用户名
        pwd: 数据库密码
        database: 数据库名
    '''

    def __init__(self, active='db'):
        cfg = common.get_yaml(active)
        self.host = cfg['hostname']
        self.ue = cfg['username']
        self.pwd = cfg['password']
        self.database = cfg['database']

    def insert_batch(self, sql, data):
        '''
        批量插入

        Args:
            sql: 执行sql语句
            data: 插入数据
        Returns:
            返回None
        '''
        db = pymysql.connect(self.host, self.ue, self.pwd, self.database)
        cursor = db.cursor()
        try:
            cursor.executemany(sql, data)
            db.commit()
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log('Exception|%s: %s' % (cur_func, str(e)), loglevel=3)
            db.rollback()
        finally:
            db.close()

    def select(self, sql):
        '''
        查询操作

        Args:
            sql: 执行sql语句
        Returns:
            返回list或None
        '''
        db = pymysql.connect(self.host, self.ue, self.pwd, self.database)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            ret = cursor.fetchall()
            return ret
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log('Exception|%s: %s' % (cur_func, str(e)), loglevel=3)
            db.rollback()
        finally:
            db.close()

    def execute(self, sql):
        '''
        插入、更新或删除等执行操作

        Args:
            sql: 执行sql语句
        Returns:
            返回None
        '''
        db = pymysql.connect(self.host, self.ue, self.pwd, self.database)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log('Exception|%s: %s' % (cur_func, str(e)), loglevel=3)
            db.rollback()
        finally:
            db.close()
