"""
    接收请求，逻辑处理，发送响应
"""
import sys
from socket import *
from multiprocessing import Process
from dict_db import *

# 服务器端地址
HOST = "0.0.0.0"
PORT = 1102
ADDR = (HOST, PORT)

class Handle(Process):

    def __init__(self, conn):
        self.conn = conn
        self.name = ""
        self.db = Dict()    # 得到数据库处理对象
        super().__init__()

    # 循环接收请求
    def run(self):
        while True:
            request = self.conn.recv(1024)
            tmp = request.decode().split('\t')
            if not request or tmp[0] == "E":
                break   # 客户端退出
            elif tmp[0] == "R":
                self.do_register(tmp[1], tmp[2])
            elif tmp[0] == "L":
                self.do_login(tmp[1], tmp[2])
            elif tmp[0] == "Q":
                self.do_query(tmp[1])
            elif tmp[0] == "H":
                self.do_hist()
        self.db.close()
        self.conn.close()

    # 注册，与数据库发生数据交互
    def do_register(self, name, password):
        # 数据库操作
        if self.db.register(name, password):
            self.conn.send(b"T")
        else:
            self.conn.send(b"F")

    # 登录
    def do_login(self, name, password):
        if self.db.login(name, password):
            self.conn.send(b"T")
            self.name = name    # 登录成功后改变name实例变量
        else:
            self.conn.send(b"F")

    # 查询单词
    def do_query(self, word):
        mean = self.db.query(word)  # 元组
        if mean:
            res = "T\t" + mean[0]
            self.conn.send(res.encode())
            self.db.insert_hist(self.name, word)   # 数据库插入历史记录
        else:
            self.conn.send(b"F")

    def do_hist(self):
        data = self.db.hist(self.name)
        if data:
            res = "T\t"
            for row in data:
                res += "%s,%s,%s;" % row
            self.conn.send(res.encode())
        else:
            self.conn.send(b"F")


class DictServer:

    def __init__(self, host="", port=0):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.sock = self._create_server()

    def _create_server(self):
        # 创建tcp套接字
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(ADDR)
        return sock

    def main(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        # 循环接收客户端消息
        while True:
            conn, addr = self.sock.accept()
            print("Connect the Port %d" % PORT)
            # 为客户端创建进程
            handle = Handle(conn)
            handle.run()

if __name__ == '__main__':
    t = DictServer(host="0.0.0.0", port=1102)
    t.main()