"""
    客户端：与用户交互发起请求
"""
from socket import *
import sys

ADDR = ("127.0.0.1", 1102)

# 具体向服务端发送请求
class Handle:
    def __init__(self):
        self.sock = self._connect()

    def _connect(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(ADDR)
        return sock

    # 发送注册请求
    def do_register(self, name, password):
        request = "R\t%s\t%s" % (name, password)
        self.sock.send(request.encode())
        response = self.sock.recv(128)
        if response == b"T":
            print("注册成功")
        elif response == b"F":
            print("注册失败")

    # 发送登录请求
    def do_login(self, name, password):
        request = "L\t%s\t%s" % (name, password)
        self.sock.send(request.encode())
        response = self.sock.recv(128)
        if response == b"T":
            print("登录成功")
            return True
        elif response == b"F":
            print("登录失败")

    # 发送退出请求
    def do_exit(self):
        self.sock.send(b"E")
        self.sock.close()
        sys.exit("成功退出")

    # 查询单词
    def do_query(self):
        while True:
            word = input("请输入查询的单词：")
            if not word or word == "#":
                break
            request = "Q\t%s" % word
            self.sock.send(request.encode())
            response = self.sock.recv(1024)
            tmp = response.decode().split("\t", 1)
            if tmp[0] == "T":
                print("%s: %s\n" % (word, tmp[1]))
            else:
                print("没有查到该单词")

    # 查询历史记录
    def do_hist(self):
        self.sock.send(b"H")
        response = self.sock.recv(1024)
        tmp = response.decode().split("\t")
        if tmp[0] == "T":
            for row in tmp[1].split(";"):
                print(row)
        else:
            print("您还没有历史记录")

# 与用户交互
class DictView:
    def __init__(self):
        self.handle = Handle()

    def _menu_1(self):
        while True:
            print("""
            ========== Welcome ==========
              1. 登录    2.注册    3.退出
            =============================
            """)
            cmd = input("请输入选项：")
            if cmd == "1":
                name = input("User：")
                password = input("Password：")
                if self.handle.do_login(name, password):
                    self._menu_2()
            elif cmd == "2":
                name = input("User：")
                password = input("Password：")
                self.handle.do_register(name, password)
            elif cmd == "3":
                self.handle.do_exit()
            else:
                print("请输入正确选项:")

    def _menu_2(self):
        while True:
            print("""
            ============== Query =============
              1. 查单词    2.历史记录    3.注销
            ==================================
            """)
            cmd = input("请输入选项：")
            if cmd == "1":
                self.handle.do_query()
            elif cmd == "2":
                self.handle.do_hist()
            elif cmd == "3":
                self._menu_1()
            else:
                print("请输入正确选项!")

    def main(self):
        self._menu_1()

if __name__ == '__main__':
    view = DictView()
    view.main()