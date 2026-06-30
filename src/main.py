from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv("src/.env")
from src.routes import base,data




app = FastAPI()

app.include_router(base.base_router)
app.include_router(data.data_router)

@app.get("/")
def home():
    return {"message": "SmartDesk AI API is running"}




