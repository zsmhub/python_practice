# -*- coding: utf-8 -*-
'''
爬取漫画台或知音漫客的漫画
'''

import requests, os, re, time
from bs4 import BeautifulSoup
from urllib import parse
from common import Common

# 通用函数接口
common = Common()

class Singleton(object):
    '''
    实现单例模式， Crawl在程序中只有一个实例

    Attributes:
        _instance: 唯一实例的引用
    '''
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

class Crawl(Singleton):
    '''
    爬取漫画台或知音漫客的漫画

    Attributes:
        img_special: [需手动配置的参数]图片名后缀特殊字符,GQ代表高清版，SM代表抢先版(持续关注抢先版后面是否会换成普通版，http://www.manhuatai.com/doupocangqiong/621.html)
    '''
    def __init__(self):
        self.img_special = ('', 'GQ')

    def mkdir_platform(self, platform='manhuatai'):
        '''
        创建漫画平台文件夹

        Args:
            platfomr: 平台文件名
        '''
        img_path = os.getcwd() + '/' + platform
        common.mkdir(img_path)
        return img_path

    def download_img(self, img_obj):
        '''
        下载一部漫画的图片

        Args:
            img_obj: 漫画参数，dict类型
        '''
        img_src = img_obj['url']
        img_zero = img_obj['zero']
        img_path_first = img_obj['img_path_first'] # 漫画路径

        # 创建漫画文件夹
        common.mkdir(img_path_first)

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
            common.mkdir(img_path)

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
                            # print('cur_img_src', cur_img_src)
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
                common.removedirs(img_path)
                break
            else:
                num += 1
                time.sleep(0.3) # 睡眠，防止ip被封

        return True