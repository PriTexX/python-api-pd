from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from userInfo import login, getUserInfo
from schedule import parseSchedule
from models import Credentials
from exceptions import FailedToLoginException
from exceptionHandlers import failedToLoginHandler
from typing import Dict, Any

app = FastAPI(title="Lk app API")


@app.post("/getUserInfo")
async def UserInfo(creds: Request):
    credentials = await creds.json()

    token = await login(credentials=credentials)
    user = await getUserInfo(token)
    headers = {
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Origin': '*',
    }
    return JSONResponse(content=user, headers=headers)


# @app.options("/getUserInfo")
# async def sendBackCORS():
#     return JSONResponse(headers={
#         'Access-Control-Allow-Credentials': 'true',
#         'Access-Control-Allow-Origin': '*',
#     })


@app.get("/getScheduleForYear")
async def get_schedule(token: str):
    schedule = parseSchedule(token)
    headers = {
        'Access-Control-Allow-Origin': '*',
    }
    return JSONResponse(content=schedule, headers=headers)


@app.exception_handler(FailedToLoginException)
async def loginHandler(request: Request, exc: FailedToLoginException):
    return await failedToLoginHandler(request, exc)
