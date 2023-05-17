import time
import jwt
import json
from datetime import datetime, timedelta
from conf import JWT_SECRET, JWT_EXP_DELTA_SECONDS, JWT_EXP_RENEW_SECONDS


def set_token(user, time=None):
    if time is not None:
        # 设置过期时间
        exp_time = datetime.utcnow() + timedelta(seconds=time)
    else:
        # 默认过期时间
        exp_time = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)

    payload = {
        'sub': user,
        'exp': exp_time
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm='HS256'
    )
    return token


def verify_token(self):
    # 获取请求头中保存的 token，并进行验证
    data = json.loads(self.request.body.decode('utf-8'))
    token = data['token']
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = decoded['sub']

        if 'exp' in decoded:
            # 如果 token 带有过期时间，判断是否快要过期了
            remaining_time = decoded['exp'] - int(time.time())
            isRefresh = (remaining_time < JWT_EXP_RENEW_SECONDS)

            if isRefresh:
                # 生成新的 token
                new_token = set_token(user)
                # 更新客户端的 token
                resp = {'code': 200, 'msg': '有效 token，并已自动续约',
                        'token': new_token}
                self.write(resp)
                return

        resp = {'code': 200, 'msg': '有效 token'}
        self.write(resp)
    except (jwt.exceptions.InvalidSignatureError,
            jwt.exceptions.DecodeError,
            jwt.exceptions.ExpiredSignatureError):
        resp = {'code': 400, 'msg': '无效 token'}
        self.write(resp)
