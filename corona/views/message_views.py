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
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['action']['params']['내가만든지역명']
    path = "/corona-kakao-bot/crawler/assets/texts/cities/"
    datas = []
    right = False

    for i in range(500):
        try:
            f = open(path + str(i), "r", encoding="utf-8-sig")
            key = f.readline()[:-1]
            f.close()
            if key == return_str:
                f = open(path + str(i), "r", encoding="utf-8-sig")
                for line in f:
                    if line[:-1] == return_str:
                        pass
                    else:
                        datas.append(line)
                f.close()
                right = True

        except FileNotFoundError:
            pass
    if right is False:
        text = "📭 해당 지역은 오늘자 코로나 관련 재난 문자가 없어요."
    else:
        text = ''.join(datas)
        text = text[:-2]

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
                    'label': '2️⃣번 실시간 집계 확인',
                    'action': 'message',
                    'messageText': '실시간'
            },
                {
                    'label': '📬 다른 지역 코로나 재난 문자 확인',
                    'action': 'message',
                    'messageText': '검색'
            },
                {
                    'label': '🏡홈으로',
                    'action': 'message',
                    'messageText': '도움말'
            }

            ]
        }
    })