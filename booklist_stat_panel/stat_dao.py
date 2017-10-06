
##########################################
#
# 程序功能：
#   书单数据库访问借口，
# 提供书单数据库的各种查询，获取感兴趣的书籍推荐
# 已提供接口：
# 1.top15 最多人关注的书单
# 2.top30 最多被书单收集的书
# 3.top50 最多人喜欢的书
# 4.top20 最多作品被收集的作者的书
#
##########################################

import pymysql
import re

class StatDao:


    # 构造函数
    def __init__(self):
        # 打开数据库连接
        # drop database testdb;
        # create database testdb charset utf8mb4;
        # 注意数据库创建连接的时候需要设置字符集，否则插入字符将导致插入失败！！！
        self.databasename = 'testdb3'
        self.db = pymysql.connect("localhost", "tianjiqx", "123456", self.databasename, charset='utf8mb4')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.dbcurosr = self.db.cursor();
        # 使用自动提交
        self.db.autocommit(True)


    # api1：top15 最多人关注的书单
    def stat_most_attentions(self):

        top_num = 15

        # 查询sql
        sql = "select * from booklists ORDER BY attention DESC limit " + str(top_num);

        # 执行sql
        self.dbcurosr.execute(sql)

        # 获取所有的记录列表
        results = self.dbcurosr.fetchall()

        #返回结果
        return results

    # api2:top30 最多被书单收集的书
    def stat_most_collected_books(self):

        top_num = 30

        # 查询sql
        sql = '''SELECT bookid
                    ,bookname
                    ,writer
                    ,intro
                    ,group_concat(quote separator '\n§----❀❀❀----✿✿✿✿✿----❀❀❀----$') as quotes
                    ,sum(heart) AS sum_heart
                    ,count(bookid) AS num
                    ,url
                FROM books
                GROUP BY bookid
                ORDER BY num DESC limit ''' + str(top_num);

        # 执行sql
        self.dbcurosr.execute(sql)

        # 获取所有的记录列表
        results = self.dbcurosr.fetchall()

        # 返回结果
        return results

    # api3:top50 最多人喜欢的书
    def stat_most_hearts(self):

        top_num = 50

        # 查询sql
        sql = '''SELECT bookid
                    ,bookname
                    ,writer
                    ,intro
                    ,group_concat(quote separator '\n§----❀❀❀----✿✿✿✿✿----❀❀❀----$') AS quotes
                    ,sum(heart) AS sum_heart
                    ,count(bookid) AS num
                    ,url
                FROM books
                GROUP BY bookid
                ORDER BY sum_heart DESC
                    ,num DESC limit '''+ str(top_num);

        # 执行sql
        self.dbcurosr.execute(sql)

        # 获取所有的记录列表
        results = self.dbcurosr.fetchall()

        # 返回结果
        return results

    # api4: top20 最多作品被收集的作者(不去重)
    def stat_most_woker_collecteds(self):

        top_num = 20

        # 查询sql
        sql = '''SELECT writer
                    ,group_concat(bookid separator ' | ') AS bookids
                    ,group_concat(bookname separator '》、《') AS booknames
                    ,group_concat(intro separator '\n§----❀❀❀----✿✿✿✿✿----❀❀❀----$\n')
                    ,group_concat(quote separator '\n§----❀❀❀----✿✿✿✿✿----❀❀❀----$\n') AS quotes
                    ,sum(heart) AS sum_heart
                    ,count(bookid) AS num
                    ,group_concat(url separator '\n§----❀❀❀----✿✿✿✿✿----❀❀❀----$\n') AS urls
                FROM books
                GROUP BY writer
                ORDER BY num DESC,sum_heart DESC limit '''+ str(top_num);

        # 执行sql
        self.dbcurosr.execute(sql)

        # 获取所有的记录列表
        results = self.dbcurosr.fetchall()

        # 返回结果
        return results


    # 关闭数据库连接
    def close(self):

        self.dbcurosr.close()