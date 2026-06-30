
from fastapi import APIRouter
import os
from dotenv import load_dotenv


load_dotenv(".env")


base_router=APIRouter(prefix="/api/v1",
                      tags=["api_v1"])


@base_router.get("/")
async def welcome():
    app_name=os.getenv("APP_NAME")
    return {"message" : "Welcome to " + app_name}
    