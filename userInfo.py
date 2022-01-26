import requests
from exceptions import FailedToLoginException
from models import Credentials


async def login(credentials: Credentials):
    resp = requests.post("https://e.mospolytech.ru/old/lk_api.php", data={
        'ulogin': credentials.login,
        'upassword': credentials.password,
    }, verify=False)

    if resp.status_code == 400:
        raise FailedToLoginException("Неверно указан логин или пароль")

    return resp.json()['token']


async def getUserInfo(token):
    userInfo = requests.get(
        f"https://e.mospolytech.ru/old/lk_api.php/?getUser&token={token}",
        verify=False
    ).json()

    user = userInfo['user']
    user['token'] = token

    return user
