
# 收集数据，保存与统计显示
import dao


class Outputer(object):

    # 构造函数
    def __init__(self):
        self.datas = []

        #统计
        self.booklistcount = 0;
        self.bookcount = 0;
        self.bookdetailcount = 0;

        self.dao = dao.Dao()

    # 构建数据库
    def build(self):
        self.dao.build()

    # 收集数据并归纳
    def collect_data(self, data):
        if data is None:
            return
        #self.datas.append(data)
        self.dao.storeData(data)

        # 统计
        # 统计书单列表数
        if len(data['booklists']) != 0:
            self.booklistcount += 1
        # 统计书单数
        if len(data['books']) != 0:
            self.bookcount += 1
        # 统计书籍数
        # for bookdetail in  data['bookdetails']:
        #     bookdetailcount += len(bookdetail)
        if len(data['bookdetails']) != 0:
            self.bookdetailcount += 1


    # 保存到mysql 数据库
    def store_data(self):
        pass

    # 读取数据库中结果，并显示相关统计信息，汇总所有的结果
    def show_panel(self):
        # fout = open('output.html', 'w', encoding="utf-8")
        for data in self.datas:
            print('=======================')
            # 书单列表
            for booklist in data['booklists']:
                print("*****booklist*******")
                for x in booklist:
                    print('-----------')
                    print(x)
                if len(booklist) != 0:
                    print('-----------')
            if len(data['booklists']) != 0:
                print('************')
            # 书单
            for book in data['books']:
                print('*****book*******')
                for x in book:
                    print('-----------')
                    print(x)
                if len(booklist) != 0:
                    print('-----------')
            if len(data['books']) != 0:
                print('************')
            # 书籍
            for book in data['bookdetails']:
                print('*****bookdetails*******')
                for x in book:
                    print('-----------')
                    print(x)
                if len(booklist) != 0:
                    print('-----------')
            if len(data['bookdetails']) != 0:
                print('************')
        if len(self.datas) != 0:
            print('=======================')

    # 读取数据库中结果，并显示相关统计信息，汇总所有的结果
    def show_panel2(self):

        # close
        #self.dao.close()

        # booklistcount = 0;
        # bookcount = 0;
        # bookdetailcount = 0;
        # for data in self.datas:
        #     # 统计书单列表数
        #     if len(data['booklists']) != 0:
        #         booklistcount = booklistcount + 1
        #     # 统计书单数
        #     if len(data['books']) != 0:
        #         bookcount += 1
        #     # 统计书籍数
        #     # for bookdetail in  data['bookdetails']:
        #     #     bookdetailcount += len(bookdetail)
        #     if len(data['bookdetails']) != 0:
        #         bookdetailcount += 1


        print("共成功的爬取到\n书单列表：%s\t书单：%s\t书籍：%s"%(self.booklistcount,self.bookcount,self.bookdetailcount))
