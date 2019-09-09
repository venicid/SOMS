#!/usr/bin/env python
# coding: utf8
'''
@author: qitan
@contact: qqing_lai@hotmail.com
@file: saltapi.py
@time: 2017/3/30 15:29
@desc:
'''

import ssl
import urllib
from urllib import request
from urllib import parse
# python3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# ssl._create_default_https_context = ssl._create_unverified_context
context = ssl._create_unverified_context()

try:
    import json
except ImportError:
    import simplejson as json

import requests


class SaltAPI(object):
    __token_id = ''

    def __init__(self):
        self.url = 'https://192.168.194.140:8000/'
        self.__user = 'saltapi'
        self.__password = 'saltapi'
        self.headers = {"Accept":"application/json",'content-type': 'application/json'}
        self.__token = self.get_token()

    def get_token(self):
        ''' user login and get token id '''
        params = {'username': self.__user, 'password': self.__password, 'eauth': 'pam'}
        res = requests.post(url=self.url + 'login', headers=self.headers, verify=False, json=params)
        print(res.headers['x-auth-token'])
        return res.headers['x-auth-token'] if res.headers.get('x-auth-token') else ''

    def __post(self,**kwargs):
        self.headers['X-Auth-Token'] = self.__token
        res = requests.post(url=self.url, headers=self.headers, verify=False, **kwargs)
        print(res.json())
        return res.json()['return'][0] if res.json().get('return') else ''

    def remote_execution(self,tgt,fun,arg,tgt_type='glob'):
        '''
        异步执行远程命令
        '''
        params = {"client": "local_async", "tgt": tgt, "fun": fun, "arg": arg, "tgt_type": tgt_type}
        print(params)
        ret = self.__post(json=params)
        print(ret)
        return ret.get('jid')

    def getRequest(self,prefix='/'):
        url = self.url + prefix
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib.request.Request(url, headers=headers)
        opener = urllib.request.urlopen(req, context=context)
        content = json.loads(opener.read())
        return content

    def postRequest(self,obj,prefix='/'):
        url = self.url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, obj, headers)
        opener = urllib.request.urlopen(req, context=context)
        content = json.loads(opener.read())
        return content


    def list_all_key(self):
        '''
        获取包括认证、未认证salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.parse.urlencode(params)
        content = self.__post(obj)
        print(111111111111111,content)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        print(minions,minions_pre)
        return minions,minions_pre


    def delete_key(self,node_name):
        '''
        拒绝salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.parse.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self,node_name):
        '''
        接受salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.parse.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def salt_runner(self,jid):
        '''
        通过jid获取执行结果
        '''
        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        print(params)
        res = requests.get(url=self.url+'jobs/'+jid, headers=self.headers, verify=False, json=params)
        print(res)
        return res.json()



    def salt_running_jobs(self):
        '''
        获取运行中的任务
        '''

        params = {'client':'runner', 'fun':'jobs.active'}
        obj = urllib.parse.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret


    def salt_alive(self,tgt):
        '''
        salt主机存活检测
        '''

        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        obj = urllib.parse.urlencode(params)

        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def remote_server_info(self,tgt,fun):
        '''
        获取远程主机信息
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}

        obj = urllib.parse.urlencode(params)

        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

def main():
    sapi = SaltAPI()

if __name__ == '__main__':
    main()

