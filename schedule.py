from datetime import date as Date
from datetime import datetime
import requests
import json
import calendar
from Constants import DAYS_OF_THE_WEEK, MONTHS
import re

schedule = None


def getSchedule(token):
    Schedule = requests.get(f"https://e.mospolytech.ru/old/lk_api.php/?getSchedule&token={token}", verify=False)
    return json.loads(Schedule.content.decode('utf8'))


def getScheduleSession(token):
    ScheduleSession = requests.get(f"https://e.mospolytech.ru/old/lk_api.php/?getSchedule&session=1&token={token}", verify=False)
    return json.loads(ScheduleSession.content.decode('utf8'))


def checkDay(lesson, date: Date):
    lessonDays = re.findall('\d\d', lesson['dateInterval'])
    lessonMonths = re.findall('[А-я]{3}', lesson['dateInterval'])
    startDate = Date(date.year, MONTHS[lessonMonths[0]], int(lessonDays[0]))

    if MONTHS[lessonMonths[0]] > MONTHS[lessonMonths[-1]]:
        endDate = Date(date.year + 1, MONTHS[lessonMonths[-1]], int(lessonDays[-1]))
    else:
        endDate = Date(date.year, MONTHS[lessonMonths[-1]], int(lessonDays[-1]))
    return startDate <= date <= endDate # checks whether current date is in range of the lesson's dates


def findLessons(date: Date):
    global schedule
    pairs = {'lessons': []}

    day = calendar.day_name[date.weekday()]
    pairs['day'] = day

    if day == 'Sunday':
        return pairs

    for pair in schedule[day]['lessons']:
        if checkDay(pair, date):
            pairs['lessons'].append(pair)
    return pairs


def parseSessionSchedule(token):
    session = getScheduleSession(token)

    for date in session.keys():
        session[date]['day'] = calendar.day_name[datetime.strptime(date, '%Y-%m-%d').weekday()]
    return session


def parseSchedule(token):
    global schedule
    schedule = getSchedule(token)
    yearSchedule = {**parseSessionSchedule(token)}
    Calendar = calendar.Calendar()
    today = Date.today()

    if 8 <= today.month <= 12:
        firstSemesterYear = today.year
        secondSemesterYear = firstSemesterYear + 1
    else:
        secondSemesterYear = today.year
        firstSemesterYear = secondSemesterYear - 1

    for month in range(9, 13):
        for date in Calendar.itermonthdates(firstSemesterYear, month):
            yearSchedule[str(date)] = yearSchedule.get(str(date), findLessons(date))

    for month in range(1, 8):
        for date in Calendar.itermonthdates(secondSemesterYear, month):
            yearSchedule[str(date)] = yearSchedule.get(str(date), findLessons(date))

    return yearSchedule
