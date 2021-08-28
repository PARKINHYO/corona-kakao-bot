import os
import datetime
from pytz import timezone
from github_utils import get_github_repo, upload_github_issue
from daily import Function1
from realtime import Function2
from message import Function3


if __name__ == "__main__":
    access_token = os.environ['CORONAKAKAOBOT_GITHUB_TOKEN']
    repository_name = "corona-kakao-bot"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.datetime.now(seoul_timezone)
    
    today_data = today.strftime("%Y년 %m월 %d일")
    issue_title = f"😷{today_data} 0시 기준 확진자 현황"
    
    start = (datetime.datetime.now(seoul_timezone) - datetime.timedelta(7)).strftime("%Y%m%d")
    end = datetime.datetime.now(seoul_timezone).strftime("%Y%m%d")
    
    upload_contents = Function1(start, end).getCovidKR()
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    
    
    today_data = datetime.datetime.now(seoul_timezone).strftime("%Y년 %m월 %d일 %p %I시 %M분 %S초")
    issue_title = f'📌{today_data} 실시간 확진자 현황'
    upload_contents = Function2().getCovidRealTime()
    upload_github_issue(repo, issue_title, upload_contents)
    
    today_data = datetime.datetime.now(seoul_timezone).strftime("%Y년 %m월 %d일 %p %I시 %M분 %S초")
    issue_title = f'📫{today_data} 실시간 전국 재난 문자 현황'
    now = datetime.datetime.now(seoul_timezone).strftime("%Y/%m/%d")
    upload_contents = Function3(now).getCovidCities()
    upload_github_issue(repo, issue_title, upload_contents)
    
    print("Upload Github Issue Success!")
    