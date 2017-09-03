# _*_ coding: utf-8 _*_
'''
一个简单的Python爬虫，用于抓取豆瓣Top前100的电影名称

Author: Insomnia
Version：0.0.1
Date: 2017-09-03
Language: Python3.6.2
Editor: Sublime Text3
参考原文地址：https://github.com/Andrew-liu/dou_ban_spider/blob/master/douban_spider.py
'''

import requests, time
from bs4 import BeautifulSoup

class DouBanSpider(object):
    '''
    本类主要用于抓取豆瓣排行榜的电影名称

    Attribute:
        page: 表示当前所处的抓取页面
        url: 爬虫目标链接
        data: 存储处理好的抓取到的电影名称
        _top_num: 用于记录当前的top号码
    '''

    def __init__(self):
        self.page = 1
        self.url = 'https://movie.douban.com/top250?start='
        self.data = []
        self._top_num = 1

    def get_page(self, cur_page):
        '''
        根据当前页码爬取网页HTML

        Args:
            cur_page: 当前所抓取的网站页码

        Returns:
            返回抓取到的整个页面的HTML
        '''
        cur_url = self.url + str((cur_page - 1) * 25)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        }
        html = BeautifulSoup(requests.get(cur_url, headers=headers).text, 'html.parser')
        return html

    def find_title(self, html):
        '''
        通过返回的整个网页HTML，查找并获取电影名称
        '''
        movie_items = html.find('div', class_="article").find_all('span', class_="title")
        for movie in movie_items:
            movie_title = movie.get_text()
            if movie_title.find("/") == -1:
                self.data.append('Top' + str(self._top_num) + ' ' + movie_title)
                self._top_num += 1

    def start_spider(self):
        '''
        爬虫入口，并控制爬虫抓取页面的范围,每页25个电影名称
        '''
        while self.page <= 4:
            html = self.get_page(self.page)
            self.find_title(html)
            self.page += 1

    def get_time(self):
        '''
        获取当前时间并返回
        '''
        timestamp = time.time()
        time_local = time.localtime(timestamp)
        datetime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        return datetime

def main():
    spider = DouBanSpider()
    print('豆瓣电影爬虫开始...', spider.get_time())
    spider.start_spider()
    for title in spider.data:
        print(title)
    print('豆瓣电影爬虫结束...', spider.get_time())

if __name__ == '__main__':
    main()