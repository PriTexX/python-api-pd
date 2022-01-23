import requests
import re
import json


def login(credentials):
    session = requests.Session()
    resp = session.post("https://e.mospolytech.ru/old/lk_api.php", data={
        'ulogin': credentials.login,
        'upassword': credentials.password,
    }, verify=False)

    if resp.status_code == 400:
        raise Exception("Неверно указан логин или пароль")

    return json.loads(resp.content)['token']


def getUserInfo(token):
    userInfo = requests.get(
        f"https://e.mospolytech.ru/old/lk_api.php/?getUser&token={token}",
        verify=False
    ).content

    user = json.loads(userInfo.decode('unicode_escape'))['user']
    user['token'] = token

    return user
