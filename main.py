import requests
from fake_useragent import UserAgent
import re
from weekParser import parseWeek


def login():
    try:
        headers = {
            "User-Agent": UserAgent().random
        }
        session = requests.Session()
        session.headers.update(headers)
        resp = session.post("https://e.mospolytech.ru/index.php", data={
            'ulogin': 'v.a.bulavin',
            'upassword': 'Stud336266!',
            'auth_action': 'userlogin',
        })
        isErr = re.search("Неверно указан логин и/или пароль", resp.text)
        if isErr:
            raise Exception(isErr.group())
        return session
    except Exception as error:
        print(error.args)


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


