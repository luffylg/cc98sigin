import os
import re
import time
from configparser import ConfigParser
from datetime import datetime

from selenium import webdriver


class Site:
    def __init__(self, username, password):
        self.today_executed=False
        self.useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.username = username
        self.password = password
        self.driver = self.getdriver()

    @staticmethod
    def getdriver():
        driver = webdriver.PhantomJS(executable_path='D:\\phantomjscx\\bin\\phantomjs')
        return driver

    def issigin(self):
        self.driver.get('http://www.cc98.org/signin.asp')
        time.sleep(3)
        if '你今天已经签到过了' in self.driver.page_source:
            times = \
            re.findall(r'\d', self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/p[2]').text)[0]
            print('已连续签到{0}天了！'.format(times))
            return True
        return False

    def signin(self):
        if not self.issigin():
            if '没有签到' in self.driver.page_source:
                self.driver.find_element_by_id('content').send_keys('lg')
                self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[5]/td/button').click()
                print('签到中...... ',end='')
                time.sleep(3)
                if not self.issigin():
                    print('出错啦！')
            else:
                print('出错啦！')

    def login(self):
        self.driver.get('http://www.cc98.org/login.asp')
        self.driver.find_element_by_id('userName').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_id('submit').click()
        time.sleep(3)
        if '密码错误' in self.driver.page_source:
            print('密码错误')
            self.driver.quit()

    def run(self):
        print(datetime.now())
        self.driver.get('http://www.cc98.org/index.asp')
        if not self.driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr/td[2]/a[1]'):
            self.login()
        self.signin()

    def re_exe(self, inc=86390):
        # 智障做法
        while True:
            self.run()
            time.sleep(inc)


def getconfig(section, key):
    config = ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '\\user.conf'
    config.read(path)
    return config.get(section, key)

if __name__ == '__main__':
    username = getconfig('user','username')
    password = getconfig('user','password')
    s = Site(username, password)
    # s.re_exe()
    s.run()