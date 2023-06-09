import logging
import base64
import functools
import json
import tornado.gen
import tornado.web
import tornado.escape


logger = logging.getLogger(__name__)


class Router():
    def __init__(self, base_handler, redirect=True):
        self._handlers = []
        self._requests = []
        self._base_handler = base_handler
        # redirect if true, not return redirect_url
        self._redirect = redirect

    @property
    def handlers(self):
        return self._handlers

    @property
    def requests(self):
        return self._requests

    # authentication wrapper
    def _auth_wrap(self, f):
        @functools.wraps(f)
        @tornado.gen.coroutine
        def auth_request(handler):
            user = yield handler.get_cur_user()
            if not user:
                redirect_url = handler.get_login_url() + '?referrer=' + \
                    str(base64.b64encode(
                        handler.request.uri.encode('ascii')))[2:-1]
                if self._redirect:
                    # redirect
                    handler.redirect(redirect_url)
                else:
                    # return json response
                    handler.set_header('Content-Type', 'application/json')
                    handler.write(tornado.escape.json_encode(
                        {'redirect': redirect_url}))
                return
            yield f(handler)

        return auth_request

    # json wrapper
    def _json_wrap(self, f):
        @functools.wraps(f)
        @tornado.gen.coroutine
        def json_request(handler):
            # todo: there's no need to prepare dict input??
            try:
                resp = yield f(handler)
                handler.set_header('Content-Type', 'application/json')
                handler.write(tornado.escape.json_encode(resp))
            except Exception as e:
                raise tornado.web.HTTPError(500, str(e))
                # todo: raise HTTPError
                # handler.logger.warn(str(e) + '\n' + repr(traceback.format_stack()))
                # traceback.print_exc()
        return json_request

    # route of HTTP
    def route(self, method='get', url=None, auth=False, json=False, xsrf=True):

        # self.application.settings.get("xsrf_cookies")

        if method.upper() not in tornado.web.RequestHandler.SUPPORTED_METHODS:
            raise ValueError('invalid HTTP method {} found! tornado only supports HTTP methods in {}'.format(
                method, tornado.web.RequestHandler.SUPPORTED_METHODS))

        def req_wrap(f):

            if not self._base_handler:
                raise RuntimeError('base_handler must be initialized!')

            class InnerHandler(self._base_handler):
                pass

            req = self._json_wrap(tornado.gen.coroutine(
                f)) if json else tornado.gen.coroutine(f)
            req = self._auth_wrap(req) if auth else req

            setattr(InnerHandler, method.lower(), req)

            if not xsrf:
                setattr(InnerHandler, "check_xsrf_cookie", lambda self: None)

            InnerHandler.logger = logging.getLogger(f.__name__)

            f_url = url
            if not f_url:
                f_url = '/' + f.__name__

            self._handlers.append((f_url, InnerHandler))

            @functools.wraps(f)
            def request():
                pass

            self._requests.append(request)
            return request

        return req_wrap

    # route of WebSocket
    def ws_route(self, url_pattern, handler_class):
        self._handlers.append((url_pattern, handler_class))


class BaseHandler(tornado.web.RequestHandler):

    _login_url = '/login'

    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Authorization')
        self.set_header('Access-Control-Allow-Methods', "POST, GET, OPTIONS")

    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "*")
    #     self.set_header("Access-Control-Allow-Credentials", "true")
    #     self.set_header("Access-Control-Allow-Methods",
    #                     "POST, GET, PUT, OPTIONS, DELETE, PATCH")
    #     self.set_header("Access-Control-Allow-Headers",
    #                     "content-type,x-requested-with,Authorization, x-ui-request,lang,token")
    #     self.set_header("Access-Control-Max-Age", 3600)

    def options(self):
        # 设置对 OPTIONS 请求的响应头信息
        self.set_status(204)
        self.finish()

    def get_login_url(self):
        return self._login_url

    @tornado.gen.coroutine
    def get_cur_user(self):
        if not hasattr(self, '_cur_user'):
            self._cur_user = None
        current_user = self._cur_user
        if not current_user:
            user_cookie = self.get_secure_cookie('user', max_age_days=1)
            if not user_cookie:
                return None
            current_user = json.loads(user_cookie.decode('utf-8'))
        self._cur_user = current_user
        return self._cur_user

    @tornado.gen.coroutine
    def set_cur_user(self, user):
        self.set_secure_cookie('user', json.dumps(user).encode(
            'utf-8'), expires_days=1, httponly=True)
        self._cur_user = user

    @tornado.gen.coroutine
    def clear_cur_user(self):
        self.clear_cookie('user')
        self._cur_user = None
