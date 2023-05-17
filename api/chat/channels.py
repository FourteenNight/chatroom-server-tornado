#!coding=utf-8
import json
import sys
from db import Rooms
sys.path.append("..")


def queryRooms():
    _ROOM = Rooms()
    arr = _ROOM.query()
    res = []
    for i in arr:
        res.append({
            'id': str(i['_id']),
            'name': i['name'],
            'creator': i['creator']
        })
    return res


# 频道名字更改
def channelsUpdate(self):
    _ROOM = Rooms()
    data = json.loads(self.request.body.decode('utf-8'))
    id = data['id']
    user = data['user']
    newName = data['name']
    name = _ROOM.queryName(id)['name']
    if newName == name:
        resp = {'code': 400, 'msg': '频道名字重复'}
        self.write(resp)
        return
    else:
        if _ROOM.updateName(id,newName,user):
            if _ROOM.updateMsgsRoomName(name,newName):
                resp = {'code': 200, 'msg': '修改成功'}
                self.write(resp)
                return
        else:
            resp = {'code': 400, 'msg': '修改失败'}
            self.write(resp)
            return

# 频道创建
def channelsAdd(self):
    _ROOM = Rooms()
    data = json.loads(self.request.body.decode('utf-8'))
    user = data['user']
    name = data['name']
    nameArr = _ROOM.query()
    # print(isName)
    for i in nameArr:
        if name == i['name']:
            resp = {'code': 400, 'msg': '频道名字重复'}
            self.write(resp)
            return
    if _ROOM.insertChannels(user,name):
            resp = {'code': 200, 'msg': '创建成功'}
            self.write(resp)
            return
    else:
        resp = {'code': 400, 'msg': '创建失败'}
        self.write(resp)
        return
    
# 频道删除
def channelsDel(self):
    _ROOM = Rooms()
    data = json.loads(self.request.body.decode('utf-8'))
    id = data['id']
    if _ROOM.deleteChannels(id):
            resp = {'code': 200, 'msg': '删除成功'}
            self.write(resp)
            return
    else:
        resp = {'code': 400, 'msg': '删除失败'}
        self.write(resp)
        return


def queryMsgs():
    _ROOM = Rooms()
    arr = _ROOM.queryGroupMsgs()
    res = []
    for i in arr:
        res.append({
            'channels_id': str(i['channels_id']),
            'content': i['content'],
            'create_time': i['create_time'],
            'channels_name': i['channels_name'],
            'user': i['user'],
        })
    return res


def queryPersonalMsgs():
    _ROOM = Rooms()
    arr = _ROOM.queryPersonalMsgs()
    res = []
    for i in arr:
        res.append({
            'content': i['content'],
            'create_time': i['create_time'],
            'receiver': i['receiver'],
            'sender': i['sender'],
        })
    return res
