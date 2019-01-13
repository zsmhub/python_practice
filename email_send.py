# -*- coding: utf-8 -*-
'''
使用qq邮箱发送邮件
'''

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    '''
    收发件人地址格式化
    '''
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


from_addr = '你的qq邮箱'
password = '你的授权码'
to_addr = '收件邮箱'
smtp_server = 'smtp.qq.com'
smtp_port = 465

msg = MIMEText('hello, send by Python开发者...', 'plain', 'utf-8')
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

server = smtplib.SMTP_SSL(smtp_server, smtp_port)
# server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
