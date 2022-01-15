from typing import Counter
import mysql.connector
from mysql.connector import Error
import pymysql
import bs4
import requests
import os
import time
import datetime


# the id is unique identifier for any row data
id = 0

# cursor.execute("CREATE DATABASE `second`;")

'''cursor.execute("SHOW DATABASES;")
records = cursor.fetchall()
for r in records:
  print(r)'''

# cursor.execute("USE `first`;")

# return id+1 for next row to use


def new_table(id, room, ip, flow, date):
    conncetion = mysql.connector.connect(user='root',
                                         password='1234',
                                         host='127.0.0.1',
                                         database='first',
                                         auth_plugin='mysql_native_password')
    cursor = conncetion.cursor()
    # sql = 'CREATE TABLE  `test_crawler` (room VARCHAR(6) PRIMARY KEY, ip VARCHAR(15), flow VARCHAR(30))'
    # sql = 'DROP TABLE `test_crawler`'
    # sql = 'SELECT * FROM `test_crawler`;'
    temp=str(id)
    sql = 'INSERT INTO `test_crawler` VALUES(\'' + temp + '\',\'' + room + '\',\'' + ip + '\',\'' + flow + '\',\'' + date + '\')'
    # sql = 'UPDATE test_crawler SET flow=\'' + flow + '\' WHERE room=\'' + room + '\''
    print(sql)
    cursor.execute(sql)

    records = cursor.fetchall()
    for r in records:
        print(r)

    conncetion.commit()
    cursor.close()
    conncetion.close()
    id=id+1
    return id




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
    global id
    print("call crawler")
    fn = 'file.txt'
    with open(fn) as file_obj:
        file_list = file_obj.readlines()
        for line in file_list:
            # time.sleep(randint(2,7))
            remove_space = line.split(' ')
            # print(remove_space)
            headers = {'content-type': 'text/html; charset=UTF-8',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
            ip3 = remove_space[1]
            remove_EOF = remove_space[2].split('\n')
            ip4 = remove_EOF[0]
            # print(remove_space[0], " Ip = 10.10." + ip3 + '.' + ip4, end='')

            dath = today_date()
            month = today_month()
            year = today_year()
            hour = now_hour()
            url = "http://140.130.81.95/cgi-bin/ipquery.cgi?&date=" + \
                year + month + dath + "&ip3=" + ip3 + "&ip4=" + ip4
            print(url)
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                soup = bs4.BeautifulSoup(response.text, "lxml")
                # print(soup.prettify())
                result = soup.find_all("td")
                counter = 0
                for tag in result:
                    counter += 1
                    if(counter == 4):
                        room = remove_space[0]
                        ip = "10.10." + ip3 + '.' + ip4
                        flow = tag.string
                        print("call new_table()")
                        # print(room, ip, flow)
                        id = new_table(id, room, ip, flow,
                                       year + month + dath + hour)
                        # print(". Flow = ", tag.string)
                if(counter == 0):
                    room = remove_space[0]
                    ip = "10.10." + ip3 + '.' + ip4
                    flow = '0'
                    # print(room, ip, flow)
                    print("call new_table()")
                    id = new_table(id, room, ip, flow,
                                   year + month + dath + hour)
                    # print(". Flow = ", tag.string)
                    # print(". Flow = 0")
            else:
                print("Fail to fatch content.")

id=input()
id=int(id)
print(id)
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
