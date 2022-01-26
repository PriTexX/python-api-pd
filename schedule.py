from datetime import date as Date
from datetime import datetime
import requests
import json
import calendar
from Constants import MONTHS, DAYS_OF_THE_WEEK_RU, DAYS_OF_THE_WEEK_SHORT
import re
from exceptions import NoDataFromServer

schedule = None


def getSchedule(token):
    response = requests.get(f"https://e.mospolytech.ru/old/lk_api.php/?getSchedule&token={token}", verify=False).json()

    if not response:
        raise NoDataFromServer('No schedule data available')

    return response


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
    pairs['day_ru'] = DAYS_OF_THE_WEEK_RU[day]
    pairs['day_short'] = DAYS_OF_THE_WEEK_SHORT[day]

    if day == 'Sunday':
        return pairs

    for pair in schedule[day]['lessons']:
        if checkDay(pair, date):
            pairs['lessons'].append(pair)
    return pairs


def parseSessionSchedule(token):
    session = getScheduleSession(token)

    for date in session.keys():
        dayName = calendar.day_name[datetime.strptime(date, '%Y-%m-%d').weekday()]
        session[date]['day'] = dayName
        session[date]['day_ru'] = DAYS_OF_THE_WEEK_RU[dayName]
        session[date]['day_short'] = DAYS_OF_THE_WEEK_SHORT[dayName]
    return session


def parseSchedule(token):
    global schedule
    yearSchedule = {**parseSessionSchedule(token)}

    try:
        schedule = getSchedule(token)
    except NoDataFromServer:
        return yearSchedule

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
