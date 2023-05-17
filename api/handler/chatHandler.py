import tornado.gen
from ..router import BaseHandler
from ..chat import channelsUpdate as _channelsUpdate
from ..chat import channelsAdd as _channelsAdd
from ..chat import channelsDel as _channelsDel


class ChatHandler(BaseHandler):
    @tornado.gen.coroutine
    def channelsUpdate(self):
        _channelsUpdate(self)

    @tornado.gen.coroutine
    def channelsAdd(self):
        _channelsAdd(self)

    @tornado.gen.coroutine
    def channelsDel(self):
        _channelsDel(self)
