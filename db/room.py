from .sql import DB
from bson import ObjectId


class Rooms(DB):
    def __init__(self) -> None:
        super().__init__('chatroom')
        self.channels= self.db['channels']
        self.group_chat= self.db['group_chat_message']
        self.personal_chat= self.db['personal_chat_message']

    # ============================================ 频道 ============================================

    # ************** 
    # @description: 查询频道
    # @param {*} self
    # @return {*} 返回所有频道信息
    # @notes: 
    # **************     
    def query(self):
        documents = self.channels.find()
        arr = []
        for document in documents:
            arr.append(document)
        return arr
    
    # ************** 
    # @description: 查询频道ID
    # @param {*} self
    # @param {*} name 需要查需频道的名字
    # @return {*} 返回查询频道的ID
    # @notes: 
    # **************     
    def queryId(self,name):
        findCondition = {'name': name}
        filter = {'creator': 0}
        res = self.channels.find_one(findCondition, filter)
        return res
    
    # ************** 
    # @description: 查询频道名字
    # @param {*} self
    # @param {*} id 需要查询的ID
    # @return {*}
    # @notes: 
    # **************     
    def queryName(self,id):
        findCondition = {'_id': ObjectId(id)}
        filter = {'_id': 0}
        res = self.channels.find_one(findCondition, filter)
        return res
    

     # **************
    # @description: 更新频道名字
    # @param {str} id 频道id
    # @param {str} name 更改名字
    # @param {str} user 更改的用户
    # @return {*}
    # @notes:
    # **************
    def updateName(self, id: str, name: str,user:str):
        try:
            findCondition = {'_id': ObjectId(id)}
            self.channels.update_one(findCondition, {'$set': {
                'name': name,
                'creator': user,
            }})
            return True
        except Exception as e:
            print(e)
            return False

    # ************** 
    # @description: 更新所有聊天记录中的频道名字
    # @param {*} self
    # @param {str} name 原来的名字
    # @param {str} newName 新名字
    # @return {*}
    # @notes: 
    # **************     
    def updateMsgsRoomName(self, name: str, newName: str):
        try:
            findCondition = {'channels_name': name}
            self.group_chat.update_many(findCondition, {'$set': {
                'channels_name': newName
            }})
            return True
        except Exception as e:
            print(e)
            return False
    
    # ************** 
    # @description: 插入频道数据
    # @param {*} self
    # @param {str} creator 创建者
    # @param {str} name 频道名字
    # @return {*}
    # @notes: 
    # **************     
    def insertChannels(self, creator: str, name: str):
        try:
            self.channels.insert_one({
                'creator': creator,
                'name': name,
            })
            return True
        except Exception as e:
            print(e)
            return False

    # ************** 
    # @description: 删除频道 
    # @param {*} self
    # @param {str} id 频道ID
    # @return {*}
    # @notes: 
    # **************     
    def deleteChannels(self, id: str):
        try:
            self.channels.delete_one({'_id': ObjectId(id)})
            return True
        except Exception as e:
            print(e)
            return False



    # ============================================ 聊天 ============================================

    # ************** 
    # @description: 插入群聊数据
    # @param {*} self
    # @param {str} id 频道id
    # @param {str} name 频道名字
    # @param {str} user 用户
    # @param {str} time 创建时间
    # @param {str} msg 消息
    # @return {*}
    # @notes: 
    # **************     
    def insertGroupMsg(self, id: str,name:str, user: str, time: str,msg: str):
        try:
            self.group_chat.insert_one({
                'channels_id': id,
                'channels_name': name,
                'create_time': time,
                'user': user,
                'content': msg,
            })
            return True
        except Exception as e:
            print(e)
            return False
        
    # ************** 
    # @description: 插入私聊数据
    # @param {*} self
    # @param {str} sender 发送人
    # @param {str} receiver 接收人
    # @param {str} time 创建时间
    # @param {str} msg 消息
    # @return {*}
    # @notes: 
    # **************     
    def insertPersonalMsg(self, sender: str,receiver:str, time: str,msg: str):
        try:
            self.personal_chat.insert_one({
                'sender': sender,
                'receiver': receiver,
                'content': msg,
                'create_time': time,
            })
            return True
        except Exception as e:
            print(e)
            return False

    # ************** 
    # @description: 查询群聊记录
    # @param {*} self
    # @return {*}
    # @notes: 
    # ************** 
    def queryGroupMsgs(self):
        documents = self.group_chat.find()
        arr = []
        for document in documents:
            arr.append(document)
        return arr
    
    # ************** 
    # @description: 查询私聊记录
    # @param {*} self
    # @return {*}
    # @notes: 
    # ************** 
    def queryPersonalMsgs(self):
        documents = self.personal_chat.find()
        arr = []
        for document in documents:
            arr.append(document)
        return arr
