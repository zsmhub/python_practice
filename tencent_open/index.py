# -*- coding: UTF-8 -*-
'''
腾讯开放平台模拟登录并获取对账结算数据

Author: Michael
Date: 2019-01-10
Language: 3.7.2
'''

from selenium import webdriver
from bs4 import BeautifulSoup
from common import Common
from log import Log
from mysql import Mysql
from multiprocessing import Pool
import pickle5 as pickle
import requests
import time
import re
import os
import json
import sys

# 通用函数接口
common = Common()

# 日志接口
log = Log()

# mysql接口
mysql = Mysql()

# 当前脚本目录
cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'

# User Agent
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

# http请求头
headers = {'User-Agent': UA}


class TencentOpen(object):
    '''
    本类主要用于获取腾讯开放平台对账数据

    Attribute:
        __session: 建立会话
        __cookies: 保存cookies
        username: 用户名
        pwd: 用户密码
        company: 公司名
    '''

    def __init__(self, username, pwd, company):
        self.__session = requests.Session()
        self.__cookies = ''
        self.username = username
        self.pwd = pwd
        self.company = company

    def login(self):
        '''
        模拟登录

        Returns:
            返回bool
        '''
        log.write_log('账号%s|正在登录...' % self.username, logname=self.username)
        username = self.username
        pwd = self.pwd
        # cookies保存路径
        cookies_dir = cur_path + 'cookies/'
        common.mkdir(cookies_dir)
        cookies_path = cookies_dir + 'cookies_%s.pkl' % username

        try:
            with open(cookies_path, 'rb') as f:
                self.__cookies = pickle.load(f)
                return True
        except:
            # 模拟浏览器路径
            chrome_path = common.get_yaml('chrome_path')

            # 登录界面url
            url_login = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?s_url=http://op.open.qq.com/manage_centerv2/'

            # 打开模拟浏览器
            wd = webdriver.Chrome(executable_path=chrome_path)

            # 输入账号密码并登陆
            wd.get(url_login)
            wd.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
            time.sleep(1)  # 设定1秒睡眠
            wd.find_element_by_xpath('//*[@id="u"]').send_keys(username)
            wd.find_element_by_xpath('//*[@id="p"]').send_keys(pwd)
            wd.find_element_by_xpath('//*[@id="login_button"]').click()
            time.sleep(20)  # 设定睡眠时间，方便手动处理可能出现的验证码

            # 请求链接添加并保存cookies
            cookies = wd.get_cookies()
            if cookies:
                with open(cookies_path, 'wb') as f:
                    pickle.dump(cookies, f)
                    self.__cookies = cookies
                wd.quit()  # 关闭浏览器
                return True
            else:
                log.write_log(
                    '账号%s|登录失败' % self.username,
                    logname=self.username,
                    loglevel=4)
                return False

    def get_session(self):
        '''
        返回请求会话对象

        Returns:
            返回会话对象
        '''
        s = self.__session
        for cookie in self.__cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        s.headers.clear()  # 删除原始 session 里面标记有python机器人的信息
        return s

    def crawl_android_latest(self):
        '''
        获取已上线最新10款应用信息

        Returns:
            返回list或False
        '''
        log.write_log(
            '账号%s|正在获取已上线最新10款应用信息...' % self.username, logname=self.username)

        # 安卓应用页面
        url_android = 'http://op.open.qq.com/manage_centerv2/'

        try:
            session = self.get_session()
            req = session.get(url_android, headers=headers)
            if req.status_code != 200:
                log.write_log(
                    '账号%s|请求失败: %s' % (self.username, req.text),
                    logname=self.username,
                    loglevel=4)
                return False

            soup = BeautifulSoup(req.content, 'html.parser')
            regex = re.compile('var G_DATA={"online":(.*?),"develop":')
            match_obj = re.search(regex, soup.get_text())
            if match_obj is None:
                log.write_log(
                    '账号%s|爬取游戏应用信息失败' % self.username,
                    logname=self.username,
                    loglevel=4)
                return False
            app_str = match_obj.groups()[0]
            app_list = json.loads(app_str)  # 字符串转为json

            return app_list
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log(
                '账号%s|%s|Exception: %s' % (self.username, cur_func, str(e)),
                logname=self.username,
                loglevel=3)
            return False

    def crawl_app_android(self):
        '''
        获取该账户的所有安卓应用

        Returns:
            返回list或False
        '''
        ret = self.crawl_android_latest()
        if not ret:
            return False

        log.write_log(
            '账号%s|正在获取该账户所有安卓应用...' % self.username, logname=self.username)

        add_time = common.get_day()
        new_app = []  # 存放新上线的安卓应用

        try:
            # 获取已有的安卓应用
            sql = '''
                SELECT
                    appid, app_alias
                FROM tenxun_android
                WHERE company = '%s'
            ''' % self.company
            all_app = mysql.select(sql)
            all_app = list(all_app)
            appids = [x[0] for x in all_app]

            for i in ret:
                appid = str(i['appid'])
                app_alias = i['app_alias']
                if appid not in appids:
                    new_app.append([self.company, appid, app_alias, add_time])
                    all_app.append((appid, app_alias))

            # 将新上线的安卓应用保存到数据库中
            if len(new_app) != 0:
                sql = '''
                    INSERT INTO tenxun_android(
                        company,
                        appid,
                        app_alias,
                        add_time
                    )
                    VALUES(%s, %s, %s, %s)
                '''
                mysql.insert_batch(sql, new_app)

            return all_app
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log(
                '账号%s|%s|Exception: %s' % (self.username, cur_func, str(e)),
                logname=self.username,
                loglevel=3)
            return False

    def crawl_yyb(self, begin_date, end_date, appid, app_alias):
        '''
        获取对账数据

        Args:
            begin_date: 开始日期
            end_date: 结束日期
            appid: 游戏应用id
        Returns:
            返回list或False
        '''
        log.write_log(
            '账号%s|正在获取对账数据|%s...' % (self.username, app_alias),
            logname=self.username)

        add_time = common.get_day()
        yyb = []  # 存放结账数据
        url_yyb = 'https://midas.qq.com/v3/yyb/Account/%s/1' % appid
        form_data = {
            'txtStartDate': begin_date,
            'txtEndDate': end_date,
            'offerStatus': 1,
        }
        try:
            session = self.get_session()

            req = session.post(url_yyb, headers=headers, data=form_data)
            if req.status_code != 200:
                log.write_log(
                    '账号%s|请求失败: %s' % (self.username, req.text),
                    logname=self.username,
                    loglevel=4)
                return False

            # 爬所需数据
            soup = BeautifulSoup(req.content, 'html.parser')
            items = soup.find('div', class_='numb_table')
            if items is None:
                error = soup.find('div', id='prillege').find('h5').get_text()
                log.write_log(
                    '账号%s|游戏%s|出现错误：%s' % (self.username, app_alias, error),
                    logname=self.username,
                    loglevel=4)
                return False

            items = items.find('tbody')
            for i in items.find_all('tr'):
                tds = i.find_all('td')
                tds = list(map(lambda x: x.get_text(), tds))
                yyb.append([
                    self.company,  # company
                    app_alias,  # app_alias
                    tds[0],  # date
                    tds[1],  # amount
                    add_time  # add_time
                ])

            # 写入数据库
            if len(yyb) != 0:
                sql = '''
                    INSERT INTO tenxun_yyb(
                        company,
                        app_alias,
                        date,
                        amount,
                        add_time
                    )
                    VALUES(%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        amount=VALUES(amount),
                        add_time=VALUES(add_time)
                '''
                mysql.insert_batch(sql, yyb)

            return True
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log(
                '账号%s|%s|Exception: %s' % (self.username, cur_func, str(e)),
                logname=self.username,
                loglevel=3)
            return False

    def crawl_cbs(self, begin_month, end_month, appid, app_alias):
        '''
        获取结算数据

        Args:
            begin_month: 开始月份
            end_month: 结束月份
            appid: 游戏应用id
        Returns:
            返回list或False
        '''
        log.write_log(
            '账号%s|正在获取结算数据|%s...' % (self.username, app_alias),
            logname=self.username)

        add_time = common.get_day()
        cbs = []  # 存放新增的结算数据
        url_cbs = 'https://midas.qq.com/v3/cbs/searchByBtn/%s/1/%s/%s/-1' % (
            appid,
            begin_month,
            end_month,
        )
        try:
            # 获取数据库一年内已获取的结算单号
            sql = '''
                SELECT
                    number
                FROM tenxun_cbs
                WHERE
                    app_alias = '%s'
                    AND month BETWEEN '%s' AND '%s'
            ''' % (app_alias, begin_month, end_month)
            select = mysql.select(sql)
            numbers = [x[0] for x in select]
            numbers_new = []

            session = self.get_session()

            req = session.get(url_cbs, headers=headers)
            if req.status_code != 200:
                log.write_log(
                    '账号%s|请求失败: %s' % (self.username, req.text),
                    logname=self.username,
                    loglevel=4)
                return False

            # 爬所需数据
            soup = BeautifulSoup(req.content, 'html.parser')
            items = soup.find('div', class_='numb_table')
            if items is None:
                error = soup.find('div', id='prillege').find('h5').get_text()
                log.write_log(
                    '账号%s|游戏%s|出现错误：%s' % (self.username, app_alias, error),
                    logname=self.username,
                    loglevel=4)
                return False

            items = items.find('tbody')
            for i in items.find_all('tr'):
                tds = i.find_all('td')
                tds = list(map(lambda x: x.get_text(), tds))
                service_fee = tds[4].replace("\r\n", '').strip()
                row = [
                    self.company,  # company
                    app_alias,  # app_alias
                    add_time,  # add_time
                    tds[0] + '-01',  # month
                    tds[1].replace("\n", ""),  # number
                    tds[2].replace(',', ''),  # init_income
                    tds[3].replace(',', ''),  # settle_income
                    service_fee.replace(',', ''),  # service_fee
                    tds[5].replace("\r\n", "").strip(),  # settle_status
                    '正常'
                ]
                number = row[4]
                if number not in numbers:
                    cbs.append(row)

                numbers_new.append(number)

            # 被腾讯删除的结算单号
            delete = list(set(numbers).difference(set(numbers_new)))

            # 写入数据库
            if len(cbs) != 0:
                sql = '''
                    INSERT INTO tenxun_cbs(
                        company,
                        app_alias,
                        add_time,
                        month,
                        number,
                        init_income,
                        settle_income,
                        service_fee,
                        settle_status,
                        is_del
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                mysql.insert_batch(sql, cbs)
            if len(delete) != 0:
                sql = '''
                    UPDATE tenxun_cbs
                    SET is_del='删除', add_time='%s'
                    WHERE number in ('%s')
                ''' % (add_time, "','".join(delete))
                mysql.execute(sql)

            return True
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            log.write_log(
                '账号%s|%s|Exception: %s' % (self.username, cur_func, str(e)),
                logname=self.username,
                loglevel=3)
            return False

    def index(self):
        '''
        自动爬虫入口，每天跑数

        Returns:
            返回None
        '''
        log.write_log(
            '账号%s|正在进入自动爬虫入口...' % self.username, logname=self.username)

        yesterday = common.get_day(-1)
        cur_month = common.get_day(0, '%Y-%m')

        # 对账默认跑昨天的数据
        begin_date = yesterday  # 对账开始日期
        end_date = begin_date  # 对账结束如期

        # 结算默认跑一年内的数据
        begin_month = common.get_day(-365, '%Y-%m')  # 结算开始月份
        end_month = cur_month  # 结算结束月份

        ret = self.login()
        if not ret:
            log.write_log(
                '账号%s|登录失败...' % self.username, logname=self.username)
            return

        app_list = self.crawl_app_android()
        if not app_list:
            log.write_log(
                '账号%s|没有安卓应用...' % self.username, logname=self.username)
            return

        for app in app_list:
            appid = app[0]
            app_alias = app[1]
            self.crawl_yyb(begin_date, end_date, appid, app_alias)
            self.crawl_cbs(begin_month, end_month, appid, app_alias)

    def manual(self, begin_date, begin_month, app_name=''):
        '''
        人工爬虫入口，比如添加新客户时需重跑到很久之前的数据

        Args:
            begin_date: 对账开始日期
            begin_month: 结算开始月份
            app_name: 需跑数应用名称，多款应用使用英文逗号分隔
        Returns:
            返回None
        '''
        log.write_log(
            '账号%s|正在进入人工爬虫入口...' % self.username, logname=self.username)

        end_date = common.get_day(-1)
        end_month = common.get_day(0, '%Y-%m')

        ret = self.login()
        if not ret:
            log.write_log(
                '账号%s|登录失败...' % self.username,
                logname=self.username,
                loglevel=4)
            return

        app_list = self.crawl_app_android()
        if not app_list:
            return

        if app_name != '':
            app_name_list = app_name.split(',')

        for app in app_list:
            appid = app[0]
            app_alias = app[1]
            if app_name != '' and app_alias not in app_name_list:
                continue
            self.crawl_yyb(begin_date, end_date, appid, app_alias)
            self.crawl_cbs(begin_month, end_month, appid, app_alias)

    def update_cookie(self):
        '''
        循环更新cookie

        Returns:
            返回None
        '''
        log.write_log(
            '正在进入循环更新cookie入口|%s...' % self.username, logname=self.username)

        ret = self.login()
        if not ret:
            log.write_log(
                '登录失败|%s...' % self.username,
                logname=self.username,
                loglevel=4)
            return

        ret = self.crawl_android_latest()
        log.write_log(
            '账号%s|cookie更新结束|应用数量: %s...' % (self.username, len(ret)),
            logname=self.username)


if __name__ == '__main__':
    # 腾讯开放平台需爬虫账号
    accounts = common.get_yaml('accounts')

    argv = sys.argv
    if len(argv) == 2 and argv[1] == 'manual':
        log.write_log('腾讯开放平台爬虫开始...')
        account = input('请输入需爬虫的腾讯开放平台账号: ')

        begin_date = input('请输入爬虫对账开始日期: ')
        while not common.is_valid_date(begin_date):
            begin_date = input('请输入正确的对账开始日期: ')

        begin_month = input('请输入爬虫结算开始月份: ')
        while not common.is_valid_date(begin_month + '-01'):
            begin_month = input('请输入正确的结算开始月份: ')

        app_name = input('请输入指定跑数的安卓应用(为空则跑全部安卓应用): ')

        # 单进程跑1个账号的数据
        for item, value in accounts.items():
            u = str(value['username'])

            if u != account:
                continue

            pwd = value['password']
            tx = TencentOpen(u, pwd, item)
            tx.manual(begin_date, begin_month, app_name)
        log.write_log('腾讯开放平台爬虫结束...')
    elif len(argv) == 2 and argv[1] == 'update_cookie':
        log.write_log('腾讯开放平台update cookie开始...')
        # 多进程更新多个cookie
        num = len(accounts)
        p = Pool(num)
        for item, value in accounts.items():
            u = value['username']
            pwd = value['password']
            tx = TencentOpen(u, pwd, item)
            p.apply_async(tx.update_cookie)
        p.close()
        p.join()
        log.write_log('腾讯开放平台update cookie结束...')
    else:
        log.write_log('腾讯开放平台爬虫开始...')
        # 多进程跑多个账号的数据
        num = len(accounts)
        p = Pool(num)
        for item, value in accounts.items():
            u = value['username']
            pwd = value['password']
            tx = TencentOpen(u, pwd, item)
            p.apply_async(tx.index)
            time.sleep(10)  # 解决多进程同时打开多个chromedriver时失败的问题
        p.close()
        p.join()
        log.write_log('腾讯开放平台爬虫结束...')
