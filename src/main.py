from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Discord FastAPI Bot!"}

@app.get("/ping")
async def ping():
    return {"message": "Pong!"}