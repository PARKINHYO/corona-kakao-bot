### 리눅스 업데이트, pip, django 설치

```bash
$ sudo apt update
$ sudo apt install python3-pip
$ pip install --upgrade pip
$ sudo pip install django
```

### 가상환경 설정, 실행

```bash
$ mkdir python-django-project
$ cd python-django-project
$ sudo apt-get install python3-venv
$ python3 -m venv myvenv
$ source myvenv/bin/activate
```

가상환경을 만드는 이유는 어떤 프로젝트 동작을 위해 적합한 환경설정을 하기 위해서입니다. 우리가 만들 봇은 지금은 django, apache 정도만 설치하겠지만 후에 웹크롤링을 하려면 beautifulsoup, selenium 및 드라이버 설치도 필요합니다. 이런 게 중구난방 흩어져있는 것보다 가상환경 활성화를 해두고 설치해서 사용하면 편하겠죠?

### 가상환경 안에서도 마찬가지로 설치

```bash
$ pip install --upgrade pip
$ pip install django
$ django-admin startproject corona_kakao_bot
$ python3 manage.py startapp my_first_app
$ python3 manage.py migrate
```

여기서 파이썬 실행이 안될시에 [python3 실행 환경변수 설정](https://somjang.tistory.com/entry/PythonUbuntu%EC%97%90%EC%84%9C-Python37-%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0bashrc%ED%8C%8C%EC%9D%BC%EC%88%98%EC%A0%95)을 해줘야 합니다. 

아까 입력했던 것 같은 pip upgrade 명령어를 실행해줍니다. 이건 아까 했던 거 같은데 왜 또 하는 걸까요? 그것은 가상환경은 가상환경 밖의 리눅스 환경과 별개이기 때문에 pip이 업데이트되지 않은 갓 나온 상태이기 때문입니다. 이처럼 가상환경과 그 밖이 별개라는 점을 기억하고 가도록 합시다. 마찬가지로 django 도 다시 설치해줍니다.

### 아파치2, MOD-WSGI 설치

```bash
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi-py3
```

apache2 를 설치하고 mod-wsgi 를 설치합니다. Django 는 엄밀히 말하면 서버가 아니고 웹앱을 만드는 웹 프레임워크입니다. 그렇기 때문에 웹앱을 실제로 배포하려면 서버가 필요한데 apache 가 그 역할을 해줄 것입니다. 그리고 apache 와 django 앱을 배포하기 위해 중간자가 필요한데요. mod-wsgi 가 이 역할을 합니다.

mod-wsgi 는 Apache HTTP Server 모듈로 Apache에서 Python 기반 웹 응용 프로그램을 호스팅하기위한 WSGI 호환 인터페이스를 제공한다는 설명이 있습니다. 쉽게 말하면 Python 웹 프레임워크로 만든 웹앱을 Apache 에서의 배포하기 위해 통신하는 인터페이스라는 건데요. 그래서 mod-wsgi 는 django 뿐 아니라 flask 에서도 사용이 가능합니다. 

python3 에서는 반드시 libapache2-mod-wsgi 뒤에 -py3 을 붙여줘야 동작이 가능하다는 것을 염두에 두고 설치하시기 바랍니다. 프로젝트 setting을 잠깐 해보겠습니다. 다음을 입력합니다.

### `setting.py` , `wsgi.py` 설정

```bash
$ cd [base_name]/[project_folder]
$ vi settings.py

# settings.py
# 다음과 같이 수정합니다.
ALLOWED_HOSTS = '*'
INSTALLED_APPS = 'app_name' 
# 주의. app_name 빼고 다 지우는 게 아니라 app_name을 맨 마지막에 추가합니다.
TIME_ZONE = 'Asia/Seoul'
```

ALLOWED_HOSTS 는 본 서버 컴퓨터에 액세스를 요청하는 호스트를 누굴 받을 거냐 하는 건데요. '*'는 어떤 것이든 받는다는 뜻입니다.

그런 다음 INSTALLED_APPS 말미에 만들어둔 app을 추가해줍니다. 전 포스팅에서 설명했듯이 한 프로젝트는 여러 앱을 포함할 수 있습니다. 이 프로젝트가 이 앱을 제공하려면 app을 추가해줘야 가능하겠죠?

TIME_ZONE 은 우리가 작업하는 한국으로 바꿔줍니다. 

```bash
vi wsgi.py
"""
WSGI config for corona_kakao_bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/ubuntu/python-django-project')
sys.path.append('/home/ubuntu/python-django-project/myvenv/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corona_kakao_bot.settings')

application = get_wsgi_application()
```

`wsgi.py` 는 django 웹앱 코드가 WSGI에서 호출될 수 있게 하는 역할을 합니다. 쉽게 말하면 외부로 장고 앱을 export해주는 느낌입니다.

### apache 설정파일

```bash
$ sudo vi /etc/apache2/sites-available/000-default.conf

<VirtualHost *:80>
WSGIDaemonProcess corona_kakao_bot python-home=/home/ubuntu/python-django-project/myvenv python-path=/home/ubuntu/python-django-project/corona_kakao_bot
# The ServerName directive sets the request scheme, hostname and port that
# the server uses to identify itself. This is used when creating
# redirection URLs. In the context of virtual hosts, the ServerName
# specifies what hostname must appear in the request's Host: header to
# match this virtual host. For the default virtual host (this file) this
# value is not decisive as it is used as a last resort host regardless.
# However, you must set it for any further virtual host explicitly.
#ServerName www.example.com

ServerAdmin webmaster@localhost
WSGIScriptAlias / /home/ubuntu/python-django-project/corona_kakao_bot/corona_kakao_bot/wsgi.py
<Directory /home/ubuntu/python-django-project/corona_kakao_bot/corona_kakao_bot>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
DocumentRoot /var/www/html

# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
# error, crit, alert, emerg.
# It is also possible to configure the loglevel for particular
# modules, e.g.
#LogLevel info ssl:warn

ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined

# For most configuration files from conf-available/, which are
# enabled or disabled at a global level, it is possible to
# include a line for only one particular virtual host. For example the
# following line enables the CGI configuration for this host only
# after it has been globally disabled with "a2disconf".
#Include conf-available/serve-cgi-bin.conf
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

mod-wsgi 데몬 모드로 설정해주는 겁니다. 데몬이란 기본적으로 멀티태스킹 OS에서 사용자가 직접적으로 제어하지 않고, 백그라운드에서 돌면서 여러 작업을 하는 프로그램을 가리킵니다. 우리 상황에 더 특화시켜서 설명하자면 데몬 모드는 mod_wsgi 운영 시 권장되는 모드입니다. python-home 에는 가상환경 위치, python-path 에는 프로젝트 디렉토리 위치가 들어갑니다.

그 다음 ServerAdmin 아래 문장에 WSGIScriptAlias 로 시작되는 문장에는 `wsgi.py` 경로가 들어갑니다. 경로 앞에 / 라고 적혀 있는데, 이건 요청 url의 '/' 아래로 들어오는 요청은 `wsgi.py`를 호출하게 된다는 뜻이라는 정도만 알고 갑니다.

<Directory> 경로는 프로젝트 경로로 해주신 뒤 Require all granted 를 합니다. Require all granted 는 모든 액세스에 대해 허용한다는 뜻입니다.

### 아파치 재시작, 로그확인

```bash
$ sudo apachectl -k restart

$ vi /var/log/apache2/error.log
```

apache 서버 재시작 명령어를 한 뒤 아마존에서 받은 IP 주소로 접속을 시도해 보십시오. It worked! 나 apache 기본 페이지가 뜬다면 성공입니다. 만약 접속이 되지 않거나 500 Internal Server, 403 코드가 뜬다면 아래 명령어를 입력해 로그를 확인합니다. 서버에 문제가 있기 때문에 로그를 보고 잘못 처리한 부분을 수정하십시오.

### 챗봇 자동 응답 구현

모든 설정 구현들은 가상환경에서 해야함. 

```python
$ vi urls.py

# urls.py
from django.conf.urls import url
from [app_name] import views

urlpatterns = [
  url(r'^keyboard/?$', views.keyboard)
]
```

일단 app_name 에서 views 파일을 import 해줍니다. url 메소드는 첫 번째 매개변수로 url 패턴과 두 번째 매개변수로 그 URL 요청이 들어왔을 때 실행될 함수 이름을 추가하게 됩니다. ' ' 안에 예상되는 url 패턴을 넣을 수 있습니다. ^은 문자열의 시작이고, ?는 바로 앞의 한 글자가 있을지 없을지 모른다는 뜻입니다. $는 문자열의 마지막을 의미하는 문자인데 생략할 수 있습니다. 이것에 따르면 첫 번째 url은 `http://IP주소/keyboard/`나 `http://IP주소/keyboard` 요청이 왔을 때 views.keyboard 함수를 실행하게 됩니다.

```python
vi views.py

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })
```

일단 django.http 모듈에서 JsonResponse 를 import 합니다. 이유는 조금 이따가 message 함수가 호출되면 챗봇에서 조건에 따라 사용자에게 응답을 줘야 하는데 카카오톡 채팅봇 특성상 JSON 파일을 HTTP POST 방식으로 주고받기 때문에 JsonResponse 가 필요합니다.

그 다음 csrf_exempt 를 하는데 이것은 django 에서 CSRF 토큰을 이용해 CSRF 공격을 방지하기 때문입니다. HTTP POST 에서는 csrf verification failed 하면서 해당 코드가 먹통이 됩니다. 이에 따라 @csrf_exempt 를 붙여주는데 이것은 데코레이터로 message view에만 csrf를 비활성화시켜 줍니다. 

keyboard 함수를 만듭니다. 이것은 사용자가 최초로 채팅방에 들어갔을 때 보이게 되는 것입니다. 사실상 이건 쓸 일이 없어서(더구나 API형이 중지되고 i 빌더로 넘어와서는 쓸 일이 없어짐) 브라우저 테스트를 하기 좋게 간단하게 JsonResponse 를 하도록 해봤습니다. `http://ip주소/keyboard 테스트하기. 

![image](https://user-images.githubusercontent.com/47745785/102905177-157a3800-44b6-11eb-89e1-8b6f021f85ef.png)

```python
vi views.py
# keyboard 함수 밑에 이어서 작성

@csrf_exempt
def message(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']

    if return_str == '테스트':
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "테스트 성공입니다."
                    }
                }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
            }
        })
