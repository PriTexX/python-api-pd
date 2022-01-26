from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import FailedToLoginException


async def failedToLoginHandler(request: Request, exc: FailedToLoginException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.details, "type": "login"}
    )
