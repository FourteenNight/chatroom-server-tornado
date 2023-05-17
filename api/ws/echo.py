import json
import tornado.websocket
from ..chat import queryRooms
from db import User


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    connections = {}
    _USERS = User()

    def open(self):
        # self.connections.add(self)
        wsid = id(self)
        account = self.get_argument("user")
        user = self._USERS.queryName(account)
        if not account:
            self.close(code=1008, reason='User not authenticated')
        self._USERS.updateStatus(account, True, wsid)
        self.connections.update({account: self})
        self.send_name(user)
        self.send_onlineUser()
        self.send_rooms()
        print("WebSocket opened with ID:", wsid)

    def on_close(self):
        wsid = id(self)
        account = self.get_argument("user")
        self._USERS.updateStatus(account, False, '')
        try:
            del self.connections[account]
            self.send_onlineUser()
        except:
            print(self.connections)
        print("WebSocket closed with ID:", wsid)

        # print(self.connections)

    def on_message(self, message):
        # self.write_message("You say:" + message)
        print(f"WebSocket {self.request.remote_ip}: {message}")

    @classmethod
    def broadcast_message(self, messages):
        print('WebSocket broadcast')
        for account, connection in self.connections.items():
            connection.write_message(messages)
            # print(connection)

    def send_onlineUser(self):
        userArr = []
        for user in self.connections:
            name = self._USERS.queryName(user)
            userArr.append(name)
        resp = json.dumps({
            'type': 'user-online',
            'data': userArr
        })
        self.broadcast_message(resp)

    def send_rooms(self):
        rooms = queryRooms()
        resp = json.dumps({
            'type': 'rooms',
            'data': rooms
        })
        self.write_message(resp)

    def send_name(self, user):
        resp = json.dumps({
            'type': 'user-info',
            'data': user
        })
        self.write_message(resp)

    def check_origin(self, origin):
        return True  # 允许 WebSocket 跨域请求
