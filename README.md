<h1 align="center">Welcome to Corona Kakao Bot 👋</h1>
<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-2.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/PARKINHYO/corona-kakao-bot/blob/master/README.md" target="_blank">
  </a>
  <a href="https://github.com/PARKINHYO/corona-kakao-bot/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" />
  </a>  
    <a href="https://github.com/PARKINHYO/corona-kakao-bot/actions/workflows/upload_crawler.yml" target="_blank"><img alt="crawler docker compose" src="https://github.com/PARKINHYO/corona-kakao-bot/actions/workflows/upload_crawler.yml/badge.svg"></a>
  <a href="https://github.com/PARKINHYO/corona-kakao-bot/actions/workflows/crawler_container.yml" target="_blank"><img alt="crawler docker compose" src="https://github.com/PARKINHYO/corona-kakao-bot/actions/workflows/crawler_container.yml/badge.svg"></a>
  <a href="https://github.com/PARKINHYO/corona-kakao-bot/actions/workflows/webserver_container.yml" target="_blank"><img alt="crawler docker compose" src="https://github.com/PARKINHYO/corona-kakao-bot/actions/workflows/webserver_container.yml/badge.svg"></a>
</p>

<p align="center">
<img alt="character" width="300" src="https://user-images.githubusercontent.com/47745785/105130533-8f8bf400-5b2a-11eb-9b33-27e4d68b5736.png" />
</p>

<p align="center">
카카오톡을 통해 코로나 정보를 알려주는 채널 봇입니다. 
</p>

--------

### 🔑 채널 아이디 : coronavirus19

### 📷 Qr 코드

<img alt="Qr코드" width="200" height="200" src="https://user-images.githubusercontent.com/47745785/104895108-d22dbf00-59b8-11eb-8af9-d1c3d25af5d5.png"/>

<br><br>

## 📜 봇 & 서버 테스트

**개발 환경 : Ubuntu Server 20.04 LTS x86**

### 사전 설치 프로그램

1. git 설치

    ```bash
    $ sudo apt install git -y
    ```
2. [도커](https://docs.docker.com/engine/install/ubuntu/) 설치
3. 도커 컴포즈 설치(**root권한에서 설치**)

   [레포](https://github.com/docker/compose)에서 릴리즈 최신 버전 확인

    ```bash
    $ curl -L https://github.com/docker/compose/releases/download/(최신버전)/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    $ chmod +x /usr/local/bin/docker-compose
    $ docker-compose -v
    ```

### 서버 시간 KST로 변경

서버와 컨테이너가 시간대를 공유하기 때문에 서버의 시간대를 한국 시간대로 변경합니다. 

```bash
$ sudo dpkg-reconfigure tzdata
Asia
Seoul
```

### 컨테이너 설치

```bash
$ git clone https://github.com/PARKINHYO/corona-kakao-bot.git
$ cd corona-kakao-bot/crawler
$ docker-compose up -d
```

```bash
$ cd corona-kakao-bot
$ docker-compose up -d
```

### 컨테이너 로그 관리

크롤링 로그가 많이 쌓여 일정 간격으로 삭제합니다. 

```bash
$ cd corona-kakao-bot
$ sh container-logs.sh
```

### 코로나 관련 정보 확인 

코로나 관련 정보들은 /crawler/assets 폴더에 저장됩니다.

* /assets/texts/daily : 날짜, 총 확진자, 0시 기준 신규 확진자, 격리 해체, 치료 중, 사망
* /assets/images/dailyimage.png : 주간 확진자 그래프
* /assets/texts/realtime : 시간, 동 시간대 어제 확진자, 실시간 확진자 
* /assets/texts/cities/ : 지역별 재난 문자

### 참고

* 실제 서비스에 활용할 때는 [이 부분](https://github.com/PARKINHYO/corona-kakao-bot/blob/74561ac98460c850d6f7ad8f57b57e76b359f6f1/corona/views/daily_views.py#L58)에 자신의 서버 ip를 적어주어야 합니다. 
* 처음에는 /crawler/assets 폴더에 샘플 데이터가 들어있습니다. 
* 재난 문자 크롤링은 최대 4분 정도 됩니다. (나머지는 몇 초)
* 각 기능마다 크롤링 주기가 있습니다. 
  * [일일 확진자](https://github.com/PARKINHYO/corona-kakao-bot/blob/master/crawler/daily/crontab)
  * [실시간 확진자](https://github.com/PARKINHYO/corona-kakao-bot/blob/master/crawler/realtime/crontab)
  * [재난 문자](https://github.com/PARKINHYO/corona-kakao-bot/blob/master/crawler/message/crontab)

<br><br>

## 📣 서버 API

설치된 서버의 ip주소와 포트 80번으로 웹서버에 접근할 수 있습니다. 

* /corona/daily/text : 0시 기준 총 확진자 정보
* /corona/daily/image : 주간 확진자 그래프
* /corona/realtime/text : 실시간 확진자
* /corona/message/text : 지역별 재난 문자

<br><br>

## 📌 Service Flow Chart

 <img alt="Service Flow Chart" src="https://user-images.githubusercontent.com/47745785/104889496-a65b0b00-59b1-11eb-947e-f82649cb4623.jpg" />

<br><br>

## 📌 Architecture

<p align="center">
 <img alt="Architecture" src="./Architecture.png" />
</p>

<br><br>

## 🎥 데모

<img alt="사용방법" height="500" src="https://user-images.githubusercontent.com/47745785/105128866-3ff7f900-5b27-11eb-895e-b9f6c3a0a1ac.gif"/>

<br><br>

## 📚 출처

* 1번 0시 기준 총 확진자 외 정보 확인하기
  * [공공데이터포털](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15043376)
* 2번 금일 실시간 확진자 수 확인하기
  * [코로나라이브](https://corona-live.com/)
* 3번 금일 지역별 코로나 재난 문자 확인하기
  * [국민재난안전포털](https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679)
  * ![img_opentype04](https://user-images.githubusercontent.com/47745785/105054890-d7bcff00-5ab5-11eb-94d3-e9b32a776a9d.png)

## 🖋 Author

👤 **박인효**

* Mail: [inhyopark122@gmail.com](mailto:inhyopark122@gmail.com)
* GitHub: [@PARKINHYO](https://github.com/PARKINHYO)

## 📝 License

Copyright © 2021 [박인효](https://github.com/parkinhyo).<br/>
This project is [MIT](https://github.com/PARKINHYO/corona-kakao-bot/blob/master/LICENSE) licensed.
***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_