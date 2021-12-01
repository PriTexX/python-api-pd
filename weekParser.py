from bs4 import BeautifulSoup
from datetime import date
from Constants import MONTHS, getMonth
import re

NOW = date(2021,11,29)


def checkLessonDates(since, to):
    return since <= NOW <= to


def findLessonDates(lesson):
    scheduleDates = lesson.select_one(".schedule-dates").text
    lessonDays = re.findall('\d\d', scheduleDates)
    lessonMonths = re.findall('[А-я]{3}', scheduleDates)
    since = date(NOW.year, MONTHS[lessonMonths[0]], int(lessonDays[0]))

    if MONTHS[lessonMonths[0]] > MONTHS[lessonMonths[-1]]:
        to = date(NOW.year + 1, MONTHS[lessonMonths[-1]], int(lessonDays[-1]))
    else:
        to = date(NOW.year, MONTHS[lessonMonths[-1]], int(lessonDays[-1]))
    return since, to


def parseWeek(week):
    soup = BeautifulSoup(week, 'html.parser')
    daysOfTheWeek = soup.findAll('div', class_="pairs")
    weekSchedule = []

    for day in daysOfTheWeek:
        daySchedule = []
        for pairs in day.findAll('div', class_="pair"):
            pair = {}
            pair['time'] = pairs.div.text
            for lesson in pairs.findAll('div', class_="schedule-lesson"):
                fromDate, toDate = findLessonDates(lesson)

                if checkLessonDates(fromDate, toDate):
                    if fromDate == toDate:
                        pair['dates'] = f"{fromDate.day} {getMonth(fromDate.month)}"
                    else:
                        pair['dates'] = f"{fromDate.day} {getMonth(fromDate.month)} - {toDate.day} {getMonth(toDate.month)}"
                    auditory = lesson.select_one('.schedule-auditory')
                    pair['auditory'] = {'link': auditory.a['href'], 'text': auditory.a.text}
                    pair['subject'] = lesson.select_one('.bold.small').text
                    pair['teacher'] = lesson.select_one('.teacher').span.text
                    daySchedule.append(pair)

        weekSchedule.append(daySchedule)
    for day in weekSchedule:
        for pair in day:
            print(pair)
        print()
        print()





