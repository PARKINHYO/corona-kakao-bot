from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pytz import timezone
import os, sys, datetime
from webdriver_manager.chrome import ChromeDriverManager

class Function3:
    def __init__(self, now=None):
        self.now = now

    def getCovidCities(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(1000000)
        driver.get("https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679")
        sleep(3)
        driver.find_element_by_id("bbs_tr_0_bbs_title").click()
        sleep(3)
        content = ''
        while True:
            html = driver.page_source
            sleep(3)
            soup = BeautifulSoup(html, 'html.parser')
            sleep(3)
            msg_time = soup.find(attrs={'id': 'sj'}).get_text()
            if self.now == msg_time[0:10]:
                text = soup.find(attrs={'id': 'cn'}).get_text()
                text = '✉' + text + '\n\n'
                print(text)
                content += text
                # self.times.append(msg_time[11:19])
                # self.datas.append(text)
            else:
                driver.quit()
                break
            driver.find_element_by_id("bbs_gubun").click()
            sleep(3)
        return content
