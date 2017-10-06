
import pymysql
import re

class Dao:

    tablenames = ['booklists','books','bookdetails']
    booklists = ['booklistid varchar(10) primary key,',
                'title varchar(45),',
                'content text(5000),',
                'attention int,',
                'count int,',
                'url varchar(45)'

                ]
    books = ['bookid varchar(10) ,',
            'bookname varchar(45),',
            'writer varchar(45),',
            'intro text(10000),'
            'quote text(50000),',
            'heart int,',
            'booklistid varchar(10),',
            'url varchar(45),'
            'primary key(booklistid,bookid)'
            ]
    bookdetails = ['bookdetailid varchar(10) primary key,',
                  'bookname varchar(45),',
                  'writer varchar(45),',
                  'booktype varchar(10),',
                  'wordcount int,',
                  'catalogcount int,',
                  'clickcount int,',
                  'recommandcount int,',
                  'bookscore double,',
                  'bookintro text(5000),',
                  'url varchar(45)'
                ]
    ddlsqls = [booklists,books,bookdetails]
    # 构造函数
    def __init__(self):
        # 打开数据库连接
        # drop database testdb;
        # create database testdb charset utf8mb4;
        # 注意数据库创建连接的时候需要设置字符集，否则插入字符将导致插入失败！！！
        # self.db = pymysql.connect("localhost", "tianjiqx", "123456", "testdb3",charset='utf8mb4')
        # # 使用 cursor() 方法创建一个游标对象 cursor
        # self.dbcurosr = self.db.cursor();
        # self.db.autocommit(True)

        #self.curosr.execute('use testdb')

        # insert 需要的列
        pass

    # 创建连接
    def connect(self):
        # 打开数据库连接
        # drop database testdb;
        # create database testdb charset utf8mb4;
        # 注意数据库创建连接的时候需要设置字符集，否则插入字符将导致插入失败！！！
        self.db = pymysql.connect("localhost", "tianjiqx", "123456", "testdb3",charset='utf8mb4')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.dbcurosr = self.db.cursor();
        self.db.autocommit(True)

    # 构建数据库
    def build(self):
        self.connect();
        # 如果数据表已经存在使用 execute() 方法删除表。
        for tablename in self.tablenames:
            try:
                ddlsql = "DROP TABLE IF EXISTS "+tablename
                self.dbcurosr.execute(ddlsql)
            except:
                print('drop talbe[%s] fail'% tablename)
        print('drop table success.')
        # 创建表
        for i, tablename in enumerate(self.tablenames):
            try:
                ddlsql = "create table " + tablename + "("
                for col in self.ddlsqls[i]:
                    ddlsql += col
                ddlsql += ')'
                self.dbcurosr.execute(ddlsql)
            except:
                print("create table [%s] fail. \n sql = %s"% (tablename,ddlsql))

        print('create table success.')
        self.close()

    # 插入数据
    def storeData(self,data):
        if data == None:
            return
        self.connect()
        # bug: 字符串中存在 ' 的插入失败
        try:
            for tablename in self.tablenames:
                for row in data[tablename]:
                    # sql = "insert into testdb." + tablename +" values("
                    # if len(row) >1:
                    #     sql += "'%s'"
                    # loop = len(row) -1
                    # while loop > 0:
                    #     loop -=1
                    #     sql +=",'%s'"
                    # sql +=")"

                    if tablename == 'booklists':
                        try:
                            sql = "insert into booklists VALUES ('%s','%s','%s','%s','%s','%s')" % tuple(row)
                            self.dbcurosr.execute(sql)
                        except:
                            print('store booklist fail.\nsql=%s'%sql)
                        #self.dbcurosr.execute("insert into testdb.booklists VALUES (%s,%s,%s,%s,%s,%s)",
                        #                      ("'"+row[0]+"'","'"+row[1]+"'","'"+row[2]+"'","'"+row[3]+"'","'"+row[4]+"'","'"+row[5]+"'"))
                    elif tablename == 'books':
                        try:
                            sql = "insert into books VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(row)
                            self.dbcurosr.execute(sql)
                            #print('book suc')
                        except:
                            print('store book fail.\nsql=%s'%sql)
                    elif tablename == 'bookdetails':
                        try:
                            sql = "insert into bookdetails VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(row)
                            self.dbcurosr.execute(sql)
                            #print('bookdetail suc')
                        except:
                           print('store bookdetail fail.\nsql=%s'%sql)
                    pass

        except:
            print('store data fail.\n sql = %s'% sql)

        self.close()

    # 关闭dao
    def close(self):
        self.db.close()

