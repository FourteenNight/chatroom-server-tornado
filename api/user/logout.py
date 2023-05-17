#!coding=utf-8
import json
from db import User
import sys
sys.path.append("..")


def logout(self):
    _USERS = User()
    data = json.loads(self.request.body.decode('utf-8'))
    account = data['account']
    if account == None:
        resp = {'code': 400, 'msg': '账号为空'}
        self.write(resp)
        return

    res = _USERS.updateStatus(account, False, '')
    if res:
        resp = {'code': 200, 'msg': '退出登录'}
        self.write(resp)
        return
    else:
        resp = {'code': 400, 'msg': '退出登录失败'}
        self.write(resp)
        return
