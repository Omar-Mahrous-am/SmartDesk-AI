from fastapi import APIRouter, Depends, File, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
import logging
import aiofiles
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController, ProcessController,NLPController
from src.models.enums.ResponseSignal import ResponseSignal
from src.schemas.data import ProcessRequest
from src.models.ProjectModel import ProjectModel
from src.models.ChunkModel import ChunkModel
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
    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)

    chunk_model= await ChunkModel.create_instance(db_client=request.app.db_client)
    
    project= await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"signal": ResponseSignal.PROJEXT_NOT_FOUND_ERROR.value})

    nlp_controller_instance=NLPController(vectordb_client=request.app.vectordb_client,generation_client=request.app.generation_client,embedding_client=request.app.embedding_client)

    inserted_count=0
    has_records=True
    page_number=1
    idx=0
    
    while has_records:
        page_chunks=await chunk_model.get_project_chunks(project_id=project.project_id,page_number=page_number,page_size=push_request.page_size)
        
        if len(page_chunks):
            page_number+=1
            
        if len(page_chunks)==0:
            has_records=False
            break

        chunks_ids=list(range(idx,idx+len(page_chunks)))
        idx+=len(page_chunks)


        is_inserted =nlp_controller_instance.index_into_vectordb(project=project,chunks=page_chunks,do_rest=push_request.do_rest,chunks_ids=chunks_ids) 
        inserted_count+=len(page_chunks)

        if not is_inserted:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"signal": ResponseSignal.INSERT_INTO_VECTOR_DB_FAILED.value})
    
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"signal": ResponseSignal.INSERT_INTO_VECTOR_DB_SUCCESS.value,
                                                                "inserted_count":inserted_count})















    
    