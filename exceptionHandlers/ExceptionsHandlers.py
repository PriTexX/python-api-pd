from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import FailedToLoginException, NoDataFromServer


async def failedToLoginHandler(request: Request, exc: FailedToLoginException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.details, "type": "login"}
    )


async def noDataFromServerHandler(request: Request, exc: NoDataFromServer):
    return JSONResponse(
        status_code=404,
        content={"message": exc.details, "type": "schedule"}
    )