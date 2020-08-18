import pymysql

conn = pymysql.connect(database="txt_spider",
                host="127.0.0.1",
                user="root",
                password="123456",
                port=3306,
                charset='utf8')

cursor = conn.cursor()

cursor.close()
conn.close()