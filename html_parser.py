
from bs4 import BeautifulSoup
from urllib import parse
#引入正则模块
import re


# 解析网页中的内容
class HtmlParser(object):


    # 获得新的url
    # /booklist/detail/
    def __get_new_urls(self,page_url,soup):
        new_urls = set()
        # 获取书单url
        if re.match(r'.*/booklist/$',page_url) or re.match(r'.*/booklist/latest',page_url):
            links = soup.find_all('a',href = re.compile(r'^/booklist/detail/[0-9]+'))
            for link in links:
                new_url = link['href']
                new_full_url = "http://book.qidian.com" + new_url
                new_urls.add(new_full_url)

        # 获取书单中的书籍url
        if re.match(r'.*/booklist/detail.*',page_url):
            links = soup.find_all('a',href = re.compile(r'^//book.qidian.com/info/[0-9]+'))
            for link in links:
                new_url = link['href']
                new_full_url = "http:" + new_url
                new_urls.add(new_full_url)

        # 返回连接
        return new_urls

    # 获取网页的数据
    def __get_new_data(self,page_url,soup):
        # 返回一个字典对象
        res_data = {}
        # 字典中的内容
        booklists = []
        books = []
        bookdetails = []
        # 处理书单列表
        if re.match(r'.*/booklist/$',page_url) or re.match(r'.*/booklist/latest',page_url):
            booklistnodes = soup.find_all('div',class_ = 'info-wrap')
            for i,booklistnode in enumerate(booklistnodes):
                # print(booklistnode)
                try:
                    booklistnode = repr(booklistnode)
                    inner_soup = BeautifulSoup(booklistnode, 'html.parser')
                    # 书单id
                    booklistid = inner_soup.find('a',{'data-eid':'qd_Q06'})
                    booklistid = booklistid['href']
                    #print('xxx')
                    booklistid = re.search(r'\d+',booklistid).group(0)
                    #print('xxxxx')
                    # 书单名
                    title = inner_soup.find('h3').get_text().strip()
                    # 书单简介
                    content = inner_soup.find('p').get_text().strip()
                    #print('xxxxddx')
                    # 关注
                    # 额外处理 空关注
                    attention = inner_soup.find('a',class_ = 'attention ').get_text().strip()
                    attention = re.findall(r'\d+',attention)
                    if len(attention) == 0:
                        attention = 0
                    else:
                        attention = attention[0]
                    # 书单中的书的总数
                    # 额外处理 空
                    count = inner_soup.find('b').get_text().strip()
                    count = re.findall(r'\d+', count)
                    if len(count) == 0:
                        count = 0
                    else:
                        count = count[len(count)-1]
                    # 书单连接
                    url = 'http://book.qidian.com/booklist/detail/' + booklistid

                    booklist = [booklistid,title,content,attention,count,url]
                    booklists.append(booklist)
                except:
                    print('parse booklistnode fail')
                    print(booklistid,'|',title,'|',content,'|',attention[0],'|',count[len(count)-1],'|',url)

        #print('xxx')
        # 处理书单页面
        # bug:只处理了第一页的书籍，没有处理剩余页的内容
        if re.match(r'.*/booklist/detail.*',page_url):
            booknodes = soup.find('div',class_='detail-content-list').find_all('dd')
            for booknode in booknodes:
                try:
                    booknode = repr(booknode)
                    inner_soup = BeautifulSoup(booknode, 'html.parser')
                    bookid = inner_soup.find('a',class_ = 'j-bookName')['href']
                    # 书籍id
                    bookid = re.findall(r'\d+',bookid)
                    bookid = bookid[0]
                    # 书籍名
                    bookname = inner_soup.find('a',class_ = 'j-bookName').get_text().strip()
                    # 作者名
                    writer = inner_soup.find('a',class_ = 'writer').get_text().strip()
                    # 类型
                    #
                    # 简介
                    intro = inner_soup.find('p',class_='intro').get_text().strip()
                    # 推荐理由
                    quote = inner_soup.find('div',class_='quote').get_text().strip()
                    # 喜欢人数
                    heart = inner_soup.find('a',class_='heart ').get_text().strip()
                    # 还有  人喜欢的
                    heart = re.search(r'\d+', heart)
                    if heart:
                        heart = heart.group(0)
                    else:
                        heart = 0
                    # booklistid
                    booklistid = re.search(r'\d+',page_url).group(0)

                    # 书籍链接
                    url = 'http://book.qidian.com/info/'+ bookid

                    book = [bookid,bookname,writer,intro,quote,heart,booklistid,url]
                    books.append(book)
                except:
                    print('parse booknode fail.')
                    print(bookid,'|',bookname,'|',writer,'|',intro,'|',quote,'|',heart,'|',booklistid,'|',url)


        # 处理书籍页面
        if re.match(r'.*/info/.*',page_url):
            try:
                bookdetail = soup.find('div',class_='book-detail-wrap center990')
                bookinfo = soup.find('div',class_='book-info ')
                # 书id
                bookdetailid = bookinfo.find('a',class_='red-btn J-getJumpUrl ')['data-bid']
                # 书名
                bookname = bookinfo.find('h1').find('em').get_text()
                # 作者
                writer = bookinfo.find('a',class_='writer').get_text()
                # 类型
                booktype = bookinfo.find('a',{'data-eid':'qd_G10'}).get_text()
                # 数据
                bookstat = bookinfo.find_all('p')[2].get_text()
                bookstat = bookstat.split('|')
                # 字数
                wordcount = bookstat[0]
                if re.match(r'.*万字.*',wordcount):
                    wordcount = re.findall(r'\d+',wordcount)[0] + ' * 10000'
                    wordcount = eval( wordcount)
                else:
                    wordcount = eval(re.findall(r'\d+')[0])
                # 点击
                clickcount = bookstat[1]
                if re.match(r'.*万总.*',clickcount):
                    clickcount = eval(re.findall(r'\d+',clickcount)[0] +'* 10000' )
                else:
                    clickcount = eval(re.findall(r'\d+',clickcount)[0])
                # 推荐
                recommandcount = bookstat[2]
                if re.match(r'.*万总.*', recommandcount):
                    recommandcount = eval(re.findall(r'\d+',recommandcount)[0] + '* 10000')
                else:
                    recommandcount = eval(re.findall(r'\d+',recommandcount)[0])

                # 评分
                bookscore = bookdetail.find('h4',{'id':'j_bookScore'}).get_text()

                # 章数
                catalogcount = bookdetail.find('span',{'id':'J-catalogCount'}).get_text()
                catalogcount = re.findall(r'\d+',catalogcount)[0]

                # 简介
                bookinfodetail = bookdetail.find('div',class_='book-info-detail')
                bookintro = bookinfodetail.find('div',class_ ='book-intro' ).get_text().strip()

                # url
                url = page_url

                #
                bookinfodet = [bookdetailid,bookname,writer,booktype,wordcount,catalogcount,
                               clickcount,recommandcount,bookscore,
                               bookintro,url]
                bookdetails.append(bookinfodet)

            except:
                print('parse bookdetailnode fail.')
                print(bookdetailid,'|',bookname,'|',writer,'|',booktype,'|',wordcount,'|',catalogcount,'|',
                               clickcount,'|',recommandcount,'|',bookscore,'|',
                               bookintro,'|',url)

        # 保存到返回结果
        res_data['booklists'] = booklists
        res_data['books'] = books
        res_data['bookdetails'] = bookdetails
        # 返回结果
        return res_data


    # 解析
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        #print("begin parse...")
        soup = BeautifulSoup(html_cont, 'html.parser')
        #print("begin get_urls...")
        try:
            new_urls = self.__get_new_urls(page_url, soup)
        except:
            print('parse new urls fail.')
        #print("begin get_data...")
        try:
            new_data = self.__get_new_data(page_url, soup)
        except:
            print('parse new datas fail.')
        #print("end get_parse...")

        return new_urls, new_data