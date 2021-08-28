from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from PIL import Image


@csrf_exempt
def text(request):
    datas = []
    f = open('/corona-kakao-bot/crawler/assets/texts/daily', 'r')
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
                        'imageUrl': "http://[server ip address]:80/corona/daily/image",
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


@csrf_exempt
def image(request):
    valid_image = "/corona-kakao-bot/crawler/assets/images/dailyimage.png"

    try:
        with open(valid_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response