```

일단 request가 뭔지 살펴봐야겠습니다.봇 시스템은 스킬 서버에 HTTP POST Request(body는 json)을 보내고 스킬 서버는 HTTP Response(body json)을 요청한 봇 시스템으로 보내 줍니다. message 에서 받는 request 가 POST Request 인 것을 알 수 있습니다. 이 request.body 를 까보면 json 형식의 payload 인데 이것을 utf-8 방식으로 디코딩해서 answer 라는 변수에 집어넣는 게 첫 줄의 의미입니다. 그리 까다롭진 않습니다.

이것을 return_json_str 이라는 변수에 대입해 줍니다. 그런 다음엔 이 json에서 ['userRequest']['utterance']만 빼내게 되는데요. 이건 뭘 의미할까요? payload 에 무엇이 있는지 살펴보면 이것은 쉽습니다.

![image](https://user-images.githubusercontent.com/47745785/102905496-95a09d80-44b6-11eb-8bb2-7df9493c8a6c.png)

json 에 userRequest 라는 필드가 있고 그 안에 또 utterance 라는 필드가 있는데 이게 바로 사용자의 발화(입력)인 것입니다. 그럼 return_str 에는 사용자가 입력한 알맹이만 남게 되는 거죠. 이렇게 세 줄짜리 코드 분석을 했습니다.

저는 사용자가 '테스트'라고 입력했을 때 "테스트 성공입니다."라는 출력이 나오도록 봇을 꾸며보고 싶습니다. 그래서 if 문을 등장시켜 조건을 만족할 때 JsonResponse 를 return 하도록 했습니다.

인덴트에 주목해 주십시오. 일단 version 과 template 은 가장 외곽에 있고, outputs과 quickReplies가 template 안에 들어가 있습니다.

* version: 스킬 응답의 version 입니다. major.minor 로 구성되어 2.0, 2.1, 3.0 식으로 되어 있습니다.
* template: 스킬 응답의 출력을 담습니다. outputs 는 필수이며 quickReplies 는 생략이 가능합니다.
  * outputs: template 안의 필수 요소인 출력 그룹입니다. simpleText, simpleImage, basicCard 등의 요소를 포함하며 하나 이상을 골라 쓸 수 있습니다.
    * simpleText: outputs 의 한 요소인 간단한 텍스트형 출력입니다. text 를 필드로 갖습니다.
  * quickReplies: template 안의 요소인 바로가기 그룹입니다. 기존 API 형에서의 버튼과 비슷한 역할을 하며 사용자의 특정 발화 이후 기대되는 발화에 대한 힌트를 줄 수 있습니다.
    * label: 사용자에게 보이는 버튼의 텍스트입니다.
    * action: 바로가기 응답의 기능입니다. message 이거나 block 입니다.
    * messageText: action 이 message 일 때 해당 버튼을 누르게 되면 messageText 의 value 값이 사용자의 다음 발화가 됩니다. 

quickReplies 를 제외한 JsonReponse 의 가장 간단한 구성은 version 과 template, 그리고 template 안의 outputs 입니다.

위 코드는 스킬 응답 버전은 2.0, 출력은 텍스트로 "테스트 성공입니다."가 챗봇의 발화가 되며 '처음으로'라는 버튼이 올라옵니다. 그리고 이 버튼을 누르게 되면 사용자가 '처음으로'라고 말하는 것과 똑같은 효과를 나타냅니다.

