from typing import Counter
import mysql.connector
from mysql.connector import errorcode
import pymysql
import bs4
import requests
import os
import time
import datetime


# cursor.execute("CREATE DATABASE `second`;")

'''cursor.execute("SHOW DATABASES;")
records = cursor.fetchall()
for r in records:
  print(r)'''

# cursor.execute("USE `first`;")


def create_connect():
    config = {
        'host': 'david0970.mysql.database.azure.com',
        'user': 'david0970',
        'password': 'Apple1234',
        'database': 'first',
        'client_flags': [mysql.connector.ClientFlag.SSL],
        'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
    }
    # config = {
    #     'host': '127.0.0.1',
    #     'user': 'root',
    #     'password': '1234',
    #     'database': 'first',
    #     'auth_plugin': 'mysql_native_password'
    # }

    conncetion = mysql.connector.connect(**config)

    return conncetion


def close_connection(conncetion):
    conncetion.commit()
    conncetion.close()


def new_table(room, ip, flow, date, conncetion):
    cursor = conncetion.cursor()
    # sql = 'CREATE TABLE  `test_crawler` (room VARCHAR(6) PRIMARY KEY, ip VARCHAR(15), flow VARCHAR(30))'
    # sql = 'DROP TABLE `test_crawler`'
    # sql = 'SELECT * FROM `test_crawler`;'

    sql = 'INSERT INTO `test_crawler` (room,ip,flow,date) VALUES(\'' + \
        room + '\',\'' + ip + '\',\'' + flow + '\',\'' + date + '\');'
    print(sql)
    cursor.execute(sql)

    records = cursor.fetchall()
    for r in records:
        print(r)


def now_second():
    do = datetime.datetime.now()
    return str(do.second)


def now_hour():
    do = datetime.datetime.now()
    hour = do.hour
    if hour < 10:
        hour = '0' + str(hour)
    return str(hour)


def now_minute():
    do = datetime.datetime.now()
    return str(do.minute)


def today_date():
    localtime = time.localtime(time.time())
    dath = localtime.tm_mday
    if(dath < 10):
        dath = '0'+str(dath)
    return str(dath)


def today_month():
    localtime = time.localtime(time.time())
    month = localtime.tm_mon
    if (month < 10):
        month = '0'+str(month)
    return str(month)


def today_year():
    localtime = time.localtime(time.time())
    year = localtime.tm_year
    return str(year)


def crawler():
    # print(os.getcwd())
    conncetion = create_connect()
    print("call crawler")
    fn = 'file.txt'
    with open(fn) as file_obj:
        file_list = file_obj.readlines()
        req_session = requests.Session()
        for line in file_list:
            while True:
                try:
                    remove_space = line.split(' ')
                    headers = {'content-type': 'text/html; charset=UTF-8',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
                    ip3 = remove_space[1]
                    remove_EOF = remove_space[2].split('\n')
                    ip4 = remove_EOF[0]

                    dath = today_date()
                    month = today_month()
                    year = today_year()
                    hour = now_hour()
                    url = "http://140.130.81.95/cgi-bin/ipquery.cgi?&date=" + \
                        year + month + dath + "&ip3=" + ip3 + "&ip4=" + ip4
                    print(url)
                    response = req_session.get(url)
                    if response.status_code == requests.codes.ok:
                        soup = bs4.BeautifulSoup(response.text, "lxml")
                        result = soup.find_all("td")
                        counter = 0
                        for tag in result:
                            counter += 1
                            if(counter == 4):
                                room = remove_space[0]
                                ip = "10.10." + ip3 + '.' + ip4
                                flow = tag.string
                                print("call new_table()")
                                new_table(room, ip, flow, year +
                                            month + dath + hour, conncetion)
                        if(counter == 0):
                            room = remove_space[0]
                            ip = "10.10." + ip3 + '.' + ip4
                            flow = '0'
                            print("call new_table()")
                            new_table(room, ip, flow, year +
                                        month + dath + hour, conncetion)
                    else:
                        print("Fail to fatch content.")
                except Exception:
                    continue
                break

    close_connection(conncetion)


# crawler()
time.sleep(1)
while(True):
    _ = os.system('cls')
    if(now_minute() == "37"):
        print("do crawler")
        crawler()

    else:
        _ = os.system('cls')
        print(now_hour() + ":" + now_minute() + ":" + now_second() + " " +
              today_year() + "," + today_month() + "," + today_date() + " sleep...")
        time.sleep(3)
