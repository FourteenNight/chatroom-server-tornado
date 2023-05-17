#!coding=utf-8
import json
from db import User
from lib import set_token
import sys
sys.path.append("..")


def login(self):
    _USERS = User()
    data = json.loads(self.request.body.decode('utf-8'))
    account = data['account']
    password = data['password']
    if account == None:
        resp = {'code': 400, 'msg': '账号为空'}
        self.write(resp)
        return

    user = _USERS.queryAll(account)
    if user:
        if user['online'] == True:
            resp = {'code': 400, 'msg': '用户已登录'}
            self.write(resp)
            return
        if user['pwd'] == password:
            userInfo = _USERS.query(account)
            token = set_token(account)
            resp = {'code': 200, 'msg': '登录成功', 'data': {
                'userInfo': userInfo,
                'token': token
            }}
            self.write(resp)
        else:
            resp = {'code': 400, 'msg': '密码错误'}
            self.write(resp)
    else:
        resp = {'code': 400, 'msg': '账号不存在'}
        self.write(resp)
