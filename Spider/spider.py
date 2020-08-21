from fake_useragent import UserAgent
import ProxyPool.proxyPool as ProxyPool
import requests
from bs4 import BeautifulSoup
import os
import time


class QuBookSpider:
    def __init__(self):
        self.proxypool = ProxyPool.ProxyPool(50, 'https://qubook.net/TXT/list1_1.html', 'qubook_ipport.txt')
        self.getproxy = self.proxypool.getProxy()


    def begin(self, startPage=1, endPage=100):
        self.proxypool.startThread()

        for page in range(startPage, endPage+1):
            url = 'https://qubook.net/TXT/list1_{}.html'.format(page)
            headers = {'User-Agent': UserAgent().random}
            response = self.proxypool.get(url, self.getproxy, headers=headers, timeout=3)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'lxml')
            div = soup.find("div", attrs={'class': 'll1'})
            all_li = div.find_all('li')

            for li in all_li:
                dl = "https://qubook.net/"
                name = ""
                writer = ""
                size = ""
                intime = ""
                for tag in li.contents:
                    if tag.name == 'a':
                        dl += tag.attrs['href']

                    if tag.name == 'h1':
                        name = tag.text

                    if tag.name == 'h3':
                        part = tag.text.split('　')
                        writer = part[0]
                        size = part[1]
                        intime = part[2]
                print(name, writer, size, intime, dl)

            time.sleep(1)  # 限制访问频率

        self.proxypool.closeThread()

        print("QuBookSpider, work done")