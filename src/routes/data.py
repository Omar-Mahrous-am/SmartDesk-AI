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


logger = logging.getLogger(__name__)
app_settings = Settings()

data_router = APIRouter(prefix="/api/v1",
                        tags=["api_v1"])


@data_router.post("/upload/{project_id}")
async def upload_file(request:Request,  project_id: str, file: UploadFile = File(...)):

    
    project_model=ProjectModel(db_client=request.app.db_client)
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
            "project_id": str(project._id)
        }
    )


@data_router.post("/process/{project_id}")
def process_file_endpoint(project_id: str, process_request: ProcessRequest):

    project_controller = ProjectController()
    project_dir = project_controller.get_project_path(project_id)
    file_path = os.path.join(project_dir, process_request.file_id)

    if not os.path.exists(file_path):
        return {"status": ResponseSignal.FILE_PROCESSING_FAILED.value,
                "data": [], "message": "File not found"}

    process_controller = ProcessController()
    doc = process_controller.load_pdf(file_path)
    chunks = process_controller.split_text_into_chunks(
        doc, process_request.chunk_size, process_request.chunk_overlap
    )

    if chunks:
        return {"status": ResponseSignal.FILE_PROCESSED_SUCCESS.value,
                "data": chunks}
    else:
        return {"status": ResponseSignal.FILE_PROCESSING_FAILED.value,
                "data": []}
