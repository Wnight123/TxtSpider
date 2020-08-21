from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import time
import os
import threading


class ProxyPool:
    def __init__(self, setSize=100, testurl='https://www.baidu.com', filename='ip_port.txt'):
        self.ip_port_set = set()
        self.fileName = filename
        self.testurl = testurl
        self.setSize = setSize
        self.updateFlag = False
        self.update = None
        self.initSet()

    def startThread(self):
        if self.update == None:
            self.updateFlag = True
            self.update = threading.Thread(target=self.updateSet)
            self.update.start()

    def closeThread(self):
        while len(self.ip_port_set) != self.setSize:
            time.sleep(3)
        self.updateFlag = False
        self.update.join()
        self.update = None

    def getUrl(self):
        i = [0]
        def inner_func():
            i[0] += 1
            return 'https://www.kuaidaili.com/free/inha/{}'.format(i[0])
        return inner_func

    def initSet(self):
        if os.path.exists(self.fileName):
            file = open(self.fileName, 'r')
            lines = file.readlines()
            for line in lines:
                self.ip_port_set.add(line.strip())
            file.close()
        else:
            url = self.getUrl()
            headers = {'User-Agent': UserAgent().random}

            done = False
            while not done:
                response = requests.get(url(), headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')

                tbody = soup.find("tbody")
                all_tr = tbody.find_all('tr')
                for tr in all_tr:
                    strlist = tr.text.split('\n')
                    ip_port = strlist[1] + ":" + strlist[2]
                    if ip_port in self.ip_port_set:
                        continue

                    proxies = {"http": "http://" + ip_port}
                    try:
                        res = requests.get(self.testurl, headers=headers, proxies=proxies, timeout=1)
                        if res.status_code == 200:
                            self.ip_port_set.add(ip_port)
                            # time.sleep(1)
                            if len(self.ip_port_set) == self.setSize:
                                done = True
                                print("ip_port_set init done, set size", len(self.ip_port_set))

                                file = open(self.fileName, "w")
                                file.write('\n'.join(self.ip_port_set))
                                file.close()

                                break;
                    except:
                        continue;

                print("init ip_port_set, cur set size:", len(self.ip_port_set))

    def getProxy(self):
        i = [0]
        ip_port_arr = []
        for v in self.ip_port_set:
            ip_port_arr.append(v)

        def inner_func():
            i[0] = i[0] % len(ip_port_arr) + 1;
            return {"http": "http://" + ip_port_arr[i[0] - 1]}

        return inner_func

    def updateSet(self):
        while self.updateFlag:
            if len(self.ip_port_set) < self.setSize:
                getUrl = self.getUrl()
                headers = {'User-Agent': UserAgent().random}

                done = False
                while not done:
                    url = getUrl()
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.text, 'lxml')
                    tbody = soup.find("tbody")

                    try:
                        all_tr = tbody.find_all('tr')
                        for tr in all_tr:
                            strlist = tr.text.split('\n')
                            ip_port = strlist[1] + ":" + strlist[2]
                            if ip_port in self.ip_port_set:
                                continue

                            proxies = {"http": "http://" + ip_port}
                            try:
                                res = requests.get(self.testurl, headers=headers, proxies=proxies, timeout=1)
                                if res.status_code == 200:
                                    self.ip_port_set.add(ip_port)
                                    # time.sleep(1)
                                    if len(self.ip_port_set) == self.setSize:
                                        done = True
                                        print("ip_port_set update done, set size", len(self.ip_port_set))

                                        file = open(self.fileName, "w")
                                        file.write('\n'.join(self.ip_port_set))
                                        file.close()

                                        break;
                            except:
                                print("timeout: ", ip_port)
                                continue
                    except:
                        print("网页异步加载，取不到数据， url:", url)
                        continue

                    print("update ip_port_set, cur set size:", len(self.ip_port_set))

            time.sleep(5)

    def get(self, url, getproxy, **kwargs):
        while True:
            try:
                proxies = getproxy()
                response = requests.get(url, proxies=proxies, **kwargs)
                return response
            except requests.exceptions.RequestException as e:
                print(e)
                ip_port = proxies['http'].split('/')[2]
                self.ip_port_set.remove(ip_port)
                print("cur set size", len(self.ip_port_set))





# proxytool = ProxyTool(10)
# proxy = proxytool.getProxy()
# for i in range(0,11):
#     print(proxy())


