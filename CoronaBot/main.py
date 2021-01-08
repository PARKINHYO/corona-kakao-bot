import datetime, function1

today = datetime.datetime.now()
two_weeks_ago = today - datetime.timedelta(14)
sums, adds = function1.getCovidKR(today.strftime("%Y%m%d"), two_weeks_ago.strftime("%Y%m%d"))
# sums, adds = Function1.getCovidKR("20210107", "20201224") # 자정부터 오전 10시까지 테스트용
function1.getCovidTxt(sums, adds)
function1.getCovidGraph(sums, adds)


