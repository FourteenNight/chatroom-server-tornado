#!coding=utf-8

from .sql import DB


class User(DB):
    def __init__(self) -> None:
        super().__init__('chatroom')
        self.users = self.db['users']

    # **************
    # @description: 用户账号信息
    # @param {str} account 需要查询的用户账号
    # @return {*} 返回用户的 账号、用户名、用户类型、创建和更新时间
    # @notes:
    # **************
    def query(self, account: str):
        findCondition = {'account': account}
        filter = {'_id': 0,  'pwd': 0}
        res = self.users.find_one(findCondition, filter)
        return res

    # **************
    # @description: 查询用户所有信息
    # @param {str} account 需要查询的用户账号
    # @return {*} 返回所查询用户的所有信息
    # @notes:
    # **************
    def queryAll(self, account: str):
        findCondition = {'account': account}
        filter = {'_id': 0}
        res = self.users.find_one(findCondition, filter)
        return res

    # **************
    # @description: 查询账号
    # @param {str} account 需要查询的账号
    # @return {*} 返回所查询用户的 账号、用户名
    # @notes:
    # **************
    def queryName(self, account: str):
        findCondition = {'account': account}
        filter = {
            '_id': 0,
            'creation_time': 0,
            'update_time': 0,
            'pwd': 0,
            'online': 0,
            'wsid': 0,
        }
        res = self.users.find_one(findCondition, filter)
        return res
    
    # **************
    # @description: 查询账号
    # @param {str} name 需要查询的用户名
    # @return {*} 返回所查询用户的 账号、用户名
    # @notes:
    # **************
    def queryAccount(self, name: str):
        findCondition = {'name': name}
        filter = {
            '_id': 0,
            'creation_time': 0,
            'update_time': 0,
            'pwd': 0,
            'type': 0,
            'online': 0,
            'wsid': 0,
        }
        res = self.users.find_one(findCondition, filter)
        return res

    # **************
    # @description: 插入普通用户数据
    # @param {str} account 用户账号
    # @param {str} name 用户名
    # @param {str} pwd 用户密码
    # @return {*}
    # @notes:
    # **************
    def insert(self, account: str, name: str, pwd: str, time: str):
        try:
            self.users.insert_one({
                'account': account,
                'name': name,
                'pwd': pwd,
                'creation_time': time,
                'online': False,
                'type': 'user',
            })
            return True
        except Exception as e:
            print(e)
            return False

    # **************
    # @description: 删除用户数据
    # @param {str} account 用户账号
    # @return {*}
    # @notes:
    # **************
    def delete(self, account: str):
        try:
            self.users.delete_one({'account': account})
            return True
        except Exception as e:
            print(e)
            return False

    # **************
    # @description: 更新用户数据
    # @param {str} account 用户账号
    # @param {str} name 用户名
    # @param {str} pwd 用户密码
    # @return {*}
    # @notes:
    # **************
    def update(self, account: str, name: str, pwd: str):
        try:
            findCondition = {'account': account}
            if name=='':
                self.users.update_one(findCondition, {'$set': {
                    'pwd': pwd,
                }})
                return True
            if pwd=='':
                self.users.update_one(findCondition, {'$set': {
                    'name': name,
                }})
                return True
            if name!='' and pwd!='':
                self.users.update_one(findCondition, {'$set': {
                    'name': name,
                    'pwd': pwd,
                }})
                return True
        except Exception as e:
            print(e)
            return False

    # **************
    # @description: 更新用户在线状态
    # @param {str} account 用户账号
    # @param {str} online 在线状态
    # @param {str} id wsid
    # @return {*}
    # @notes:
    # **************
    def updateStatus(self, account: str, online: bool, id: str,):
        try:
            findCondition = {'account': account}
            self.users.update_one(findCondition, {'$set': {
                'online': online,
                'wsid': id,
            }})
            return True
        except Exception as e:
            print(e)
            return False
