from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import sys, datetime


class Function3:
    def __init__(self, url):
        self.cities = []
        self.times = []
        self.messages = []
        self.url = url

    def getCovidCities(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.implicitly_wait(30)
        driver.get(self.url)
        while True:
            try:
                sleep(1)
                driver.find_element_by_class_name("_more_btn").click()
            except:
                break
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            date = soup.find(attrs={'class': '_selectorText'})
            if datetime.datetime.now().strftime("%Y.%m.%d") != date.get_text()[:10]:
                driver.quit()
                return
            else:
                city = soup.find_all(attrs={'class': 'city'})
                for i in range(len(city)):
                    self.cities.append(city[i].get_text())

                time = soup.find_all(attrs={'class': 'time'})
                for i in range(len(time)):
                    self.times.append(time[i].get_text())

                message = soup.find_all(attrs={'class': 'message'})
                for i in range(len(message)):
                    self.messages.append(message[i].get_text())
        except:
            driver.quit()
            return

        self.getCovidText()
        driver.quit()

    def getCovidText(self):
        sameCities = ['부산 강서구', '서울 강서구', '강원 고성', '경남 고성', '부산 동구', '인천 동구', '인천 서구',
                      '부산 서구', '서울 중구', '인천 중구', '부산 중구', '경기 광주']
        bigCities = ['경기', '서울', '인천', '경남', '경북', '전남', '부산', '강원', '충북', '전북', '중남']
        cities = self.cities[:]
        for i in range(len(self.cities)):
            if self.cities[i] in bigCities:
                pass
            elif self.cities[i] in sameCities:
                if self.cities[i][0:2] == '서울' or self.cities[i][0:2] == '인천' or self.cities[i][0:2] == '부산':
                    filenames = 'Text/Cities/' + str(i)
                    f = open(filenames, 'w', encoding='utf-8-sig')
                    f.write((cities[i].replace(" ", ""))[:-1] + '\n' + self.cities[i] + '\n' \
                            + self.times[i] + '\n' + self.messages[i] + '\n\n')
                    f.close()
                else:
                    filenames = 'Text/Cities/' + str(i)
                    f = open(filenames, 'w', encoding='utf-8-sig')
                    f.write(cities[i].replace(" ", "") + '\n' + self.cities[i] + '\n' + self.times[i] + '\n' + \
                            self.messages[i] + '\n\n')
                    f.close()
            elif self.cities[i][0:2] == '경기' or self.cities[i][0:2] == '경남' or self.cities[i][0:2] == '경북' or \
                    self.cities[i][0:2] == '전남' or self.cities[i][0:2] == '전북' or self.cities[i][0:2] == '충북' or \
                    self.cities[i][0:2] == '충남' or self.cities[i][0:2] == '강원':
                filenames = 'Text/Cities/' + str(i)
                f = open(filenames, 'w', encoding='utf-8-sig')
                f.write(cities[i][3:] + '\n' + self.cities[i] + '\n' + self.times[i] + '\n' + self.messages[i] + '\n\n')
                f.close()
            elif self.cities[i][0:2] == '서울' or self.cities[i][0:2] == '인천' or self.cities[i][0:2] == '부산':
                if self.cities[i] == '인천 강화' or self.cities[i] == '인천 옹진' or self.cities[i] == '부산 기장':
                    filenames = 'Text/Cities/' + str(i)
                    f = open(filenames, 'w', encoding='utf-8-sig')
                    f.write(
                        cities[i][3:] + '\n' + self.cities[i] + '\n' + self.times[i] + '\n' + self.messages[i] + '\n\n')
                    f.close()
                else:
                    filenames = 'Text/Cities/' + str(i)
                    f = open(filenames, 'w', encoding='utf-8-sig')
                    f.write(cities[i][3:-1] + '\n' + self.cities[i] + '\n' + self.times[i] + '\n' + self.messages[
                        i] + '\n\n')
                    f.close()
            elif self.cities[i][0:2] == '세종':  # 네이버에 한칸 띄어져 있음
                filenames = 'Text/Cities/' + str(i)
                f = open(filenames, 'w', encoding='utf-8-sig')
                f.write(cities[i][:2] + '\n' + self.cities[i] + '\n' + self.times[i] + '\n' + self.messages[i] + '\n\n')
                f.close()
            else:
                filenames = 'Text/Cities/' + str(i)
                f = open(filenames, 'w', encoding='utf-8-sig')
                f.write(self.cities[i] + '\n' + self.times[i] + '\n' + self.messages[i] + '\n\n')
                f.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        Function3("https://m.news.naver.com/covid19/live.nhn").getCovidCities()
    elif sys.argv[1] == '--demo':
        Function3("https://m.news.naver.com/covid19/live.nhn?date=20210113").getCovidCities()
