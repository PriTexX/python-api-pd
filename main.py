import requests
from fake_useragent import UserAgent
import re
from weekParser import parseWeek


def getGroupToken():
    resp = session.get("https://e.mospolytech.ru/?p=rasp")
    pattern = '''\('.{0,}'\)\+"&token=.{0,}"'''
    group_token = re.search(pattern, resp.text).group()
    token = re.search('(?<=&token=).+(?=")', group_token).group()
    group = re.search("(?<=\(').{7,}(?='\))", group_token).group()
    return group, token


def getSchedule(group, token):
    rasp = session.get(f"https://rasp.dmami.ru/site/group-html?group={group}&token={token}")
    if rasp.status_code == 200:
        return rasp.text
    else:
        print("error")

if __name__ == "__main__":
    session = login()
    group, token = getGroupToken()
    schedule = getSchedule(group, token)
    parseWeek(schedule)


