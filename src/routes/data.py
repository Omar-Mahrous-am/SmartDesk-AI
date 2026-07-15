from aiofiles import tempfile
from aiofiles import tempfile
from aiofiles import tempfile
from fastapi import APIRouter, File, UploadFile, status,Request
from fastapi.responses import JSONResponse
import os
import logging
import aiofiles
from src.controllers import ProcessController, ProjectController
from src.models.enums.ResponseSignal import ResponseSignal
from src.schemas.data import ProcessRequest
from src.helpers.config import Settings
from src.models.ProjectModel import ProjectModel
from src.models.db_schemas import DataChunk
from src.models.ChunkModek import ChunkModel


logger = logging.getLogger(__name__)
app_settings = Settings()

data_router = APIRouter(prefix="/api/v1",
                        tags=["api_v1"])


@data_router.post("/upload/{project_id}")
async def upload_file(request:Request,  project_id: str, file: UploadFile = File(...)):

    
    project_model=await ProjectModel.create_instance(db_client=request.app.mongodb)
    project=await project_model.get_project_or_create_one(project_id=project_id)




    project_controller = ProjectController()
    project_dir = project_controller.get_project_path(project_id)
    file_path = os.path.join(project_dir, file.filename)
    file_id = file.filename

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
            "project_id": str(project.id)
        }
    )


@data_router.post("/process/{project_id}")
async def process_file_endpoint(request:Request,project_id: str, process_request: ProcessRequest):

    project_controller = ProjectController()
    project_dir = project_controller.get_project_path(project_id)
    file_path = os.path.join(project_dir, process_request.file_id)
    do_reset=process_request.do_reset

    

    project_model=await ProjectModel.create_instance(db_client=request.app.mongodb)
    project=await project_model.get_project_or_create_one(project_id=project_id)

 



    if not os.path.exists(file_path):
        return {"status": ResponseSignal.FILE_PROCESSING_FAILED.value,
                "data": [], "message": "File not found"}

    process_controller = ProcessController()
    doc = process_controller.load_pdf(file_path)
    chunks = process_controller.split_text_into_chunks(
        doc, process_request.chunk_size, process_request.chunk_overlap
    )

    if not chunks:
        return JSONResponse(
            status_code=400,
            content={"status": ResponseSignal.FILE_PROCESSING_FAILED.value, "data": []}
        )

    file_chunks_records=[
        DataChunk(
         chunk_content=chunck.page_content,
         chunk_order=i+1,
         chunk_metadata=chunck.metadata,
         chunk_project_id=project.id
        )
        for i,chunck in enumerate(chunks)
    ]

    chunk_model=await ChunkModel.create_instance(db_client=request.app.mongodb)

    if do_reset==1:
        await chunk_model.delete_chunks_by_project_id(project.id) 

    

    no_of_records=await chunk_model.insert_many_chunks(file_chunks_records)


    return JSONResponse(content={"signal":ResponseSignal.FILE_PROCESSED_SUCCESS.value,"inserted_chunks":no_of_records})





    
