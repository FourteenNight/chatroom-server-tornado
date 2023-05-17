import yaml
import os

# 路径设置
TEMPLATE_PATH = os.path.join(os.path.abspath(os.getcwd()), 'templates')
STATIC_PATH = os.path.join(os.path.abspath(os.getcwd()), 'static')
_CONF_PATH = os.path.join(os.path.abspath(os.getcwd()), 'conf')
# token 设置
JWT_SECRET = "some_secret_key"  # 加密密钥
JWT_EXP_DELTA_SECONDS = 86400  # 过期时间为一天
JWT_EXP_RENEW_SECONDS = 86400*2  # 剩下2天时间续约


# 服务器&数据库地址设置
with open(_CONF_PATH+'/config.yml', 'r', encoding='utf-8') as f:
    data = f.read()
    result = yaml.load(data, Loader=yaml.FullLoader)
HOST = result['host']  # 服务器地址
DB_SERVER = result['dbServer']  # 数据库地址
