import sys
from conf import UPLOAD_PATH
sys.path.append("..")


def download(self):
    upload_path = UPLOAD_PATH+'/files/'
    name = self.get_argument('name')
    with open(upload_path+name, 'rb') as f:
        while 1:
            data = f.read(16384)  # 或者其他一些大小合适的大块
            if not data:
                break
            self.write(data)
    self.finish()
    return
