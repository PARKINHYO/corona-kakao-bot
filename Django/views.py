from django.shortcuts import render

# Create your views here.
#-*- coding:utf-8 -*-

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import os
import random
from PIL import Image


@csrf_exempt
def function1(request):
    datas = []
    f = open('/home/ubuntu/CoronaBot/Text/func1data.txt', 'r')
    for line in f:
        datas.append(line)
    f.close()

    if datas[4][0] == '-':
        datas[4] = '↓' + datas[4][1:]
    else:
        datas[4] = '↑' + datas[4]

    if datas[6][0] == '-':
        datas[6] = '↓' + datas[6][1:]
    else:
        datas[6] = '↑' + datas[6]

    if datas[8][0] == '-':
        datas[8] = '↓' + datas[8][1:]
    else:
        datas[8] = '↑' + datas[8]

    days = {'Monday': '월', 'Tuesday': '화', 'Wednesday': '수',
            'Thursday': '목', 'Friday': '금', 'Saturday': '토', 'Sunday': '일'}
    d = datetime.date(int(datas[0][:4]), int(datas[0][4:6]), int(datas[0][6:]))
    text = '⌚ ' + datas[0][:4] + '. ' + datas[0][4:6] + '. ' + datas[0][6:8] + ' (' + days[d.strftime('%A')] + ') 0시 기준\n\n' \
        + '😷 총 확진자 ' + format(int(datas[1]), ",") + '명\n' + '😷 신규 확진자 ' + format(int(datas[2]), ",") + '명\n' \
        + '😅 격리 해체 ' + format(int(datas[3]), ",") + '명(' + datas[4][:len(datas[4])-1] + ')\n' \
        + '💊 치료 중 ' + format(int(datas[5]), ",") + '명(' + datas[6][:len(datas[6])-1] + ')\n' \
        + '🙏 사망 ' + format(int(datas[7]), ",") + \
        '명(' + datas[8][:len(datas[8])-1] + ')'
    return JsonResponse({
        'version': "2.0",
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': text
                    }
                },
                {
                    'simpleText': {
                        'text': "📊 일일 및 누적 확진 환자 추세를 보여드릴께요."
                    }
                },
                {
                    'simpleImage': {
                        'imageUrl': "http://ipadress/func1Image",
                        'altText': "주간그래프"
                    }
                }
            ],
            'quickReplies': [{
                'label': '2️⃣번 실시간 집계 확인',
                'action': 'message',
                'messageText': '실시간',
            },
                {
                    'label': '3️⃣번 코로나 재난 문자 확인',
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


@csrf_exempt
def func1Image(request):
    valid_image = "/home/ubuntu/CoronaBot/Image/function1.png"

    try:
        with open(valid_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response


@csrf_exempt
def function2(request):
    datas = []
    f = open("/home/ubuntu/CoronaBot/Text/func2data.txt", "r")
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
                },
                {
                    'simpleText': {
                        'text': "📈 어제와 오늘 시간대 별 확진 환자 추세를 보여드릴께요."
                    }
                },
                {
                    'simpleImage': {
                        'imageUrl': "http://ipaddress/func2Image",
                        'altText': "실시간그래프"
                    }
                }
            ],
            'quickReplies': [{
                'label': '1️⃣번 0시 기준 집계 확인',
                'action': 'message',
                'messageText': '총'
            },
                {
                    'label': '3️⃣번 코로나 재난 문자 확인',
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


@csrf_exempt
def func2Image(request):
    valid_image = "/home/ubuntu/CoronaBot/Image/function2.png"

    try:
        with open(valid_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response


@csrf_exempt
def function3(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['action']['params']['내가만든지역명']
    path = "/home/ubuntu/CoronaBot/Text/Cities/"
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
