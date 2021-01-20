from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import datetime, re, os, sys


class Function3:
    def __init__(self, now=None):
        self.datas = []
        self.cities = []
        self.times = []
        self.messages = []
        self.now = now

    def getCovidCities(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.implicitly_wait(1000000)
        driver.get("https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679")
        sleep(0.5)
        driver.find_element_by_id("bbs_tr_0_bbs_title").click()
        sleep(0.5)

        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            msg_time = soup.find(attrs={'id': 'sj'}).get_text()
            if self.now == msg_time[0:10]:
                text = soup.find(attrs={'id': 'cn'}).get_text()
                p = re.search('코로나', text)
                p2 = re.search('확진', text)
                p3 = re.search('거리두기', text)
                if p or p2 or p3:
                    self.times.append(msg_time[11:19])
                    self.datas.append(text)
            else:
                driver.quit()
                break
            sleep(0.5)
            driver.find_element_by_id("bbs_gubun").click()
            sleep(0.5)
        self.getCovidText()

    def getCovidText(self):

        first_cities = ['대전', '대구', '울산', '광주', '세종', '제주']
        second_cities = ['서울', '인천', '부산']
        third_cities = ['경기', '강원']
        forth_cities = ['경상', '전라', '충청']
        same_cities = {'부산광역시 강서구': '부산강서', '서울특별시 강서구': '서울강서', '강원도 고성군': '강원고성',
                       '경상남도 고성군': '경남고성', '부산광역시 동구': '부산동', '인천광역시 동구': '인천동',
                       '인천광역시 서구': '인천서', '부산광역시 서구': '부산서', '서울특별시 중구': '서울중', '인천광역시 중구': '인천중',
                       '부산광역시 중구': '부산중', '경기도 광주시': '경기광주'}

        for i in range(len(self.times)):
            times = self.times[i].split(":")
            if int(times[0]) > 12:
                times[0] = int(times[0]) - 12
                self.times[i] = "오후 " + str(times[0]) + "시 " + times[1] + "분 " + times[2] + "초"
            else:
                self.times[i] = "오전 " + str(times[0]) + "시 " + times[1] + "분 " + times[2] + "초"

        path_dir = "Text/Cities"
        if len(self.times) <= len(os.listdir(path_dir)):
            pass
        else:
            for i in range(len(self.datas)):
                start = self.datas[i].index("-송출지역-")
                if self.datas[i][start + 6:] in same_cities:
                    self.cities.append(same_cities[self.datas[i][start + 6:]])
                    self.messages.append(self.datas[i][:start])
                else:
                    if self.datas[i][start + 6:start + 8] in first_cities:
                        self.cities.append(self.datas[i][start + 6:start + 8])
                        self.messages.append(self.datas[i][:start])
                    elif self.datas[i][start + 6:start + 8] in second_cities:
                        self.cities.append(self.datas[i][start + 12:-1])
                        self.messages.append(self.datas[i][:start])
                    elif self.datas[i][start + 6:start + 8] in third_cities:
                        self.cities.append(self.datas[i][start + 10:-1])
                        self.messages.append(self.datas[i][:start])
                    elif self.datas[i][start + 6:start + 8] in forth_cities:
                        self.cities.append(self.datas[i][start + 11:-1])
                        self.messages.append(self.datas[i][:start])
                    else:
                        return

            for i in range(len(self.times)):
                file_name = 'Text/Cities/' + str(i)
                f = open(file_name, 'w', encoding='utf-8-sig')
                f.write(self.cities[i] + '\n' + self.times[i] + '\n' + self.messages[i] + '\n\n')
                f.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        now = datetime.datetime.now().strftime("%Y/%m/%d")
        Function3(now).getCovidCities()
    elif sys.argv[1] == '--demo':
        Function3("2021/01/19").getCovidCities()
