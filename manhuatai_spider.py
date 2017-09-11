# _*_ coding: utf-8 _*_
'''
爬取漫画台的漫画图片,需手动配置参数:self.img_src

Author: Insomnia
Version: 0.0.1
Date: 2017-09-08
Language: Python3.6.2
Editor: Sublime Text3
'''

import requests, os, re, time
from bs4 import BeautifulSoup
from urllib import parse

# 当前项目路径
cur_path = os.getcwd() + '/'

class ManHuaTai(object):
    '''
    本类主要用于爬取漫画台的漫画图片

    Attributes:
        url: 爬虫目标
        img_src: [需手动配置的参数]
            url: 漫画图片源地址,在filebug上找 第一张漫画的图片链接[方便下面的正则判断] 即可，可以凭这一张漫画图片链接爬取整部漫画
            zero: 考虑有时该部漫画前9话加0的情况, True表示前9话不需加0，eg:第01话
            num: 第几话开始爬虫，不设置该参数，默认第1话开始
        img_special: [需手动配置的参数]图片名后缀特殊字符,GQ代表高清版，SM代表抢先版(持续关注抢先版后面是否会换成普通版，http://www.manhuatai.com/doupocangqiong/621.html)
    '''

    def __init__(self):
        self.url = 'http://www.manhuatai.com/'
        self.img_src = {
            # '逆转木兰辞' : {'url': 'http://mhpic.zymkcdn.com/comic/N%2F%E9%80%86%E8%BD%AC%E6%9C%A8%E5%85%B0%E8%BE%9E%2F15%E8%AF%9DGQ%2F1.jpg-mht.middle', 'zero': True, 'num': 6},

            # '砂与海之歌': {'url': 'http://mhpic.zymkcdn.com/comic/S%2F%E7%A0%82%E4%B8%8E%E6%B5%B7%E4%B9%8B%E6%AD%8C%2F53%E8%AF%9DSM%2F1.jpg-mht.middle', 'zero': True},

            # 已完结
            '勇者的心' : {'url': 'http://mhpic.zymkcdn.com/comic/Y%2F%E5%8B%87%E8%80%85%E7%9A%84%E5%BF%83%2F1%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False}

            # '斗破苍穹': {'url': 'http://mhpic.zymkcdn.com/comic/D%2F%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9%2F619%E8%AF%9DSM%2F1.jpg-mht.middle', 'zero': False, 'num': '619'},

            # 已连载至25话
            # '天降系拍档': {'url': 'http://mhpic.zymkcdn.com/comic/T%2F%E5%A4%A9%E9%99%8D%E7%B3%BB%E6%8B%8D%E6%A1%A3%2F2%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False},

            # 已连载至72话
            # '勇者是女孩': {'url': 'http://mhpic.zymkcdn.com/comic/Y%2F%E5%8B%87%E8%80%85%E6%98%AF%E5%A5%B3%E5%AD%A9%2F70%E8%AF%9D%2F1.jpg-mht.middle', 'zero': False}
        }
        # self.img_special = ('', 'GQ', 'SM')
        self.img_special = ('', 'GQ')

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

    def download_img(self, img_obj, img_path_first):
        '''
        下载漫画图片

        Args:
            img_obj: 漫画参数，dict类型
            img_path_first: 漫画路径
        '''
        img_src = img_obj['url']
        img_zero = img_obj['zero']

        # 第几话，默认从第1话开始
        if 'num' in img_obj:
            num = int(img_obj['num'])
        else: 
            num = 1

        # 根据图片地址规律，获取图片前缀、图片名、后缀
        regex = re.compile(r'^(http://mhpic.zymkcdn.com/comic/)(.+)\d{1,3}(.jpg-mht.middle)$')
        img_group = re.match(regex, img_src)
        img_prefix, img_name, img_postfix = (img_group.group(1), parse.unquote_plus(img_group.group(2)), img_group.group(3))
        if img_name == '':
            print('这部漫画的url解码失败：%s' % img_src)
            return False

        # 根据图片名规律，获取图片名前缀、数字后面字符、漫画是否高清标志
        regex_name = re.compile(r'^(\w+/\w+/)\d+(\w+?)(GQ)?/$')
        img_name_group = re.match(regex_name, img_name)
        img_name_prefix, img_name_postfix = (img_name_group.group(1), img_name_group.group(2))

        # 遍历下载该部漫画的所有图片
        while num:
            # 创建第几话文件夹,若文件夹已存在则表示之前已下载，不重复下载
            img_path = img_path_first + '/第' + str(num) + '话'
            # print(num, img_path)
            self.mkdir(img_path)

            # 考虑有时该部漫画前9话加0的情况
            cur_num = num
            if num < 10 and img_zero:
                cur_num = '0%s' % num # 这里cur_num为string类型

            # 下载第num话的漫画图片,由于图片有分高清版和普通版，访问链接不同，故直接访问两次，暴力判断是否一定不存在这个i图片
            i = 1 # 第几张漫画图片，从1开始
            while i:
                cur_img_path = img_path + '/' + str(i) + '.jpg'
                if not os.path.exists(cur_img_path):
                    cur_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
                    flag = True
                    j = 2
                    while j:
                        for s in self.img_special:
                            cur_img_src = img_prefix + parse.quote_plus(img_name_prefix + str(cur_num) + img_name_postfix + s + '/') + str(i) + img_postfix
                            print('cur_img_src', cur_img_src)
                            cur_request = requests.get(cur_img_src, headers=cur_headers)
                            cur_img_content = cur_request.content

                            # 正则匹配返回值是否是error
                            regex = re.compile(r'^{"error"')
                            if re.match(regex, cur_request.text):
                                continue
                            else:
                                with open(cur_img_path, 'wb') as f:
                                    f.write(cur_img_content)
                                flag = False
                                break

                        # 第2话和第02话这种url参数有时会随机出现，故需加一层遍历判断，如逆转木兰辞第1话和第5话
                        if img_zero and flag:
                            cur_num = num # cur_num 重新赋值为int类型
                            j -= 1
                        else:
                            break

                    if flag:
                        break
                i += 1

            # i等于1时，表示该部漫画已经爬取结束
            if i == 1:
                self.removedirs(img_path)
                break
            else:
                num += 1
                time.sleep(0.3) # 睡眠，防止ip被封

    def start(self, platform='manhuatai'): 
        '''
        爬虫入口

        Agrs:
            platform: 平台名，用于创建存放图片的第一个文件夹
        '''
        # 创建漫画平台文件夹
        img_path = cur_path + platform
        self.mkdir(img_path)

        begin_time = self.get_time()
        print('-'*60, '爬虫开始: %s' % begin_time, '-'*60, sep="\n")

        # 遍历爬取多部漫画
        for cartoon in self.img_src:
            print('正在爬取漫画：%s ...' % cartoon)
            # 创建动漫名文件夹
            cur_img_path = img_path + '/' + cartoon
            self.mkdir(cur_img_path)
            self.download_img(self.img_src[cartoon], cur_img_path)
            time.sleep(60) # 睡眠60s，防止ip被封
            print('报告主人，%s : 爬好了，我休息一会...' % cartoon)

        print('-'*60, '爬虫结束 %s ~ %s' % (begin_time, self.get_time()), '-'*60, sep="\n")

if __name__ == '__main__':
    ManHuaTai = ManHuaTai()
    ManHuaTai.start()