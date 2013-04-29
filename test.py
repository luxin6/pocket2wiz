# -*- coding: utf-8 -*-
import httplib
import urllib2
import urllib
import json

def getAccessToken():
    headers = {'Content-Type' : 'application/json; charset=UTF-8','X-Accept': 'application/json'}
    request_data = json.dumps({"consumer_key":"12397-4abda11cc794cf27348c4f9d"})
    url = "https://getpocket.com/v3/get/"

    response_data = makeRequest(headers,request_data,url)
    access_code, username = response_data['access_token'],response_data['username']

    return access_code,username

def makeRequest(request_headers,request_data,request_url):
    request = urllib2.Request(request_url,request_data,request_headers)
    response = urllib2.urlopen(request)
    data = json.load(response)

    return data


def sendhttp():
    #data = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
    data = urllib.urlencode({'consumer_key': '12397-4abda11cc794cf27348c4f9d', 'access_token': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection('https://getpocket.com/v3/get',80)
    conn.request('POST', '/', data, headers)
    httpres = conn.getresponse()
    print httpres.status
    print httpres.reason
    print httpres.read()


if __name__ == '__main__':
   # sendhttp()
    getAccessToken()