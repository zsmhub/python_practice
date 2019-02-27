# Python爬取腾讯开放平台对账结算数据文档，目的是方便财务人员汇总统计数据

# 每周跑数的3步操作步骤
- 1.在本机上更新腾讯开放平台获取cookies

```sh
python3 /var/www/tencent_open/index.py update_cookie
```

- 2.上传各个客户的cookies文件到服务器上（本机cookies文件存放路径为：当前项目/build/python/cookies/）

```sh
cd /var/www/tencent_open/cookies/
rz -y # 上传本机生成的所有cookies文件
```

- 3.在服务器上执行以下跑数命令，然后等待跑数完毕即可

```sh
python3 /var/www/tencent_open/index.py main
```


# 服务器上需安装python模块包括以下：

```sh
pip3 install beautifulsoup4 pickle5 requests PyYAML pymysql selenium pycrypto
```


# 注意事项
1. 当第一次跑数时，应先整理腾讯开放平台上所有已上线应用的app_alias和appid，导入数据库表tenxun_android【在系统上的安卓应用管理界面可直接导入数据】
