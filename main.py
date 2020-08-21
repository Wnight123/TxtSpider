import Database.dbtool as DbTool
import Spider.spider as Spider

# *********************  db ******************
sqlPath = "D:\GitPrj/trunk/config/sql/createDB.sql"
conn = DbTool.connectDB("txt_spider")
DbTool.execSqlFile(conn, sqlPath)

# *********************  proxy ******************
qubookSpider = Spider.QuBookSpider()
qubookSpider.begin(endPage=10)



