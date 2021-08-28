from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import datetime, time
from pytz import timezone

class Function2:
    def __init__(self):
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
        time.sleep(5)
        seoul_timezone = timezone('Asia/Seoul')
        self.data.append(datetime.datetime.now(seoul_timezone).strftime("%Y%m%d%p%I%M%S"))
        try:
            html = driver.page_source
            time.sleep(5)
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(5)
            for el in soup.find_all(attrs={'class':'value'}):
                print(el.get_text()[1:-1].replace(",",""))
                self.data.append(el.get_text()[1:-1].replace(",",""))  
            diff = int(self.data[-1]) - int(self.data[-2])
            if diff >= 0:
                diff = '↑ ' + str(format(diff, ","))
            else:
                diff = '↓ ' + str(format(diff, ","))[1:]
            
            content = '**⌚ ' + str(self.data[0][:4]) + '년 ' + \
                str(self.data[0][4:6]) + '월 ' + str(self.data[0][6:8]) + '일 ' + \
                    str(self.data[0][8:10]) + ' ' + str(self.data[0][10:12]) + '시 ' + \
                        str(self.data[0][12:14]) + '분 ' + \
                            str(self.data[0][14:]) + '초**\n' + \
                                '😷 실시간 확진자 ' + format(int(self.data[-1]), ",") + \
                                    '명\n🔍 어제 동시간 대비 ' + diff + '\n\n'
            return content
                
        except NoSuchElementException:
            driver.quit()
            return
        driver.quit()
