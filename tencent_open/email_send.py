# -*- coding: utf-8 -*-
'''
邮件模块

Author: Michael
Date: 2019-01-18
Language: 3.7.2
'''

import sys
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from common import Common

common = Common()


class Email(object):
    '''
    邮件类
    '''

    def __init__(self):
        pass

    def _format_addr(self, s):
        '''
        邮件地址格式化

        Args:
            s: 发送地址
        Returns:
            返回格式化地址
        '''
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_email(self, content, *, to='', cc='', sub=''):
        '''
        发送邮件，支持多邮件发送

        Args:
            content: 邮件内容
            to: list类型, 收件人邮箱
            cc: list类型, 抄送人邮箱
            sub: 主题
        Returns:
            返回None
        '''
        # 发件人信息
        cfg = common.get_yaml('addresser')
        addresser = cfg['user']
        password = cfg['password']
        smtp_server = cfg['host']
        smtp_port = cfg['port']

        if to == '':
            to = common.get_yaml('receiver')

        if sub == '':
            sub = common.get_yaml('system_name')

        receiver = to
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header('%s预警' % sub, 'utf-8').encode()
        msg['From'] = self._format_addr('%s <%s>' % (sub, addresser))
        msg['To'] = ','.join(to)
        if cc != '':
            msg['Cc'] = ','.join(cc)
            receiver += cc

        try:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(addresser, password)
            server.sendmail(addresser, receiver, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            cur_func = sys._getframe().f_code.co_name
            print('Exception|%s: %s' % (cur_func, str(e)))
            return False


if __name__ == '__main__':
    el = Email()
    el.send_email('test')
