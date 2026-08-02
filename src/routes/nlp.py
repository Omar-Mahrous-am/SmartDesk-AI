from fastapi import APIRouter, Depends, File, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
import logging
import aiofiles
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController, ProcessController
from src.models.enums.ResponseSignal import ResponseSignal
from src.schemas.data import ProcessRequest
from src.models.ProjectModel import ProjectModel
from src.models.ChunkModek import ChunkModel
from src.models.AssetModel import AssetModel
from src.models.db_schemas import DataChunk, Asset
from src.models.enums.AssetTypeEnum import AssetTypeEnum
from src.schemas.nlp import PushRequest     
logger = logging.getLogger('uvicorn.error')

app_settings = Settings()

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1","nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str,push_request:PushRequest):
    """
    Index all chunks of a project to the vector database.
    """
    pass



    
    