#!coding=utf-8

import yaml
import os
import datetime


def readConfig(key: str):
    path = os.getcwd()+'/config.yml'
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    result = yaml.load(data, Loader=yaml.FullLoader)  # FullLoafer可以yaml解析变得安全
    if key == 'all':
        return result
    return result[key]


def nowTime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M')
