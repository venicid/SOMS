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
import requests

# ssl._create_default_https_context = ssl._create_unverified_context
context = ssl._create_unverified_context()

try:
    import json
except ImportError:
    import simplejson as json

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
        return res.json()


    def list_all_key(self):
        '''
        获取包括认证、未认证salt主机
        '''
        print(1111111111111111)
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        content = self.__post(json=params)
        print(2222222222222222)
        print(content)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']

        return minions, minions_pre

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
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def salt_runner(self,jid):
        '''
        通过jid获取执行结果
        '''

        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        params = {}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.getRequest(prefix='/jobs/{}'.format(jid))
        #ret = content['info'][0]['Result']
        return content

    def salt_running_jobs(self):
        '''
        获取运行中的任务
        '''

        params = {'client':'runner', 'fun':'jobs.active'}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def remote_execution(self,tgt,fun,arg,expr_form):
        '''
        异步执行远程命令
        '''

        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def remote_module(self,tgt,fun,arg,kwarg,expr_form):
        '''
        异步部署模块
        '''

        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        #kwarg = {'SALTSRC': 'PET'}
        params2 = {'arg':'pillar={}'.format(kwarg)}
        arg_add = urllib.parse.urlencode(params2)
        obj = urllib.parse.urlencode(params)
        obj = obj + '&' + arg_add
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def remote_localexec(self,tgt,fun,arg,expr_form):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_state(self,tgt,arg,expr_form):
        '''
        sls文件
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def project_manage(self,tgt,fun,arg1,arg2,arg3,arg4,arg5,expr_form):
        '''
        文件上传、备份到minion、项目管理
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        # 拼接url参数
        params2 = {'arg':arg2}
        arg_add = urllib.parse.urlencode(params2)
        obj = urllib.parse.urlencode(params)
        obj = obj + '&' + arg_add
        params3 = {'arg': arg3}
        arg_add = urllib.parse.urlencode(params3)
        obj = obj + '&' + arg_add
        params4 = {'arg': arg4}
        arg_add = urllib.parse.urlencode(params4)
        obj = obj + '&' + arg_add
        params5 = {'arg': arg5}
        arg_add = urllib.parse.urlencode(params5)
        obj = obj + '&' + arg_add
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_copy(self,tgt,fun,arg1,arg2,expr_form):
        '''
        文件上传、备份到minion、项目管理
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        # 拼接url参数
        params2 = {'arg':arg2}
        arg_add = urllib.parse.urlencode(params2)
        obj = urllib.parse.urlencode(params)
        obj = obj + '&' + arg_add
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_bak(self,tgt,fun,arg,expr_form):
        '''
        文件备份到master
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_manage(self,tgt,fun,arg1,arg2,arg3,expr_form):
        '''
        文件回滚
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        params2 = {'arg': arg2}
        arg_add = urllib.parse.urlencode(params2)
        obj = urllib.parse.urlencode(params)
        obj = obj + '&' + arg_add
        params3 = {'arg': arg3}
        arg_add_2 = urllib.parse.urlencode(params3)
        obj = obj + '&' + arg_add_2
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_alive(self,tgt):
        '''
        salt主机存活检测
        '''

        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}

        content = self.__post(json=params)

        ret = content['return'][0]
        return ret

    def remote_server_info(self,tgt,fun):
        '''
        获取远程主机信息
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}

        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

def main():
    sapi = SaltAPI(url='https://192.168.194.140:8000',username='saltapi',password='saltapi')

if __name__ == '__main__':
    main()
