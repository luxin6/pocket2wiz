# -*- coding:utf-8 -*-
import json
from jsonconfig import JsonConfig
import sys
import requests
import urllib2
import hashlib
import pickle
import smtplib
import base64


RETRIEVE_URL = "https://getpocket.com/v3/get"
SEND_URL = "https://getpocket.com/v3/send"
ADD_URL = "https://getpocket.com/v3/add"

class PocketApi(object):
    def __init__(self,json_config):
        self.json_config=json_config
    def retrieve(self):
        print self.json_config,'======================='
        response = requests.get(RETRIEVE_URL, params=self.json_config.config)
        print response
        items = response.json()['list']
        return items


    def modify(self):
        if 'actions' not in self.json_config:
            raise Exception('Actions are not in the request body')
        headers = {'content-type': 'application/json',
                   'X-Accept': 'application/json'}
        payload = json.dumps(self.json_config)
        response = requests.post(SEND_URL, headers=headers, data=payload)
        if response.status_code not in range(200, 299):
            print "Returned Status Code %d: %s" % (response.status_code,
                                                   response.content)
            sys.exit(1)
        return response

    def add(self):
        if 'url' not in self.json_config:
            raise Exception('"url" is not in the request body')
        headers = {'content-type': 'application/json',
                   'X-Accept': 'application/json'}
        payload = json.dumps(self.json_config)
        response = requests.post(ADD_URL, headers=headers, data=payload)
        if response.status_code != 200:
            print "Returned Status Code %d: %s" % (response.status_code,
                                                   response.content)
            sys.exit(1)
        return response

class Article(object):
    def __init__(self):
        self.hash_id=""
        self.title=""
        self.url="www.baidu.com"
        self.content=""

    def get_content(self):
        print '=============begin get_content from',self.url,'============================================='
        response = urllib2.urlopen(self.url)
        self.content = response.read()
        print '=============get_content from',self.url,' done============================================='
        return self.content
    def get_hashid(self):
        self.hash_id=hashlib.md5(self.url).hexdigest()
        return self.hash_id
    def print_article(self):
        print "title",self.title,"url",self.url,"hash_id",self.hash_id

class Pocket(object):
    def __init__(self):
        self.CONFIG_FILE = '.creds'
        self.articleids='.articleids'
        self.json_conf=JsonConfig(self.CONFIG_FILE)
        self.conf=self.json_conf.config
        self.article_list=[]
        #这个list是最终发送成功到wiz的文章list
        self.articleid_list=[]
        self.pocket_controller=PocketApi(self.json_conf)
        #todone : 需要在硬盘保存一个hashid的文件，保证pocket里面的内容是不重复的
    def retrieve_article(self):
        print self.json_conf.read(),'--------------------'
        # self.articleid_list=self.load_articleids()
        self.load_articleids()
        print "in func: retrieve_article() articleid_list:",self.articleid_list
        item_list=self.pocket_controller.retrieve()
        for item in item_list:
            article=Article()
            article.title=item_list[item]['given_title']
            article.url=item_list[item]['resolved_url']
            article.hash_id=article.get_hashid()
            if not self.isexist_article(article):
                print "this article is not exist in wiz"
                article.print_article()
                self.article_list.append(article)
        #        self.articleid_list.append(article.hash_id)
        # 保存article id到硬盘里面，每次取完文章之后必须做的
        #self.dump_articleids()
        return self.article_list
    def send_article(self):
        if self.article_list==None or len(self.article_list)==0:
            return
        for article in self.article_list:
            try:
                title="[Pocket] "+article.title
                html=article.get_content()
                msg ="""
                这个文章是由pocket2wiz直接从pocket转发 ：）
                """+html
                self.__send2wiz(fromadd='pocket2wiz@126.com',toadd='luxin6@mywiz.cn',subject=title,body=msg)
                print "send article to wiz successful! title:",title
            except UnicodeEncodeError,UnicodeError:
                print "WARNING: the article is sended fail!.title:",article.title," url:",article.url
                continue
            self.articleid_list.append(article.get_hashid())
        self.dump_articleids()

        print "end of func send_article()"

    def print_article(self):
        print self.article_list
    def print_article_1by1(self):
        if self.article_list==None:
            print "no article updated, please select more article into pocket :)"
        print "print article 1by1,the article num is:",len(self.article_list)
        for article in self.article_list:
            article.print_article()
    def load_articleids(self):
        temp=open(self.articleids,'r')
        try:
            self.articleid_list=list(pickle.load(temp))
            print self.articleid_list
            print "before we update from the pocket,there is ",len(self.articleid_list)," articles in wiz"
        except EOFError:
            print "the file ",self.articleids," is empty"
            self.articleid_list=[]
        if len(self.articleid_list)==0 or self.articleid_list==None:
            print "the file ",self.articleids," is empty"
            self.articleid_list=[]
        temp.close()
        # return self.articleid_list
    def dump_articleids(self):
        temp=open(self.articleids,'w')
        pickle.dump(self.articleid_list,temp)
        temp.close()
    def isexist_article(self,article):
        if self.articleid_list==None:
            self.articleid_list=[]
            print "------the article list is none"
            return False
        hashid=article.get_hashid()
        print "+++++++++",self.articleid_list,"++++++++++"
        for id in self.articleid_list:
            if hashid==id:
                print "this article is aleady in wiz :),hashid:",hashid
                return True
        print "this article is not in wiz yet :(,hashid:",hashid
        return False
    def __transcode(self,subject):
        if isinstance(subject,unicode):
            subject=subject.encode('gb2312')
        else:
            subject=subject.decode('utf-8').encode('gb2312')
        return subject

    def __send2wiz(self,fromadd='xxx@xx.com',toadd='',subject='',body=''):
        #初始化
        smtp = smtplib.SMTP()
        #链接服务器
        smtp.connect('smtp.126.com',25)
        #等录认证
        smtp.login('pocket2wiz@126.com','pocket')
        #格式信息
        body = base64.b64encode(body)
        # subject = base64.b64encode(subject)
        subject=self.__transcode(subject)

        msg = 'From:%s\nTo:%s\nSubject:%s\nContent-Type:text/html\nContent-Transfer-Encoding:base64\n\n%s'%(
            fromadd,toadd,subject,body
        )
        #发送信息
        smtp.sendmail(fromadd,toadd,msg)
        #退出
        smtp.quit()


if __name__ == "__main__":
    pocket=Pocket()
    pocket.retrieve_article()
#    pocket.print_article_1by1()
    pocket.send_article()

# todo: 看一下getpocket的access_token是否有每日的使用次数
# todo: 去除每次从pocket取文章的feature还未通过测试
# todo: 补充每个函数的注释

