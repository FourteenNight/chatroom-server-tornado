import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.autoreload
from conf import TEMPLATE_PATH, STATIC_PATH
from api import router


settings = dict(
    template_path=TEMPLATE_PATH,
    static_path=STATIC_PATH,
    default_content_type="application/json",
    debug=True
)

app = tornado.web.Application(router.handlers, **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9000)
    print('Development server is running at http://127.0.0.1:9000')
    print('Quit the server with Control-C')
    tornado.ioloop.IOLoop.current().start()
