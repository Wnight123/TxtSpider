import Database.dbtool as dbtool
import Spider.spider as spider
import requests
from bs4 import BeautifulSoup

sqlPath = "D:\GitPrj/trunk/config/sql/createDB.sql"
conn = dbtool.connectDB("txt_spider")
dbtool.execSqlFile(conn, sqlPath)


url = 'https://qubook.net/TXT/list1_1.html'
#url = 'https://www.baidu.com/'
headers = spider.getHeader()
response = requests.get(url, headers=headers)
content = response.content.decode('gbk')
response.encoding = 'gbk'
soup = BeautifulSoup(response.text, 'lxml')
print(soup.contents)