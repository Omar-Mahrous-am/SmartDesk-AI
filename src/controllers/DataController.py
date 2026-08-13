"""
Data handling controller for the SmartDesk AI application.

This module provides the `DataController` class, which manages the validation,
processing, and storage paths for files uploaded to the application.
It inherits from `BaseController` to utilize common configuration.
"""
from .BaseController import BaseController
from fastapi import UploadFile
from src.models.enums.ResponseSignal import ResponseSignal
import os
import uuid


class DataController(BaseController):
    """
    Controller responsible for handling incoming data files.

    This class provides methods to validate uploaded files against allowed
    formats and size constraints, and to generate secure, unique file paths
    for storage on the server.
    """

    def __init__(self):
        """
        Initializes the DataController with validation constraints.
        """
        super().__init__()

        # Define supported file formats for data extraction and RAG processing
        self.allowed_extensions = [".pdf", ".txt", ".docx", ".doc"]
        
        # Restrict file size to prevent memory exhaustion during processing
        self.max_file_size = 10 * 1024 * 1024  # 10 MB

    def validate_uploaded_file(self, file: UploadFile):
        """
        Validates an uploaded file's type against the allowed extensions.

        Args:
            file (UploadFile): The file object uploaded via FastAPI.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating validity 
                and a response signal string providing the status.
        """
        # Extract the extension and convert to lowercase for case-insensitive comparison
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in self.allowed_extensions:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        """
        Generates a unique file path and ID for an uploaded file.

        This method creates a unique identifier using a UUID to prevent file naming
        collisions within the same project directory. It also ensures that the target
        directory exists on the filesystem.

        Args:
            orig_file_name (str): The original name of the uploaded file.
            project_id (str): The unique identifier for the project this file belongs to.

        Returns:
            tuple[str, str]: A tuple containing the full absolute file path and the
                generated unique file ID.
        """
        # Use a short UUID to generate a random key for the filename
        random_key = uuid.uuid4().hex[:8]
        file_ext = os.path.splitext(orig_file_name)[1]
        
        # Construct a unique filename while preserving the original extension
        file_id = f"{random_key}{file_ext}"

        # Build the complete path using the base directory from BaseController
        file_path = os.path.join(
            self.files_dir,
            str(project_id),
            file_id
        )

        # Create the project directory structure if it doesn't already exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        return file_path, file_id

