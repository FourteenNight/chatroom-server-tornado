import jwt
import sys
import json
from conf.settings import JWT_SECRET

sys.path.append("..")

def set_token(username):
    token = jwt.encode(
        {'username': username},
        JWT_SECRET,
        algorithm='HS256'
    )
    return token



def verify_token(self):
        # 获取cookie中保存的token，并进行验证
        data = json.loads(self.request.body.decode('utf-8'))
        token = data['token']
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            username = decoded['username']
            resp = {'code': 200, 'msg': '有效 token'}
            self.write(resp)
        except (jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError,
                jwt.exceptions.ExpiredSignatureError):
            resp = {'code': 400, 'msg': '无效 token'}
            self.write(resp)
