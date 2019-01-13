# -*- coding: utf-8 -*-
'''
mysql数据库连接
'''

import pymysql

host = '数据库IP'
username = '数据库账号'
password = '数据库密码'
database = '数据库名'

# 打开数据库连接
db = pymysql.connect(host, username, password, database)

# 创建游标对象
cursor = db.cursor()

try:
    # 执行sql语句
    cursor.execute('SELECT VERSION()')

    # 获取单条数据
    data = cursor.fetchone()

    print('Database version: %s' % data)

    db.commit()
except:
    db.rollback()
finally:
    db.close()
