import requests, xmltodict, json, datetime
from typing import List
import matplotlib.pyplot as plt
import numpy as np


def getCovidKR(end_day: str, start_day: str) -> (List[int], List[int]):
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

        for i in range(13, -1, -1):
            sums.append(int(dd['response']['body']['items']['item'][i]['decideCnt']))
            adds.append(int(dd['response']['body']['items']['item'][i]['decideCnt']) - int(
                dd['response']['body']['items']['item'][i + 1]['decideCnt']))

            print('누적 확진자:', dd['response']['body']['items']['item'][i]['decideCnt'], end='\t')
            print('추가 확진자:', int(dd['response']['body']['items']['item'][i]['decideCnt']) - int(
                dd['response']['body']['items']['item'][i + 1]['decideCnt']), end='\t\t')
            print('%s일 %s시 기준' % (
                dd['response']['body']['items']['item'][i]["stateDt"],
                dd['response']['body']['items']['item'][i]["stateTime"]))

    else:
        print('res.status_code is NOT ok')
    return (sums, adds)


def getCovidGraph(sums: List[int], adds: List[int]):
    # 1. 기본 스타일 설정
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (4, 3)
    plt.rcParams['font.size'] = 12

    # 2. 데이터 준비
    dates = []
    today = datetime.datetime.now()

    for i in range(14, 0, -1):
        dates.append((today - datetime.timedelta(i)).strftime("%m.%d"))
    x = np.array(dates)
    y1 = np.array(adds)
    y2 = np.array(sums)

    print(dates, adds, sums)

    # 3. 그래프 그리기
    fig, ax1 = plt.subplots()

    ax1.plot(x, y1, color='orange', marker='o', dash_capstyle='round', dash_joinstyle='round')
    ax1.set_ylim(0, 1500)
    ax1.set_xlabel('일 확진환자')
    ax1.set_ylabel('일 확진환자')
    ax1.tick_params(axis='both')

    ax2 = ax1.twinx()
    ax2.bar(x, y2, color='blue', label='누적 확진환자', alpha=0.7, width=0.7)
    ax2.set_ylim(0, 100000)
    ax2.set_ylabel('누적 확진환자')
    ax2.tick_params(axis='y', direction='in')

    plt.show()


if __name__ == "__main__":
    today = datetime.datetime.now()
    two_weeks_ago = today - datetime.timedelta(14)
    sums , adds = getCovidKR(today.strftime("%Y%m%d"), two_weeks_ago.strftime("%Y%m%d"))
    getCovidGraph(sums, adds)
