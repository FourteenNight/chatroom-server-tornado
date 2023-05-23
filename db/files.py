from .sql import DB

class Files(DB):
    def __init__(self) -> None:
        super().__init__('chatroom')
        self.files= self.db['files']

    # ************** 
    # @description: 查询频道
    # @param {*} self
    # @return {*} 返回所有频道信息
    # @notes: 
    # **************     
    def query(self):
        documents = self.files.find()
        arr = []
        for document in documents:
            arr.append(document)
        return arr
    
    # ************** 
    # @description: 插入文件数据
    # @param {*} self
    # @param {str} name 文件名字
    # @param {str} path 文件路径
    # @return {*}
    # @notes: 
    # **************     
    def insert(self, name: str,  path: str,sender:str,receiver: str,time: str):
        try:
            self.files.insert_one({
                'name': name,
                'path': path,
                'sender': sender,
                'time': time,
            })
            return True
        except Exception as e:
            print(e)
            return False
 