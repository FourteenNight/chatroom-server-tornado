import json
import base64
import sys
from conf import UPLOAD_PATH
from db import Files
from lib import nowTime
sys.path.append("..")


def uploads(self):
    _FILES = Files()
    upload_path = UPLOAD_PATH+'/files/'

    data = json.loads(self.request.body.decode('utf-8'))
    name = data['name']
    file = data['file']
    sender = data['sender']
    receiver = data['receiver']
    file_bytes = base64.b64decode(file)
    with open(upload_path+name, "wb") as f:
        f.write(file_bytes)
    if _FILES.insert(name, upload_path+name, sender, receiver, nowTime()):
        resp = {'code': 200, 'msg': '文件保存完成'}
    else:
        resp = {'code': 400, 'msg': '文件保存失败'}
    self.write(resp)
    return
