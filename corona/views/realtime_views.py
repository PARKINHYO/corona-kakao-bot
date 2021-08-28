from django.shortcuts import render

# Create your views here.
#-*- coding:utf-8 -*-

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime


@csrf_exempt
def text(request):
    datas = []
    f = open("/corona-kakao-bot/crawler/assets/texts/realtime", "r")
    for line in f:
        datas.append(line)
    f.close()

    days = {'Monday': '월', 'Tuesday': '화', 'Wednesday': '수',
            'Thursday': '목', 'Friday': '금', 'Saturday': '토', 'Sunday': '일'}
    ampm = {'AM': '오전', 'PM': '오후'}
    if datas[0][10] == '0':
        zeroRemove = datas[0][11]
    else:
        zeroRemove = datas[0][10:12]
    if datas[0][12] == '0':
        zeroRemove2 = datas[0][13]
    else:
        zeroRemove2 = datas[0][12:14]
    diff = int(datas[-1]) - int(datas[-2])
    if str(diff)[0] == '-':
        diff = '↓' + str(diff)[1:]
    else:
        diff = '↑' + str(diff)

    d = datetime.date(int(datas[0][:4]), int(
        datas[0][4:6]), int(datas[0][6:8]))
    text = '⌚ ' + datas[0][4:6] + '. ' + datas[0][6:8] + ' (' + days[d.strftime('%A')] + ') ' \
        + ampm[datas[0][8:10]] + ' ' + zeroRemove + '시 ' + zeroRemove2 + '분 기준\n\n' \
        + '😷 실시간 확진자 ' + \
        format(int(datas[-1]), ",") + '명\n' + '😷 어제 동시간 대비 ' + diff

    return JsonResponse({
        'version': "2.0",
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': text
                    }
                }
            ],
            'quickReplies': [{
                'label': '1️⃣번 0시 기준 집계 확인',
                'action': 'message',
                'messageText': '총'
            },
                {
                    'label': '3️⃣번 재난 문자 확인',
                    'action': 'message',
                    'messageText': '지역별'
            },
                {
                    'label': '🏡홈으로',
                    'action': 'message',
                    'messageText': '도움말'
            }

            ]
        }
    })