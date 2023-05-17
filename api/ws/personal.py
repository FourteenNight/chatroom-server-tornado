import json
import tornado.websocket
from db import User ,Rooms
from lib import nowTime
from ..chat import queryPersonalMsgs
import sys
sys.path.append("..")


class PersonalWebSocket(tornado.websocket.WebSocketHandler):
    connections = {}
    _USERS = User()
    _ROOMS = Rooms()

    def open(self):
        # self.connections.add(self)
        wsid = id(self)
        account = self.get_argument("user")
        self.connections.update({account: self})
        print(self.connections)
        self._queryMsgs()


    def on_close(self):
        wsid = id(self)
        account = self.get_argument("user")
        try:
            del self.connections[account]
        except:
            print(self.connections)
        print("personal WebSocket closed with ID:", wsid)

    def on_message(self, message):
        account = self.get_argument("user")
        receiver = self.get_argument("receiver")
        name = self._USERS.queryName(account)["name"]
        now = nowTime()
        resp = json.dumps({
            'type': 'personal',
            'receiver':receiver,
            'sender':name,
            'time':now,
            'data': message
        })
        # room = self._ROOMS.queryId(receiver)
        self._ROOMS.insertPersonalMsg(name,receiver,now,message)
        self.personal_message(resp)


    def personal_message(self, messages):
        print('personal WebSocket broadcast')
        for account, connection in self.connections.items():
                connection.write_message(messages)
    
    def _queryMsgs(self):
        res = queryPersonalMsgs()
        resp = json.dumps({
            'type': 'only-one-msgs',
            'data': res
        })
        # print(resp)
        self.personal_message(resp)




    def check_origin(self, origin):
        return True  # 允许 WebSocket 跨域请求
