import mysql.connector
from mysql.connector import Error

try:
    # 連接 MySQL/MariaDB 資料庫
    connection = mysql.connector.connect(user='root',
                                         password='1234',
                                         host='127.0.0.1',
                                         database='first',
                                         auth_plugin='mysql_native_password')
    # 查詢資料庫
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id,room,flow,date from test_crawler where room='6401D' ;")

    # 列出查詢的資料
    for (id, room, flow, date) in cursor:
        print("id: %d, room: %s, flow: %s, date: %s" % (id, room, flow, date))


except Error as e:
    print("資料庫連接失敗:", e)

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")
