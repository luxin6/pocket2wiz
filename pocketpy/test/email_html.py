# -*- coding: utf-8 -*-
'''
send email via gmail,support html email

'''
import smtplib
import urllib2

def crawler(url):
    response = urllib2.urlopen(url)
    html = response.read()
    print '============================================================'
    return html

html=crawler("http://www.baidu.com")
msg ="""From: From pocket<pocket2wiz@gmail.com>
To: mywiz <luxin6@mywiz.cn>
MIME-Version: 1.0
Content-type: text/html
Subject: pocket2wiz SMTP HTML e-mail test

This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
<h2><a href="http://www.ueseo.org">优异搜索</a></h2>
"""+html
#msg =
"""From: From pocket<pocket2wiz@gmail.com>
To: mywiz <luxin6@mywiz.cn>
MIME-Version: 1.0
Content-type: text/html
Subject: pocket2wiz SMTP HTML e-mail test

This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
<h2><a href="http://www.ueseo.org">优异搜索</a></h2>
"""


server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
#server = smtplib.SMTP('smtp.126.com',465) #port 465 or 587
server.ehlo()
server.starttls()
server.ehlo()
#server.login('pocket2wiz','luxin0987654321')#请替换成您的email和密码
server.sendmail('luxin6@mywiz.cn','luxin6@qq.com',msg)
#todo : @mywiz.cn can not receive the email....
server.close()

