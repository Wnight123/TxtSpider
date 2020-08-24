import Database.dbtool as DbTool
import Spider.spider as Spider
import urllib.parse
import time

# *********************  db ******************
# sqlPath = "D:\GitPrj/trunk/config/sql/createDB.sql"
# conn = DbTool.connectDB("txt_spider")
# DbTool.execSqlFile(conn, sqlPath)



def myUrlencode(url):
    return "http://txt.qubook.net/TXT/" + urllib.parse.quote(url.split('/')[-1])

def showDbData():
    conn = DbTool.connectDB("txt_spider")
    cursor = conn.cursor()
    cursor.execute("select * from qubook where type='玄幻奇幻' and size>6000")
    for record in cursor.fetchall():
        name, writer, type, size, intime, dl = record
        dl = myUrlencode(dl)
        print(name, writer, type, size, intime, dl)
    cursor.close()
    conn.close()

def doSpider(endpage):
    print("pageNum:{}".format(endpage))
    qubookSpider = Spider.QuBookSpider()
    qubookSpider.begin(startPage=23, endPage=endpage)

if __name__ == '__main__':
    str = input("Input page:")
    beginTime = time.time()
    if str.isnumeric():
        doSpider(int(str))
    else:
        showDbData()
    endTime = time.time()
    print("beginTime:{}, endTime:{}, delta:{}".format(beginTime, endTime, endTime-beginTime))

