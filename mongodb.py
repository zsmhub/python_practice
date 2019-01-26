# -*- encoding: utf-8 -*-
'''
MongoDB非关系型数据库连接案例

Author: Michael
Date: 2019-01-16
Language: 3.7.2
'''

import pymongo

# 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
client = pymongo.MongoClient("mongodb://root:root@127.0.0.1:27017/")

# 指定数据库
db = client.test

# 指定集合
collection = db.students

# 插入数据
student = {'id': '20190101', 'name': 'Tom3', 'age': 20, 'gender': 'female'}
ret = collection.insert_one(student)
print('insert_id:', ret.inserted_id)

# 更新数据
condition = {'name': 'Tom3'}
edit = {'age': 21}
ret = collection.update_one(condition, {'$set': edit})
print('update:', ret.matched_count, ret.modified_count)

# 查询
info = collection.find_one(condition)
print('select:', info)

# 计数
count = collection.count_documents({})
print('count:', count)

# 删除数据
ret = collection.delete_one(condition)
print('delete:', ret.deleted_count)
