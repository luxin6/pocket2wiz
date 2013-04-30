# -*- coding: utf-8 -*-
'''
send email via 126.com,support html email

'''
import smtplib
import urllib2
import base64

def crawler(url):
    response = urllib2.urlopen(url)
    html = response.read()
    print '============================================================'
    print '====================crawler done===================================='
    return html

# html=crawler("http://www.baidu.com")
html=crawler("http://www.36kr.com/p/202917.html")
msg ="""
This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
<h2><a href="http://www.ueseo.org">优异搜索</a></h2>
"""+html



def smtp(fromadd='xxx@xx.com',toadd='',subject='',body=''):
    #初始化
    smtp = smtplib.SMTP()
    #链接服务器
    smtp.connect('smtp.126.com',25)
    #等录认证
    smtp.login('pocket2wiz@126.com','pocket')
    #格式信息
    body = base64.b64encode(body)
    subject = base64.b64encode(subject)
    msg = 'From:%s\nTo:%s\nSubject:%s\nContent-Type:text/html\nContent-Transfer-Encoding:base64\n\n%s'%(
        fromadd,toadd,subject,body
    )
    #发送信息
    smtp.sendmail(fromadd,toadd,msg)
    #退出
    smtp.quit()

#测试一下
smtp(fromadd='pocket2wiz@126.com',toadd='luxin6@mywiz.cn',subject='这里是测试风格二哦',body=msg)