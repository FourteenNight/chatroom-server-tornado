#!coding=utf-8
import json
from db import User
import sys
sys.path.append("..")


def revise(self):
    _USERS = User()
    data = json.loads(self.request.body.decode('utf-8'))
    account = data['account']
    name = data['name']
    password = data['password']
    if account == None:
        resp = {'code': 400, 'msg': '账号为空'}
        self.write(resp)
        return
    isName= _USERS.queryAccount(name)
    if isName:
        resp = {'code': 400, 'msg': '用户名已存在'}
        self.write(resp)
        return
    
    if name== None:
        res = _USERS.update(account, '', password)
    if password == None:
        res = _USERS.update(account, name, '')
    if name!= None and password != None:
        res = _USERS.update(account, name, password)

    if res:
        resp = {'code': 200, 'msg': '修改成功'}
        self.write(resp)
        return
    else:
        resp = {'code': 400, 'msg': '修改失败'}
        self.write(resp)
        return