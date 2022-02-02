from datetime import datetime, timedelta
import calendar


def getDayHowWeek():
    """
    获取当前日期是第几周
    :return:
    """
    begin = datetime.now().replace(day=1).strftime("%W")
    end = datetime.now().strftime("%W")

    return int(end) - int(begin) + 1


def getNextMonday():
    today = datetime.now()
    oneday = timedelta(days=1)
    m1 = calendar.MONDAY
    if today.weekday() == 0:
        nextMonday = timedelta(days=7)+today
    else:
        while today.weekday() != m1:
            today += oneday
        nextMonday = today
    return nextMonday


def isInNextWeek(text_date):
    date = datetime.strptime(text_date, '%m月%d日')
    now = datetime.now()
    if (date.month >= now.month):
        date = date.replace(year=now.year)
    else:
        date = date.replace(year=now.year+1)

    next_monday = getNextMonday()
    # 下周的每一天
    for i in range(7):
        if (next_monday + timedelta(days=i)).date() == date.date():
            return True
    return False


def isNextMonth(text_date, format_str='%m月%d日'):
    date = datetime.strptime(text_date, format_str)
    next_month = datetime.now().month + 1
    return date.month == next_month
