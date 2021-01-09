import requests, xmltodict, json, datetime
import matplotlib.pyplot as plt
import numpy as np


<<<<<<< HEAD
def getCovidKR(end_day: str, start_day: str) -> (str, str, str, str, List[int], List[int]):
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'

    # ServiceKey는 url decode 한 값임.
    payload = {'ServiceKey': 'service_key',
               'startCreateDt': start_day, 'endCreateDt': end_day, }
    res = requests.get(url, params=payload)
    if (res.status_code == 200):
        # Ordered dictionary type
        result = xmltodict.parse(res.text)
        # dictionlay type
        dd = json.loads(json.dumps(result))
        # print(dd)

        sums = []
        adds = []

        date = dd['response']['body']['items']['item'][0]['stateDt']
        death = dd['response']['body']['items']['item'][0]['deathCnt']
        treatment = dd['response']['body']['items']['item'][0]['careCnt']
        complete = dd['response']['body']['items']['item'][0]['clearCnt']

=======
class Function1:
    def __init__(self):
        self.date = '20210101'
        self.sums = []
        self.adds = []
        self.complete = '0'
        self.completeDiff = 0
        self.treatment = '0'
        self.treatmentDiff = 0
        self.death = '0'
        self.deathDiff = 0

    def getCovidKR(self, end_day: str, start_day: str):
        url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
        payload = {
            'ServiceKey': 'service_key',
            'startCreateDt': start_day, 'endCreateDt': end_day, }
        res = requests.get(url, params=payload)
        if (res.status_code == 200):
            result = xmltodict.parse(res.text)
            dd = json.loads(json.dumps(result))

            self.date = dd['response']['body']['items']['item'][0]['stateDt']
            for i in range(6, -1, -1):
                self.sums.append(int(dd['response']['body']['items']['item'][i]['decideCnt']))
                self.adds.append(int(dd['response']['body']['items']['item'][i]['decideCnt']) - int(
                    dd['response']['body']['items']['item'][i + 1]['decideCnt']))
            self.complete = dd['response']['body']['items']['item'][0]['clearCnt']
            self.completeDiff = int(dd['response']['body']['items']['item'][0]['clearCnt']) - \
                                int(dd['response']['body']['items']['item'][1]['clearCnt'])
            self.treatment = dd['response']['body']['items']['item'][0]['careCnt']
            self.treatmentDiff = int(dd['response']['body']['items']['item'][0]['careCnt']) - \
                                 int(dd['response']['body']['items']['item'][1]['careCnt'])
            self.death = dd['response']['body']['items']['item'][0]['deathCnt']
            self.deathDiff = int(dd['response']['body']['items']['item'][0]['deathCnt']) - \
                             int(dd['response']['body']['items']['item'][1]['deathCnt'])

        else:
            print('res.status_code is NOT ok')
            return

        self.getCovidTxt()
        self.getCovidGraph()

    def getCovidTxt(self):
        f = open("Text/func1data.txt", 'w')
        f.write(self.date + '\n')
        f.write(str(self.sums[-1]) + '\n')
        f.write(str(self.adds[-1]) + '\n')
        f.write(self.complete + '\n')
        f.write(str(self.completeDiff) + '\n')
        f.write(self.treatment + '\n')
        f.write(str(self.treatmentDiff) + '\n')
        f.write(self.death + '\n')
        f.write(str(self.deathDiff) + '\n')
        f.close()

    def getCovidGraph(self):
        # 1. 기본 스타일 설정
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (20, 20)
        plt.rcParams['font.size'] = 20
        plt.rc('font', family='Malgun Gothic')

        # 2. 데이터 준비
        dates = []
        today = datetime.datetime.now()
<<<<<<< HEAD
>>>>>>> d64ce0b... Update CoronaBot.
        for i in range(13, -1, -1):
=======
        for i in range(6, -1, -1):
>>>>>>> 9ecdb3e... Update CoronaBot
            dates.append((today - datetime.timedelta(i)).strftime("%m.%d"))
        x = np.array(dates)
        y1 = np.array(self.adds)
        y2 = np.array(self.sums)

        # print(dates, adds, sums)

        # 3. 그래프 그리기
        fig, ax1 = plt.subplots()
        plt.grid(True, axis='y')
        plt.xticks(fontsize='35')

        ax1.bar(x, y2, color='blue', alpha=0.7, width=0.7, label='누적 확진환자(단위: 명)')
        ax1.set_ylim(0, 80000)
        ax1.legend(loc='upper left', fontsize=30)
        for i, v in enumerate(x):
            ax1.text(v, y2[i], y2[i], fontsize=35, color='blue', horizontalalignment='center',
                     verticalalignment='bottom')

        ax2 = ax1.twinx()
        ax2.plot(x, y1, color='orange', marker='o', dash_capstyle='round', dash_joinstyle='round',
                 label='일 확진환자(단위: 명)', linewidth='3', markersize='20')
        ax2.legend(loc='upper right', fontsize=30)
        ax2.set_ylim(0, 2500)

        for i, v in enumerate(x):
            ax2.text(v, y1[i], y1[i], fontsize=40, color='black', horizontalalignment='center',
                     verticalalignment='bottom')

        # plt.show()
        fig.savefig('Image/function1.png')


if __name__ == "__main__":
    today = datetime.datetime.now()
    two_weeks_ago = today - datetime.timedelta(7)
    Function1().getCovidKR("20210107", "20200901")  # 자정부터 오전 10시까지 테스트용
    # Function1().getCovidKR(today.strftime("%Y%m%d"), two_weeks_ago.strftime("%Y%m%d"))
