from fastapi import FastAPI, HTTPException, Request
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
async def getSchedule(token: str):
    schedule = parseSchedule(token)
    return schedule


@app.exception_handler(FailedToLoginException)
async def loginHandler(request: Request, exc: FailedToLoginException):
    return await failedToLoginHandler(request, exc)
