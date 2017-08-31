# python_practice
廖雪峰老师的练习题

<pre>
#列表生成式
L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s, str)]   # 先for循环，再if筛选，再s.lower
print("L2:", L2) # 输出: ['hello', 'world', 'apple']
L3 = [s.lower() if isinstance(s, str) else s for s in L1]   # 先for循环，再if筛选（True则s.lower，False则返回s）
print("L3:", L3) # 输出: ['hello', 'world', 18, 'apple', None]

#生成器-杨辉三角
def triangles():
    L=[1]
    while True:
        yield L
        L = [1] + [ L[x-1] + L[x] for x in range(1,len(L)) ] + [1] # +号用于组合列表

i = 0
for x in triangles():
    print(x)
    i += 1
    if i == 10:
        break

#@property:请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution
class Screen(object):
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, value):
        # 宽度值判断
        if not isinstance(value, (int,float)):
            raise ValueError('width must be an integer or float!')
        if value < 0:
            raise ValueError('width must > 0')
        self._width = value

    @height.setter
    def height(self, value):
        # 高度值判断
        if not isinstance(value, (int, float)):
            raise ValueError('height must be an integer or float!')
        if value < 0:
            raise ValueError('height must > 0')
        self._height = value

    @property
    def resolution(self):
        return self._width * self._height

s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution

#假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，均是str，请编写一个函数将其转换为timestamp：
import re
from datetime import datetime, timezone, timedelta

def to_timestamp(dt_str, tz_str):
    time_zone = re.match(r'^UTC([+|-]\d{1,2}):00$', tz_str).group(1)
    time = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')\
        .replace(tzinfo=timezone(timedelta(hours=int(time_zone))))\
        .timestamp()
    return time

t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('Pass')

#请写一个能处理去掉=的base64解码函数：
import base64

def safe_base64_decode(s):
    slen = len(s)
    if slen == 0:
        return s
    num = slen % 4
    return base64.b64decode(s + b'=' * (4 - num) if num >0 else s)

assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('Pass')

#使用qq邮箱发送邮件
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = '你的qq邮箱'
password = '你的授权码'
to_addr = '收件邮箱'
smtp_server = 'smtp.qq.com'

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

server = smtplib.SMTP_SSL(smtp_server, 465)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
</pre>