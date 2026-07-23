from .BaseController import BaseController
from fastapi import UploadFile
from src.models.enums.ResponseSignal import ResponseSignal
import os
import uuid


class DataController(BaseController):

    def __init__(self):
        super().__init__()

        self.allowed_extensions = [".pdf", ".txt", ".docx", ".doc"]
        self.max_file_size = 10 * 1024 * 1024  # 10 MB

    def validate_uploaded_file(self, file: UploadFile):
        # check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in self.allowed_extensions:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        random_key = uuid.uuid4().hex[:8]
        file_ext = os.path.splitext(orig_file_name)[1]
        file_id = f"{random_key}{file_ext}"

        file_path = os.path.join(
            self.files_dir,
            project_id,
            file_id
        )

        # ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        return file_path, file_id
