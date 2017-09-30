# -*- coding: utf-8 -*-
'''
实现多线程爬取漫画台漫画(漫画台的部分漫画来源是知音漫客)
主线程: 从响应队列中取出响应信息
工作线程: 从任务队列中获取任务，并生成响应信息放入响应队列

Author: Insomnia
Version: 0.0.1
Date: 2017-09-30
Language: Python3.6.2
Editor: Sublime Text3
'''

import os, time
from threading import Thread
from queue import Queue
from crawl import Crawl
from common import Common

# 任务队列， 从主线程到工作线程
task_queue = Queue(maxsize=100000)

# 响应队列， 从工作线程到主线程
response_queue = Queue()

# 爬虫接口
crawl = Crawl()

# 通用函数接口
common = Common()

# 工作线程的数量
threads_numbers = 20

# 当前项目路径
cur_path = os.getcwd() + '/'

# 爬虫目标
img_src = {
    # _*_ 未完结系列 _*_
    # 已连载至622话
    # '斗破苍穹': {'url': 'http://mhpic.zymkcdn.com/comic/D%2F%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9%2F619%E8%AF%9DSM%2F1.jpg-mht.middle', 'zero': False, 'num': '619'},

    # 已连载至15话
    # '逆转木兰辞' : {'url': 'http://mhpic.zymkcdn.com/comic/N%2F%E9%80%86%E8%BD%AC%E6%9C%A8%E5%85%B0%E8%BE%9E%2F15%E8%AF%9DGQ%2F1.jpg-mht.middle', 'zero': True, 'num': 6},

    # 已连载至52话
    # '砂与海之歌': {'url': 'http://mhpic.zymkcdn.com/comic/S%2F%E7%A0%82%E4%B8%8E%E6%B5%B7%E4%B9%8B%E6%AD%8C%2F01%E8%AF%9D%2F1.jpg-mht.middle', 'zero': True},

    # 已连载至25话
    # '天降系拍档': {'url': 'http://mhpic.zymkcdn.com/comic/T%2F%E5%A4%A9%E9%99%8D%E7%B3%BB%E6%8B%8D%E6%A1%A3%2F2%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False},

    # 已连载至72话
    # '勇者是女孩': {'url': 'http://mhpic.zymkcdn.com/comic/Y%2F%E5%8B%87%E8%80%85%E6%98%AF%E5%A5%B3%E5%AD%A9%2F70%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False},

    # _*_ 已完结系列 _*_
    # 共32话
    # '勇者的心' : {'url': 'http://mhpic.zymkcdn.com/comic/Y%2F%E5%8B%87%E8%80%85%E7%9A%84%E5%BF%83%2F1%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False}

    # 共165话
    # '暴走邻家': {'url': 'http://mhpic.zymkcdn.com/comic/B%2F%E6%9A%B4%E8%B5%B0%E9%82%BB%E5%AE%B6%2F01%E8%AF%9D%2F1.jpg-mht.middle', 'zero': True, 'num': 92},

    # 搞笑、恋爱
    '公子不要啊': {'url': 'http://mhpic.zymkcdn.com/comic/G%2F%E5%85%AC%E5%AD%90%E4%B8%8D%E8%A6%81%E5%95%8A%2F44%E8%AF%9D%2F3.jpg-mht.middle', 'zero': False},

    ## --- 需修改img_special为 self.img_special = ('V')
    # '送快递这件破事儿': {'url': 'http://mhpic.zymkcdn.com/comic/S%2F%E9%80%81%E5%BF%AB%E9%80%92%E8%BF%99%E4%BB%B6%E7%A0%B4%E4%BA%8B%E5%84%BF%2F1%E8%AF%9DV%2F1.jpg-zymk.middle', 'zero': False},

    # 玄幻
    '魁拔': {'url': 'http://mhpic.zymkcdn.com/comic/K%2F%E9%AD%81%E6%8B%94%2F1%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False},
    '猫又': {'url': 'http://mhpic.zymkcdn.com/comic/M%2F%E7%8C%AB%E5%8F%88%2F1%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False},

    # 后宫
    '月华玫瑰杀': {'url': 'http://mhpic.zymkcdn.com/comic/Y%2F%E6%9C%88%E5%8D%8E%E7%8E%AB%E7%91%B0%E6%9D%80%2F1%E8%AF%9DV%2F1.jpg-mht.middle', 'zero': False},

    '土星玩具店': {'url': 'http://mhpic.zymkcdn.com/comic/T%2F%E5%9C%9F%E6%98%9F%E7%8E%A9%E5%85%B7%E5%BA%97%2F1%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False},

    # 修真热血
    '风起苍岚': {'url': 'http://mhpic.zymkcdn.com/comic/F%2F%E9%A3%8E%E8%B5%B7%E8%8B%8D%E5%B2%9A%2F1%E8%AF%9D%2F2.jpg-mht.middle', 'zero': False}
}

# 创建漫画平台文件夹
img_path = crawl.mkdir_platform()

class MasterThread(Thread):
    '''
    主线程

    Attributes:
        ret: 状态信息，用于实时显示爬虫状态
    '''

    def __init__(self):
        Thread.__init__(self)
        self.ret = {
            'success_list': set(), # 成功爬虫的漫画
            'failed_list': set(), # 失败爬虫的漫画
            'crawled_count': 0, # 已爬取数量
            'task_count': 0,  # 任务数量
            'response_count': 0,  # 响应数量
            'success_count': 0,  # 单位时间获取用户信息成功数量
            'failed_count': 0,  # 单位时间获取用户失败数量
            'last_time': 0.0  # 上次刷新时间
        }
        img_key = img_src.keys()
        for key in img_key:
            try:
                task_queue.put_nowait(key)
            except:
                continue
        self.ret['task_count'] = task_queue.qsize()

    def run(self):
        try:
            while self.ret['crawled_count'] != len(img_src):
                response_item = response_queue.get()

                if response_item['state']:
                    self.ret['success_list'].add(response_item['cartoon_key'])
                    self.ret['success_count'] += 1
                else:
                    self.ret['failed_list'].add(response_item['cartoon_key'])
                    self.ret['failed_count'] += 1

                self.ret['crawled_count'] += 1

                # 输出状态信息
                self.log()
        except Exception as e:
            print(e)
        finally:
            print("MasterThread exited.")

    def log(self):
        '''
        输出状态信息
        '''
        curtime = time.time()
        interval = curtime - self.ret['last_time']

        # 每一分钟统计一次
        if interval > 1.0:
            self.ret['last_time'] = curtime
        else:
            return

        # os.system('clear')

        self.ret['task_count'] = task_queue.qsize()
        self.ret['response_count'] = response_queue.qsize()

        print("已获取：\033[30;47m" + str(self.ret['crawled_count']) + "\033[0m部")
        print("成功爬虫的漫画:" + str(self.ret['success_count']) + "部")
        print(self.ret['success_list'])
        print("失败爬虫的漫画:" + str(self.ret['failed_count']) + "部")
        print(self.ret['failed_list'])
        print("任务队列：\033[30;47m%d\033[0m部" % self.ret['task_count'])
        print("响应队列：\033[30;47m%d\033[0m部" % self.ret['response_count'])
        # print("有效：\033[30;47m%.2f\033[0m部/秒" % (self.ret['success_count']/interval))
        # print("无效：\033[30;47m%.2f\033[0m部/秒" % (self.ret['failed_count']/interval))
        # print("并发：\033[30;47m%.2f\033[0m部/秒" % ((self.ret['failed_count']+self.ret['success_count'])/interval))

class WorkerThread(Thread):
    '''
    工作线程
    '''
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            # 从任务队列获取一个漫画key
            try:
                cartoon_key = task_queue.get(block=True, timeout=30)
            except:
                break

            # 下载该部漫画图片
            cartoon = img_src[cartoon_key]
            cartoon['img_path_first'] = img_path + '/' + cartoon_key
            ret = crawl.download_img(cartoon)

            # 响应结果
            response_item = {'state': ret, 'cartoon_key': cartoon_key}

            # 将响应结果放入响应队列
            response_queue.put(response_item)
        print('Worker thread exited')

if __name__ == '__main__':
    print('-'*60, '下载图片中...', '-'*60, sep="\n")
    master_thread = MasterThread()

    worker_list = []
    for i in range(threads_numbers):
        worker_thread = WorkerThread()
        worker_list.append(worker_thread)

    master_thread.start()
    for t in worker_list:
        t.start()

    master_thread.join()
    for t in worker_list:
        t.join()