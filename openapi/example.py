import requests
import xmltodict
import json
import datetime


def getCovidKR(end_day, start_day):
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'

    # ServiceKey는 url decode 한 값임.
    payload = {'ServiceKey': 'service_key',
               'startCreateDt': start_day, 'endCreateDt': end_day, }
    res = requests.get(url, params=payload)
    if (res.status_code == 200):
        # Ordered dictionary type
        result = xmltodict.parse(res.text)
        #dictionlay type
        dd = json.loads(json.dumps(result))
        print(dd)
        print ('누적 확진자:', dd['response']['body']['items']['item'][0]['decideCnt'])
        print ('추가 확진자:', int(dd['response']['body']['items']['item'][0]['decideCnt']) - int(dd['response']['body']['items']['item'][1]['decideCnt']))
        print ('%s일 %s시 기준' %(dd['response']['body']['items']['item'][0]["stateDt"], dd['response']['body']['items']['item'][0]["stateTime"]))
    else:
        print ('res.status_code is NOT ok')

if __name__ == "__main__":
    today =datetime.datetime.now()
    yesterday = today - datetime.timedelta(1)
    d1 = today.strftime("%Y%m%d")
    d2 = yesterday.strftime("%Y%m%d")
    getCovidKR(d1, d2)
