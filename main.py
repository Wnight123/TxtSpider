import Database.dbtool as dbtool
import Spider.spider as spider
import requests
from bs4 import BeautifulSoup
import os
import time

sqlPath = "D:\GitPrj/trunk/config/sql/createDB.sql"
conn = dbtool.connectDB("txt_spider")
dbtool.execSqlFile(conn, sqlPath)


url = 'https://qubook.net/TXT/list1_1.html'
headers = spider.getHeader()
response = requests.get(url, headers=headers)
content = response.content.decode('gbk')
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, 'lxml')
div = soup.find("div", attrs ={'class':'ll1'})
all_li = div.find_all('li')
#print(all_li)
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