
# from qidain_booklist_spider import url_manager
# from qidain_booklist_spider import html_downloader
# from qidain_booklist_spider import outputer
# from qidain_booklist_spider import html_parser

###############################################
# 程序说明：
#   本程序的功能是爬取起点书单，并保持下来
#   当前支持的功能：
#   从入口http://book.qidian.com/booklist/和http://book.qidian.com/booklist/laest开始
#   爬取书单列表booklist，对应书单book和书籍详细介绍bookdetail，并且解析和存储到mysql中
#   下一阶段需要开发的功能:
#   1.读取保存下来的数据，并按照各种指标选择推荐的书籍和书单(独立的子程序) --已完成4张榜单
#   2.程序执行速度加快(多进、线程化) --多进程方法存在进程间通信不明之处，且多进程利于cpu密集型，已经改为多线程版本
#
#   3.程序爬取内容的增多(当前只能爬取2个书单列表，但是我们可从2个方面来增加爬取的内容:a.生成书单id，b.根据用户收藏书单列表，扩大书单列表)
#   4.程序使用bloomfilter 加快已爬取和未爬取链接的验证(爬取链接过万后url管理需要更好的技术)
#   5.使用代理ip技术避免被封掉ip
#   6.尝试其他数据库，是否有更好的替代数据库，提升写入和读取性能
#   7.使用爬虫框架
#
###############################################

# -*- coding: utf-8 -*-


import url_manager
import html_downloader
import outputer
import html_parser
import time
import sys
from multiprocessing import Process, Semaphore, RLock,Lock, Queue,Value,sharedctypes
from multiprocessing.managers import BaseManager


import threading
import os

# MANAGER_PORT = 34590
# MANAGER_DOMAIN = '127.0.0.1'.encode()
# MANAGER_AUTH_KEY = 'ABC'.encode()

class SpiderMain(threading.Thread):

    #构造函数
    def __init__(self,i,url_manager,lock,outputer):
        # Process.__init__(self)
        self.process_no = i

        self.urls = url_manager
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = outputer
        # 第一个进程构建数据库
        if i == 0:
            self.outputer.build()
        # 锁
        self.lock = lock
        threading.Thread.__init__(self)

    def craw(self):
        #global lock
        count = 0
        max_count = 1000
        fail_count = 0

        new_url = None # 新待爬取的url
        t1 = time.time()
        # 进程前缀
        pre_print = "Thread_no-"+str(self.process_no)+' '
        while True:
            print(pre_print,'entry while loop')

            try:
                self.lock.acquire()
                try:
                    new_url = self.urls.get_new_url(self.process_no)
                except:
                    print(sys.exc_info()[0])
                    self.lock.release()
                    break

                is_new_url = self.urls.has_new_url(self.process_no)
                self.lock.release()

                if not is_new_url and new_url == None:
                    print(pre_print,'sleep 30s zzzzzzz')
                    # 休息30s后检测
                    time.sleep(30)
                    print(pre_print,"zzzzzzz end")
                    self.lock.acquire()
                    try:
                        is_new_url = self.urls.has_new_url(self.process_no)
                    except:
                        print(pre_print,"has_new_url wrong")
                    self.lock.release()
                    print('是否还有新的url连接？',is_new_url)


                    if is_new_url and (new_url == None):
                        self.lock.acquire()
                        try:
                            new_url = self.urls.get_new_url(self.process_no)
                        except:
                            print(pre_print,"get_new_url fail")
                        print(new_url)
                        self.lock.release()
                        pass
                    else:
                        # 确实没有新的任务，该进程可以退出了
                        print('没有任务了！')
                        break


                # 退出限定
                if (count >= max_count) or (new_url == None):
                    break
                # 已爬取网页数目累计
                count = count + 1
                print(pre_print+"craw %d : %s begin！" % (count, new_url))

                #continue
                try:
                    # 下载网页
                    starttime = time.time()
                    html_cont = self.downloader.download(new_url)
                    endtime = time.time()
                    print(pre_print+"download success, spend time %s s"% (endtime-starttime))
                    # 新增待爬的网页list和本页的数据
                    starttime = time.time()
                    new_urls, new_data = self.parser.parse(new_url, html_cont)
                    endtime = time.time()
                    print(pre_print+"parse success, spend time %s s"% (endtime-starttime))
                except:
                    print('error! download new url or parse data')

                self.lock.acquire()
                try:
                    # 加入待爬取得网页
                    starttime = time.time()
                    self.urls.add_new_urls(new_urls)
                    endtime = time.time()
                    print(pre_print+"add new url success, spend time %s s"% (endtime-starttime))
                    # 收集数据（存储）
                    starttime = time.time()
                    self.outputer.collect_data(new_data)
                    endtime = time.time()
                    print(pre_print+"collect succsess, spend time %s s"% (endtime-starttime))
                except:
                    print('error! add new url or collect data')
                self.lock.release()

            except :
                # 爬取失败的网页
                print(sys.exc_info()[0])
                fail_count = fail_count + 1
                print(pre_print+"No.%d craw [%s] failed! " % (fail_count, new_url))
                #break

        t2 = time.time()
        # 显示最终的爬取结果统计
        #self.outputer.show_panel()
        self.outputer.show_panel2()
        # 显示爬取情况
        print(pre_print+"total fail count %d total %d  spend time :%f s" % (fail_count, count,(t2-t1)))

    # 执行
    def run(self):
        self.craw()
        pass


#自定义manager,进程通信
class MyManager(BaseManager):
    pass

MyManager.register('UrlManager',url_manager.UrlManager)

if __name__ == '__main__':
    lock = threading.RLock()
    # 进程数
    thread_num = 15
    # 全局的url管理器
    global_url_manager = url_manager.UrlManager(thread_num)

    # mutiprocess Manager
    my_Manager = MyManager();
    my_Manager.start()
    # server = my_Manager.get_server()
    # server.serve_forever()

    #global_url_manager = my_Manager.UrlManager(thread_num);


    # 数据库访问
    op = outputer.Outputer()
    root_urls = ["http://book.qidian.com/booklist/",
                "http://book.qidian.com/booklist/latest"]

    # 初始化起始的网址
    for url in root_urls:
        global_url_manager.add_new_url(url)

    # for i in range(thread_num):
    #     for url in global_url_manager.new_urls[i]:
    #         print(i,' : ',url)

    # 发起各进程
    for i in range(thread_num):
        p = SpiderMain(i,global_url_manager,lock,op)
        p.start()
        time.sleep(3)
