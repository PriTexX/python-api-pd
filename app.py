from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from userInfo import login, getUserInfo
from schedule import parseSchedule
from models import Credentials
from exceptions import FailedToLoginException
from exceptionHandlers import failedToLoginHandler

app = FastAPI(title="Lk app API")


@app.post("/getUserInfo")
async def UserInfo(creds: Credentials):
    token = await login(credentials=creds)
    user = await getUserInfo(token)
    return user


@app.get("/getScheduleForYear")
async def get_schedule(token: str):
    schedule = parseSchedule(token)
    headers = {
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST GET',
    }
    return JSONResponse(content=schedule, headers=headers)


@app.exception_handler(FailedToLoginException)
async def loginHandler(request: Request, exc: FailedToLoginException):
    return await failedToLoginHandler(request, exc)
