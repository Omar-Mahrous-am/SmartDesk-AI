"""
Enumerations for API response signals.

This module defines standard machine-readable string codes used in API responses
to communicate the specific outcome of a request to the client.
"""
from enum import Enum

class ResponseSignal(Enum):
    """
    Standardizes response status signals across the API.

    These signals are typically returned in the JSON body of a response (e.g., {"signal": ...})
    and allow the frontend to easily map backend outcomes to user-facing messages or actions.

    Attributes:
        FILE_VALIDATED_SUCCESS: File passed all format and size checks.
        FILE_TYPE_NOT_SUPPORTED: The uploaded file extension is not allowed.
        FILE_SIZE_EXCEEDED: The uploaded file is too large.
        FILE_UPLOAD_SUCCESS: The file was successfully saved to disk and database.
        FILE_UPLOAD_FAILED: An error occurred while saving the file.
        FILE_PROCESSED_SUCCESS: (Legacy) File processing succeeded.
        FILE_PROCESSING_FAILED: (Legacy) File processing failed.
        FILE_ID_ERROR: The requested file ID does not exist for the project.
        NO_FILES_ERROR: No files were found to process in the project.
        PROCESSING_FAILED: The chunking/extraction process failed or returned empty.
        PROCESSING_SUCCESS: Documents were successfully chunked and saved to the database.
    """
    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"  
    FILE_PROCESSED_SUCCESS = "file_processed_successfully"   
    FILE_PROCESSING_FAILED = "file_processing_failed"
    FILE_ID_ERROR = "file_id_error"
    NO_FILES_ERROR = "no_files_found"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESS = "processing_success"
    PROJECT_NOT_FOUND_ERROR="project_not_found"
    INSERT_INTO_VECTOR_DB_SUCCESS="insert_into_vector_db_success"
    INSERT_INTO_VECTOR_DB_FAILED="insert_into_vector_db_failed"
    VECTORDB_COLLECTION_RETRIEVED="vector_db_collection_retrived"
    VECTORDB_COLLECTION_NOT_RETRIEVED="vector_db_collection_not_retrived"
    SEARCH_SUCCESS="search_success"
    SEARCH_FAILED="search_failed"
    INSERT_INTO_VECTOR_DB_SUCCESS="insert_into_vector_db_success"
    INSERT_INTO_VECTOR_DB_FAILED="insert_into_vector_db_failed"    


