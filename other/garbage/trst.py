from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

# driver = webdriver.Chrome()
# driver.get("http://140.130.81.95/cgi-bin/ipquery.cgi?&date=20211217&ip3=66&ip4=31") # 更改網址以前往不同網頁
# driver.close()


fn = 'file.txt'
driver = webdriver.Chrome()
with open(fn) as file_obj:
    for line in file_obj:
        s = line.split(' ')
        # print(s[0] , ' + ', s[1], ' + ', s[2])
        url = "http://140.130.81.95/cgi-bin/ipquery.cgi?&date=20211217&ip3=" + \
            s[1] + "&ip4=" + s[2]
        # url = "http://140.130.81.95/"
        response = driver.get(url)

        result = driver.find_elements_by_tag_name('table')
        result = driver.find_elements_by_tag_name('tr')

        tdlist = result[1].find_elements_by_tag_name('td')
        for col in tdlist:
            print(col.text + '\t', end='')
        if(len(tdlist) > 0):
            print('\n',end='')

        # for row in result:
        #     tdlist = row.find_elements_by_tag_name('td')
        #     for col in tdlist:
        #         print(col.text + '\t', end='')
        #     print('\n')
