# _*_ coding: utf-8 _*_
# 图片爬虫, 代码参考的原文链接：https://vimerzhao.github.io/2017/07/02/Python%E7%88%AC%E8%99%AB%E5%AE%9E%E6%88%98-%E5%A6%B9%E5%AD%90%E5%9B%BE/#more

import requests
from bs4 import BeautifulSoup
import os

# 爬取目标
url = 'http://www.mzitu.com/page/'
# 当前项目路径
cur_path = os.getcwd() + '/'

# 设置报头,Http协议,增加参数Refer对付防盗链设置
header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36','Referer': "http://www.mzitu.com/"}

# 爬取的预览页面数量
preview_page_cnt = 1

# 循环获取每个预览页面
for cur_page_num in range(1, int(preview_page_cnt)+1):
    cur_url = url + str(cur_page_num)
    cur_page = requests.get(cur_url, headers=header)
    # 解析页面
    soup = BeautifulSoup(cur_page.text, 'html.parser')
    # 图片入口和文字取一个即可
    preview_link_list = soup.find('ul', id='pins').find_all('a', target='_blank')[1::2]
    for link in preview_link_list:
        dir_name = link.get_text().strip()
        # 图片详情链接
        link = link['href']
        soup_next_page = BeautifulSoup(requests.get(link, headers=header).text, 'html.parser')
        # 获取图片数量
        pic_cnt = soup_next_page.find('div', class_='pagenavi').find_all('a')[4].get_text()
        # 创建目录
        pic_path = cur_path + dir_name
        if os.path.exists(pic_path):
            print('directory exist!')
        else:
            os.mkdir(pic_path)
        # 进入目录
        os.chdir(pic_path)
        print('download' + dir_name + '...')
        # 遍历获取每页图片的地址
        for pic_index in range(1, int(pic_cnt)+1):
            pic_link = link + '/' + str(pic_index)
            soup_pic_page = BeautifulSoup(requests.get(pic_link, headers=header).text, 'html.parser')
            # 图片链接
            pic_src = soup_pic_page.find('div', class_='main-image').find('img')['src']
            pic_name = pic_src.split('/')[-1]
            with open(pic_name, 'wb') as f:
                f.write(requests.get(pic_src, headers=header).content)
        os.chdir(cur_path)
print('download end')

