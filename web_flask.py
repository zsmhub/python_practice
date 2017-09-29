# -*- coding: utf-8 -*-
'''
使用Flask框架编写简单web页面

Author: Insomnia
Version: 0.0.1
Date: 2017-09-29
Language: Python3.6.2
Editor: Sublime Text3
'''

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    # docker容器运行时，需加上host='0.0.0.0'，否则运行失败
    app.run(debug = False, host='0.0.0.0')