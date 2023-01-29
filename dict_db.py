"""
    根据逻辑处理需要，提供数据支持
"""
import pymysql
import re

class Dict:

    def __init__(self):
        # 参数字典
        self.kwargs = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "zhlv587..",
            "database": "dict",
            "charset": "utf8"
        }

        # 连接数据库
        self.db = pymysql.connect(**self.kwargs)
        # 生成游标对象：执行sql操作数据，得到操作结果的对象
        self.cur = self.db.cursor()

    # 注册验证
    def register(self, name, password):
        sql = "insert into user (name, password) values (%s, %s);"
        try:
            self.cur.execute(sql, [name, password])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    # 登录验证
    def login(self, name, password):
        sql = "select name from user where name = %s and password= %s;"
        self.cur.execute(sql,[name, password])
        # 查询到返回一个非空元组
        if self.cur.fetchone():
            return True
        else:
            return False

    # 查询单词
    def query(self, word):
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql, [word])
        return self.cur.fetchone()

    # 插入历史记录
    def insert_hist(self, name, word):
        sql = "select id from user where name = %s;"
        self.cur.execute(sql, [name])
        user_id = self.cur.fetchone()[0]
        sql = "select id from words where word = %s;"
        self.cur.execute(sql, [word])
        words_id = self.cur.fetchone()[0]
        sql = "insert into hists (user_id, words_id) values (%s, %s);"
        self.cur.execute(sql, [user_id, words_id])
        self.db.commit()

    # 查询历史记录
    def hist(self, name):
        sql = "select name, word, time from user inner join hists on user.id = hists.user_id " \
              "inner join words on words.id = hists.words_id " \
              "where name = %s order by time desc limit 10;"
        self.cur.execute(sql, [name])
        return self.cur.fetchall()

    def close(self):
        # 关闭
        self.cur.close()
        self.db.close()