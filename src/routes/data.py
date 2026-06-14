from fastapi import APIRouter,FastAPI
import os
from dotenv import load_dotenv
from fastapi import File,UploadFile


load_dotenv(".env")


data_router=APIRouter(prefix="/api/v1",
                      tags=["api_v1"])

@data_router.post("/upload")

def upload_file(file:UploadFile=File(...)):
    

