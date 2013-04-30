# -*- coding:utf-8 -*-
import json
from jsonconfig import JsonConfig
import sys
import requests
import urllib2

CONFIG_FILE = '.creds'
RETRIEVE_URL = "https://getpocket.com/v3/get"
SEND_URL = "https://getpocket.com/v3/send"
ADD_URL = "https://getpocket.com/v3/add"

class Article(object):
    def __init__(self):
        self.title=""
        self.url="www.baidu.com"
        self.content=""

    def get_content(self):
        print '=============begin get_content from',self.url,'============================================='
        response = urllib2.urlopen(self.url)
        self.content = response.read()
        print '=============get_content from',self.url,' done============================================='
        return self.content

class Pocket(object):
    pass

def retrieve(config, verbose=False):
    print 'a'
    if verbose:
        config["detailType"] = 'complete'
    response = requests.get(RETRIEVE_URL, params=config)
    print response
    items = response.json()['list']
    return items


def modify(config):
    if 'actions' not in config:
        raise Exception('Actions are not in the request body')
    headers = {'content-type': 'application/json',
               'X-Accept': 'application/json'}
    payload = json.dumps(config)
    response = requests.post(SEND_URL, headers=headers, data=payload)
    if response.status_code not in range(200, 299):
        print "Returned Status Code %d: %s" % (response.status_code,
                                               response.content)
        sys.exit(1)
    return response

def add(config):
    if 'url' not in config:
        raise Exception('"url" is not in the request body')
    headers = {'content-type': 'application/json',
               'X-Accept': 'application/json'}
    payload = json.dumps(config)
    response = requests.post(ADD_URL, headers=headers, data=payload)
    if response.status_code != 200:
        print "Returned Status Code %d: %s" % (response.status_code,
                                               response.content)
        sys.exit(1)
    return response
if __name__ == "__main__":
    jc = JsonConfig(CONFIG_FILE)
    print jc.read()
    #items=retrieve(jc.read())
    items=retrieve(jc.config)
    print items
    print len(items)
    for index in items:
        print index,"==",items[index]
        print "----url------",items[index]["resolved_url"]
        print "----title------",items[index]["given_title"]
        #todone:(2013.4.29 0:20) 1.字符编码问题；2.抓取url对应的网页 3.发送email到wiz里面
        # done 1.编码问题
        #done 2.抓取url对应的页面  in email_html.py
