import datetime, function1

today = datetime.datetime.now()
two_weeks_ago = today - datetime.timedelta(7)
# function1.Function1().getCovidKR("20210107", "20201224")  # 자정부터 오전 10시까지 테스트용
function1.Function1().getCovidKR(today.strftime("%Y%m%d"), two_weeks_ago.strftime("%Y%m%d"))
