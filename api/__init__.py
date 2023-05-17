import tornado.gen
from .router import Router
from .router import BaseHandler
from .ws import EchoWebSocket,ChatWebSocket,PersonalWebSocket
from .handler import UserHandler
from .handler import ChatHandler


class IndexHandler(BaseHandler):
    @tornado.gen.coroutine
    def index(self):
        self.render('index.html')


# 路由注册
router = Router(BaseHandler)
router.route(method='get', url='/', auth=False)(IndexHandler.index)

router.route(method='post', url='/api/user/login', auth=False)(UserHandler.login)

router.route(method='post', url='/api/user/logout', auth=False)(UserHandler.logout)

router.route(method='post', url='/api/user/register',
             auth=False)(UserHandler.register)

router.route(method='post', url='/api/user/revise', auth=False)(UserHandler.revise)

router.route(method='post', url='/api/token/verify',
             auth=False)(UserHandler.verifyToken)

router.route(method='post', url='/api/rooms/update',
             auth=False)(ChatHandler.channelsUpdate)

router.route(method='post', url='/api/rooms/add',
             auth=False)(ChatHandler.channelsAdd)

router.route(method='post', url='/api/rooms/del',
             auth=False)(ChatHandler.channelsDel)

router.ws_route('/ws', EchoWebSocket)
router.ws_route('/chat', ChatWebSocket)
router.ws_route('/personal', PersonalWebSocket)
