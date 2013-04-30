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
def transcode(subject):
    if isinstance(subject,unicode):
        subject=subject.encode('gb2312')
    else:
        subject=subject.decode('utf-8').encode('gb2312')
    return subject


# html=crawler("http://www.baidu.com")
html=crawler("http://www.36kr.com/p/202917.html")
msg ="""
这个文章是由pocket2wiz直接从pocket转发 ：）
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
   # subject = base64.b64encode(subject)
    subject=transcode(subject)

    msg = 'From:%s\nTo:%s\nSubject:%s\nContent-Type:text/html\nContent-Transfer-Encoding:base64\n\n%s'%(
        fromadd,toadd,subject,body
    )
    #发送信息
    smtp.sendmail(fromadd,toadd,msg)
    #退出
    smtp.quit()

#测试一下
smtp(fromadd='pocket2wiz@126.com',toadd='luxin6@mywiz.cn',subject='这里是测试风格二哦',body=msg)