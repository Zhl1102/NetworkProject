def _menu_1():
    while True:
        print("""
        ========== Welcome ==========
          1. 登录    2.注册    3.退出
        =============================
        """)
        cmd = input("请输入选项：")
        if cmd == "1":
            _menu_2()
        elif cmd == "2":
            pass
        elif cmd == "3":
            pass
        else:
            print("请输入正确选项:")

def _menu_2():
    while True:
        print("""
        ============== Query =============
          1. 查单词    2.历史记录    3.注销
        ==================================
        """)
        cmd = input("请输入选项：")
        if cmd == "1":
            pass
        elif cmd == "2":
            pass
        elif cmd == "3":
            _menu_1()
        else:
            print("请输入正确选项!")


_menu_1()