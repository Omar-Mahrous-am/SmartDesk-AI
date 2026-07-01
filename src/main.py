from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv("src/.env")
from src.routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers import config







app = FastAPI()

@app.on_event("start_up")
async def start_up():
    settings = config.get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB]
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()
    print("Closed MongoDB connection")  






app.include_router(base.base_router)
app.include_router(data.data_router)

@app.get("/")
def home():
    return {"message": "SmartDesk AI API is running"}




