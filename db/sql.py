#!coding=utf-8
from pymongo import MongoClient
from conf import DB_SERVER
import sys
sys.path.append("..")


class DB():
    def __init__(self, name) -> None:
        self.conn = MongoClient(
            DB_SERVER['ip'],
            port=DB_SERVER['port'],
            username=DB_SERVER['username'],
            password=DB_SERVER['password'],
            authSource=DB_SERVER['authSource']
        )
        self.db = self.conn[name]
        # print('[-] Database connection status', self.db.command('ping'))
