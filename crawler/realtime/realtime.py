from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import datetime, sys
# import matplotlib.pyplot as plt
import numpy as np


class Function2:
    def __init__(self, now):
        self.now = now
        self.data = []

    def getCovidRealTime(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(1000000)
        driver.get("https://corona-live.com/")

        self.data.append(datetime.datetime.now().strftime("%Y%m%d%p%I%M%S"))
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for el in soup.find_all(attrs={'class':'value'}):
                print(el.get_text()[1:-1].replace(",",""))
                self.data.append(el.get_text()[1:-1].replace(",",""))    
            self.getCovidText()
            # self.getCovidGraph()
        except NoSuchElementException:
            driver.quit()
            return
        driver.quit()

    def getCovidText(self):
        f = open('/corona-kakao-bot/assets/texts/realtime', 'w')
        f.write(self.data[0] + '\n')
        f.write(self.data[-2] + '\n')
        f.write(self.data[-1] + '\n')
        f.close()

    def getCovidGraph(self):

        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (15, 15)
        plt.rcParams['font.size'] = 20
        plt.rc('font', family='Malgun Gothic')

        dates = []

        for i in range(7, self.now + 1, 2):
            dates.append(str(i) + '시')
        dates.append("현재")
        x = np.array(dates)

        y1 = np.array(list(map(int, self.data[1::2])))
        y2 = np.array(list(map(int, self.data[2::2])))

        fig, ax1 = plt.subplots()
        plt.grid(True, axis='y')
        plt.xticks(fontsize='20')

        line1 = ax1.plot(x, y1, color='grey', marker='o', dash_capstyle='round', dash_joinstyle='round',
                         label='어제 동시간대 확진 환자(단위: 명)', linewidth='3', markersize='10')

        ax2 = ax1.twinx()
        line2 = ax2.plot(x, y2, color='blue', marker='o', dash_capstyle='round', dash_joinstyle='round',
                         label='실시간 확진 환자(단위: 명)', linewidth='3', markersize='10')
        for i, v in enumerate(x):
            #fixme
            ax2.text(v, y2[i], format(int(y2[i]), ","), fontsize=40, color='black', horizontalalignment='center',
                     verticalalignment='bottom')
        #fixme
        if int(self.data[-1]) > int(self.data[-2]):
            ax1.set_ylim(0, (int(self.data[-1])*1.3))
            ax2.set_ylim(0, (int(self.data[-1])*1.3))
        else:
            ax1.set_ylim(0, (int(self.data[-2])*1.3))
            ax2.set_ylim(0, (int(self.data[-2])*1.3))
        ax1.set_yticklabels([])

        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=30)

        fig.savefig('Image/function2.png')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        now = int(datetime.datetime.now().strftime("%H"))
        Function2(now).getCovidRealTime()
    elif sys.argv[1] == '--demo':
        Function2(22).getCovidRealTime()
