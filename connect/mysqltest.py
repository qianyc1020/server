# coding=utf-8
import pymysql as pymysql

if __name__ == '__main__':
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='Pengyi_9627',
                                 db='chess1',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        sql = "select * from account"
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                print(r["gold"])
    finally:
        connection.close()
