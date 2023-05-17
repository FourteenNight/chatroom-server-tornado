#!coding=utf-8
import json
import sys
from db import User
from lib import nowTime
sys.path.append("..")


def register(self):
    _USERS = User()
    data = json.loads(self.request.body.decode('utf-8'))
    account = data['account']
    name = data['name']
    password = data['password']
    if account == None:
        resp = {'code': 400, 'msg': '账号为空'}
        self.write(resp)
        return

    user = _USERS.query(account)
    if user:
        resp = {'code': 400, 'msg': '账号已存在'}
        self.write(resp)
        return
    else:
        now = nowTime()
        res = _USERS.insert(account, name, password, now)
        if res:
            resp = {'code': 200, 'msg': '注册成功'}
            self.write(resp)
        else:
            resp = {'code': 400, 'msg': '注册失败'}
            self.write(resp)
