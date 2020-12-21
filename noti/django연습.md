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

[python3 실행 환경변수 설정](https://somjang.tistory.com/entry/PythonUbuntu%EC%97%90%EC%84%9C-Python37-%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0bashrc%ED%8C%8C%EC%9D%BC%EC%88%98%EC%A0%95)

아까 입력했던 것 같은 pip upgrade 명령어를 실행해줍니다. 이건 아까 했던 거 같은데 왜 또 하는 걸까요? 그것은 가상환경은 가상환경 밖의 리눅스 환경과 별개이기 때문에 pip이 업데이트되지 않은 갓 나온 상태이기 때문입니다. 이처럼 가상환경과 그 밖이 별개라는 점을 기억하고 가도록 합시다. 마찬가지로 django 도 다시 설치해줍니다.

### 아파치2, MOD-WSGI 설치

```bash
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi-py3
```

apache2 를 설치하고 mod-wsgi 를 설치합니다. Django 는 엄밀히 말하면 서버가 아니고 웹앱을 만드는 웹 프레임워크입니다. 그렇기 때문에 웹앱을 실제로 배포하려면 서버가 필요한데 apache 가 그 역할을 해줄 것입니다. 그리고 apache 와 django 앱을 배포하기 위해 중간자가 필요한데요. mod-wsgi 가 이 역할을 합니다.

mod-wsgi 는 Apache HTTP Server 모듈로 Apache에서 Python 기반 웹 응용 프로그램을 호스팅하기위한 WSGI 호환 인터페이스를 제공한다는 설명이 있습니다. 쉽게 말하면 Python 웹 프레임워크로 만든 웹앱을 Apache 에서의 배포하기 위해 통신하는 인터페이스라는 건데요. 그래서 mod-wsgi 는 django 뿐 아니라 flask 에서도 사용이 가능합니다. 

python3 에서는 반드시 libapache2-mod-wsgi 뒤에 -py3 을 붙여줘야 동작이 가능하다는 것을 염두에 두고 설치하시기 바랍니다. 프로젝트 setting을 잠깐 해보겠습니다. 다음을 입력합니다.

### ```setting.py``` , ```wsgi.py``` 설정

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

sys.path.append('/home/ubuntu/python-django-projcet')
sys.path.append('/home/ubuntu/python-django-project/myvenv/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corona_kakao_bot.settings')

application = get_wsgi_application()
```

