from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import os
import time

def getUrl():
    i = [0]         # 不能使用i = 0
    def inner_func():
        i[0] += 1                   # i += 1，表示
        print("***********", i[0], "***********")
        return 'https://www.kuaidaili.com/free/inha/' + str(i[0])
    return inner_func

url = getUrl()

ua = UserAgent()
headers = {'User-Agent': ua.random}

for i in range(0, 100):
    response = requests.get(url(), headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find("tbody")
    all_tr = tbody.find_all('tr')

    for tr in all_tr:
        strlist = tr.text.split('\n')
        ip_port = strlist[1] + ":" + strlist[2]
        proxies = {"http":"http://" + ip_port}
        res = requests.get("https://www.baidu.com", headers=headers, proxies=proxies)
        if res.status_code == 200:
            print(ip_port)
    time.sleep(1)