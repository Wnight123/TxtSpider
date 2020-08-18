import pymysql
import os
import sys
import re

def delcommonds(content):
    out = re.sub(r'(--.*)', '', content)
    out = re.sub(r'/\*.*?\*/', '', out, flags=re.S)
    return out;

def execSqlFile(conn, sqlPath):
    if not os.path.exists(sqlPath):
        return

    file = open(sqlPath, "r", encoding='utf-8')
    content = file.read()
    content = delcommonds(content)
    sqlList = content.split(';')

    # execute() 每次只能执行一条语句，故先按‘;’分割成多条语句，再逐一执行
    cursor = conn.cursor()
    try:
        for sql in sqlList:
            cursor.execute(sql)
            conn.commit()
    except:
        print("execute sql failed")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def connectDB(dbName):
    conn = pymysql.connect(database=dbName,
                           host="127.0.0.1",
                           user="root",
                           password="123456",
                           port=3306,
                           charset='utf8')
    return conn



# traceback = __import__('traceback')
# try:
#     execSqlFile(conn, sqlPath)
# except:
#     traceback.print_exc()

# sqlPath = "D:\GitPrj/trunk/config/sql/createDB.sql"
# conn = connectDB("txt_spider")
# execSqlFile(conn, sqlPath)
