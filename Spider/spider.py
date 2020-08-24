from fake_useragent import UserAgent
import ProxyPool.proxyPool as ProxyPool
import pymysql
import requests
from bs4 import BeautifulSoup
import os
import time
import traceback

"""
目标网站： 
    pc版:qubook.net/         手机版:m.qubook.net
分析：
    https://www.qubook.net/TXT/list{第N类数据,无规律,可枚举}_{第M页,有规律}.html
    --> 含N本小说的数据：名字、作者、数据大小、入库时间、简述；但不含 小说类型
        detailurl(PC) :https://qubook.net//TXT/down_{数值}.html
        detailurl(MB) :https://m.qubook.net//TXT/down_{数值}.html
        
    --> detailurl(PC)页面：名字、作者、数据大小、小说类型、入库时间、简述、rar下载链接
        detailurl(MB)页面：名字、作者、数据大小、小说类型、入库时间、简述、txt下载链接
        注意：名字格式可能为; 名字 或 “名字 完结*”，须做处理
    --> txt下载链接格式为以下其中一种
        http://txt.qubook.net/TXT/小说名.txt
        http://txt.qubook.net/TXT/小说名_作者名字后两个字.txt
        注意：小说名不包括后面可能存在的 “完结、番外” 等词
        eg:
            太初  高楼大厦 http://txt.qubook.net/TXT/太初_大厦.txt
            剧透诸天万界[综]  双子座游鱼 http://txt.qubook.net/TXT/剧透诸天万界.txt
        
1、可构造 detailurl(MB)，若可访问且有数据，则解析
2、用一列表枚举第N类数据，之后遍历该列表，构造该类数据第N页的url来访问
    2_1、选择一：解析该页面下的小说数据，并构造可能的txt下载链接       一页可得20条数据，只需访问1次url,下载链接不一定有效
    2_2、选择二：解析得到detailurl(MB)/(PC),再进行访问，再解析        一页可得20条数据，须访问 1+20 次url，数据准确

"""
class QuBookSpider:
    def __init__(self):
        self.proxypool = ProxyPool.ProxyPool(50, 'https://qubook.net/TXT/list1_1.html', 'qubook_ipport.txt')
        self.getproxy = self.proxypool.getProxy()


    def begin(self, startPage=1, endPage=100):
        if endPage <= 0:
            return;

        self.proxypool.startThread()
        conn = pymysql.connect(database="txt_spider",
                               host="127.0.0.1",
                               user="root",
                               password="123456",
                               port=3306,
                               charset='utf8')
        cursor = conn.cursor()
        insertSql = "replace into qubook(name, writer, type, size, intime, dl) values(%s, %s, %s, %s, %s, %s)"
        datalist = []
        try:
            for page in range(startPage, endPage + 1):
                print("begin spider page:{}".format(page))

                url = 'https://qubook.net/TXT/list1_{}.html'.format(page)
                headers = {
                    'User-Agent': UserAgent().random,
                    'accept-language': 'zh-CN,zh;q=0.9'
                }
                res = self.proxypool.get(url, self.getproxy, headers=headers, timeout=3)
                if res.status_code != 200:
                    continue

                res.encoding = 'gbk'
                soup = BeautifulSoup(res.text, 'lxml')
                div = soup.find("div", attrs={'class': 'll1'})
                all_li = div.find_all('li')

                for li in all_li:
                    dtlUrl = "https://m.qubook.net/"
                    name = ""
                    writer = ""
                    type = ""
                    size = 0
                    intime = ""
                    dl = ""

                    for tag in li.contents:
                        if tag.name == 'a':
                            dtlUrl += tag.attrs['href']

                        if tag.name == 'h1':
                            name = tag.text

                        if tag.name == 'h3':
                            h3_list = tag.text.split('　')
                            writer = h3_list[0].split(':')[-1]
                            intime = h3_list[2].split(':')[-1]
                            size_list = h3_list[1].split(':')[-1].split(' ')
                            if size_list[1] == "MB":
                                size = int(float(size_list[0]) * 1024)
                            else:
                                size = int(float(size_list[0]))

                    if dtlUrl != "":
                        dtlRes = self.proxypool.get(dtlUrl, self.getproxy, headers=headers, timeout=3)
                        if dtlRes.status_code != 200:
                            continue

                        dtlRes.encoding = 'gbk'
                        dtlSoup = BeautifulSoup(dtlRes.text, 'lxml')
                        div_listcd = dtlSoup.find("div", attrs={'class': 'listcd'})
                        type = div_listcd.text.split(' ')[-2]

                        div_qd = dtlSoup.find("div", attrs={'class': 'qd'})
                        div_qd_a = div_qd.find_all('a')
                        dl = div_qd_a[2].attrs['href']

                    data = (name, writer, type, size, intime, dl)
                    datalist.append(data)
                    print(name, writer, type, size, "kb", intime, dl)

                cursor.executemany(insertSql, datalist)
                conn.commit()
                datalist.clear()

                time.sleep(1)  # 限制访问频率
        except Exception as e:
            traceback.print_exc()
            print(e)
            conn.rollback()
        finally:
            self.proxypool.closeThread()
            cursor.close()
            conn.close()
            print("QuBookSpider, work done")