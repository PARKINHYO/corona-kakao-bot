import requests, xmltodict, json, datetime, sys
import matplotlib.pyplot as plt
import numpy as np


class Function1:
    def __init__(self, start='20210103', end='20210110'):
        self.start_day = start
        self.end_day = end
        self.sums = []
        self.adds = []
        self.complete = '0'
        self.completeDiff = 0
        self.treatment = '0'
        self.treatmentDiff = 0
        self.death = '0'
        self.deathDiff = 0

    def getCovidKR(self):
        url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
        payload = {
            'ServiceKey': 'PBhBuzFchp55OhkeLJfa+Ll4lkWY8udxumsPOtP+uB6lSYScko6sm+eDYlA1Yuie8m3NiTRjkb5ovgxwz8t1fQ==',
            'startCreateDt': self.start_day, 'endCreateDt': self.end_day, }
        res = requests.get(url, params=payload)
        try:
            if (res.status_code == 200):
                result = xmltodict.parse(res.text)
                dd = json.loads(json.dumps(result))

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
                return
        except IndexError:
            return

        self.getCovidTxt()
        self.getCovidGraph()

    def getCovidTxt(self):
        f = open("Text/func1data.txt", 'w')
        f.write(self.end_day + '\n')
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

        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (15, 15)
        plt.rcParams['font.size'] = 20
        plt.rc('font', family='Malgun Gothic')

        dates = []
        start = datetime.datetime(int(self.start_day[0:4]), int(self.start_day[4:6]), int(self.start_day[6:]))
        for i in range(1, 8):
            dates.append((start + datetime.timedelta(i)).strftime("%m.%d"))
        x = np.array(dates)
        y1 = np.array(self.adds)
        y2 = np.array(self.sums)

        fig, ax1 = plt.subplots()
        plt.grid(True, axis='y')
        plt.xticks(fontsize='25')

        ax1.bar(x, y2, color='skyblue', alpha=0.7, width=0.7, label='누적 확진환자(단위: 명)')
        ax1.set_ylim(0, 100000)
        ax1.legend(loc='upper left', fontsize=30)
        for i, v in enumerate(x):
            ax1.text(v, y2[i], y2[i], fontsize=20, color='black', horizontalalignment='center',
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
    if len(sys.argv) == 1:
        start = (datetime.datetime.now() - datetime.timedelta(7)).strftime("%Y%m%d")
        end = datetime.datetime.now().strftime("%Y%m%d")
        Function1(start, end).getCovidKR()
    elif sys.argv[1] == '--demo':
        Function1().getCovidKR()
