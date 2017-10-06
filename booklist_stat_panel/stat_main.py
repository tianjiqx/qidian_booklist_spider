
##########################################
#
# 程序功能：
#   书单推荐模块，
# 根据书单数据库，显示各种感兴趣的书籍推荐
# 已提供推荐：
# 1.top15 最多人关注的书单
# 2.top30 最多被书单收集的书
# 3.top50 最多人喜欢的书
# 4.top20 最多作品被收集的作者的书
#
##########################################

import stat_dao
import re

class StatPanel:

    # 构造函数
    def __init__(self):

        # 获取书单数据库访问接口
        self.dao = stat_dao.StatDao()


        pass

    # 显示所有的推荐书单
    def all_panel(self):

        self.most_attention_panel()
        self.most_collected_books()
        self.most_heart_panel()
        self.most_worker_collected_panel()
        pass

    # 显示最多人关注的书单
    def most_attention_panel(self):
        # 打开文件
        # w	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
        fout = open('../output/Top15最多人关注的书单.txt', 'w', encoding="utf8")

        # 获取数据
        datas = self.dao.stat_most_attentions()

        #处理数据
        str = "\n  ☆☆☆§ Top15最多人关注的书单 §☆☆☆ \n"
        for booklist in datas:
            decorate ='\n=======================================\n'
            block = '''
书单ID：%s
书单标题：《%s》
推荐说明：
%s
关注数：%s
书单包含书籍总数：%s
地址：%s\n''' % tuple(booklist)

            str += decorate + block + decorate

        # 写入文件
        fout.write(str)

        #关闭文件
        fout.close()

    # 最多被书单收藏的书
    def most_collected_books(self):
        # 打开文件
        # w	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
        fout = open('../output/Top30最多被书单收藏的书.txt', 'w', encoding="utf8")

        # 获取数据
        datas = self.dao.stat_most_collected_books()

        # 处理数据
        str = "\n  ☆☆☆§ Top30最多被书单收藏的书 §☆☆☆ \n"
        for book in datas:
            decorate = '\n=======================================\n'
            block = '''
书籍ID：%s
书名：《%s》
作者：%s
简介：
%s
推荐理由：
%s
喜欢的人数：%s
被书单收藏次数：%s
地址：%s\n''' % tuple(book)

            str += decorate + block + decorate

        # 写入文件
        fout.write(str)

        # 关闭文件
        fout.close()

    # top50 最多人喜欢的书
    def most_heart_panel(self):
        # 打开文件
        # w	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
        fout = open('../output/Top50最多人喜欢的书.txt', 'w', encoding="utf8")

        # 获取数据
        datas = self.dao.stat_most_hearts()

        # 处理数据
        str = "\n  ☆☆☆§ Top50最多人喜欢的书 §☆☆☆ \n"
        for book in datas:
            decorate = '\n=======================================\n'
            block = '''
书籍ID：%s
书名：《%s》
作者：%s
简介：
%s
推荐理由：
%s
喜欢的人数：%s
被书单收藏次数：%s
地址：%s\n''' % tuple(book)

            str += decorate + block + decorate

        # 写入文件
        fout.write(str)

        # 关闭文件
        fout.close()

    # top20 最多作品被收集的作者(不去重)
    def most_worker_collected_panel(self):
        # 打开文件
        # w	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
        fout = open('../output/Top20最多作品被收藏的作者(不去重).txt', 'w', encoding="utf8")

        # 获取数据
        datas = self.dao.stat_most_woker_collecteds()

        # 处理数据
        str = "\n  ☆☆☆§ Top20最多作品被收藏的作者(不去重) §☆☆☆ \n"
        for book in datas:
            decorate = '\n=======================================\n'
            block = '''
作者：%s
书籍IDs：%s
书名s：《%s》
简介s：
%s
推荐理由：
%s
喜欢的人数：%s
被书单收藏次数：%s
地址s：
%s\n''' % tuple(book)

            str += decorate + block + decorate

        # 写入文件
        fout.write(str)

        # 关闭文件
        fout.close()



if __name__ == '__main__':

    obj_stat_panel = StatPanel()
    # 显示全部推荐
    obj_stat_panel.all_panel()
