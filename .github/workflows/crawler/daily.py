import requests, xmltodict, json, datetime, sys, os


class Function1:
    def __init__(self, start='20210114', end='20210121'):
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
            'ServiceKey': os.environ['DAILY_CRAWLER_SERVICE_KEY'],
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
                                 
                if self.completeDiff >= 0:
                    self.completeDiff = '↑ ' + str(format(self.completeDiff, ","))
                else:
                    self.completeDiff = '↓ ' + str(format(self.completeDiff, ","))[1:]
                
                if self.treatmentDiff >= 0:
                    self.treatmentDiff = '↑ ' + str(format(self.treatmentDiff, ","))
                else:
                    self.treatmentDiff = '↓ ' + str(format(self.treatmentDiff, ","))[1:]
                
                if self.deathDiff >= 0:
                    self.deathDiff = '↑ ' + str(format(self.deathDiff, ","))
                else:
                    self.deathDiff = '↓ ' + str(format(self.deathDiff, ","))[1:]
                    
                
                content = '**⌚ ' + str(self.end_day[:4]) + '년 ' + str(self.end_day[4:6]) + '월 ' + str(self.end_day[6:]) + '일**' + \
                    '\n😷 **총 확진자** ' + format(int(self.sums[-1]), ",") + '명\n' + \
                        '😷 **신규 확진자** ' + format(int(self.adds[-1]), ",") + '명\n' + \
                        '😅 **격리 해체** ' + format(int(self.complete), ",") + '명(' + self.completeDiff + ')\n' + \
                            '💊 **치료 중** ' + format(int(self.treatment), ",") + '명(' + self.treatmentDiff + ')\n' + \
                                '🙏 **사망** ' + format(int(self.death), ",") + '명(' + self.deathDiff + ')\n\n'
                        
                return content
            else:
                return 
        except IndexError:
            return
        