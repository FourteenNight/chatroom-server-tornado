import json
import tornado.websocket
from db import User ,Rooms
from lib import nowTime
from ..chat import queryMsgs
import sys
sys.path.append("..")


class ChatWebSocket(tornado.websocket.WebSocketHandler):
    connections = {}
    _USERS = User()
    _ROOMS = Rooms()

    def open(self):
        # self.connections.add(self)
        wsid = id(self)
        account = self.get_argument("user")
        self.connections.update({account: self})
        print("Chat WebSocket opened with ID:", wsid)
        self._queryMsgs()


    def on_close(self):
        wsid = id(self)
        account = self.get_argument("user")
        try:
            del self.connections[account]
        except:
            print(self.connections)
        print("Chat WebSocket closed with ID:", wsid)

    def on_message(self, message):
        account = self.get_argument("user")
        roomName = self.get_argument("roomName")
        name = self._USERS.queryName(account)["name"]
        now = nowTime()
        resp = json.dumps({
            'type': 'broadcast',
            'roomName':roomName,
            'sender':name,
            'time':now,
            'data': message
        })
        room = self._ROOMS.queryId(roomName)
        self._ROOMS.insertGroupMsg(room['_id'],room['name'],name,now,message)
        self.broadcast_message(resp)

    @classmethod
    def broadcast_message(self, messages):
        print('Chat WebSocket broadcast')
        for account, connection in self.connections.items():
            connection.write_message(messages)
    
    def _queryMsgs(self):
        res = queryMsgs()
        resp = json.dumps({
            'type': 'only-one-msgs',
            'data': res
        })
        # print(resp)
        self.broadcast_message(resp)




    def check_origin(self, origin):
        return True  # 允许 WebSocket 跨域请求
