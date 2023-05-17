import tornado.gen
from ..router import BaseHandler
from ..user import login as _Login
from ..user import logout as _logout
from ..user import register as _register
from ..user import revise as _revise
from lib import verify_token as _verifyToken


class UserHandler(BaseHandler):
    # 登录
    @tornado.gen.coroutine
    def login(self):
        _Login(self)

    # token验证
    @tornado.gen.coroutine
    def verifyToken(self):
        _verifyToken(self)

    # 注册
    @tornado.gen.coroutine
    def register(self):
        _register(self)

    # 退出登录
    @tornado.gen.coroutine
    def logout(self):
        _logout(self)

    # 修改信息
    @tornado.gen.coroutine
    def revise(self):
        _revise(self)
