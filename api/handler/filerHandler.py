import tornado.gen
from ..router import BaseHandler
from ..file import uploads as _uploads
from ..file import download as _download


class FlierHandler(BaseHandler):
    @tornado.gen.coroutine
    def uploads(self):
        _uploads(self)

    def download(self):
        _download(self)
