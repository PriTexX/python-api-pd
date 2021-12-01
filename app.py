from fastapi import FastAPI, HTTPException

app = FastAPI(title="testing api")

@app.get("/test")
async def test():
    return "Srabotalo"
