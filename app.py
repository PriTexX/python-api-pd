from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from userInfo import login, getUserInfo
from schedule import parseSchedule

app = FastAPI(title="Lk app API")


class Credentials(BaseModel):
    login: str
    password: str


@app.post("/getUserInfo")
async def getUserInfo(creds: Credentials):
    token = login(credentials=creds)
    user = getUserInfo(token)

    return user


@app.get("/getScheduleForYear")
async def getSchedule(token: str):
    schedule = parseSchedule(token)
    return schedule
