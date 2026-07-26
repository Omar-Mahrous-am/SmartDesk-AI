# pyrefly: ignore [missing-import]
"""
Configuration management for the SmartDesk AI application.

This module utilizes Pydantic's BaseSettings to load, validate, and manage
environment variables and application-level settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings model powered by Pydantic.

    This class automatically reads environment variables from the `.env` file
    and performs type casting and validation based on the defined type hints.

    Attributes:
        APP_NAME (str): The name of the application.
        VERSION (str): The current application version.
        OPEN_API_KEYS (str): Comma-separated API keys, if applicable.
        FILE_DEFAULT_CHUNK_SIZE (int): The default chunk size (in bytes) used
            for streaming file uploads to prevent memory overload. Defaults to 1 MB.
        MONGODB_URL (str): The connection string for the MongoDB database.
        MONGODB (str): The specific database name to use within MongoDB.
    """
    class Config:
        env_file=".env"

    APP_NAME:str
    VERSION:str
    OPEN_API_KEYS:str
    
    # 1 MB chunk size is used to process uploads in manageable pieces
    FILE_DEFAULT_CHUNK_SIZE:int = 1024 * 1024
    
    MONGODB_URL:str
    MONGODB:str


def get_settings():
    """
    Retrieves a validated instance of the application settings.

    This function instantiates the `Settings` class, triggering the load
    and validation of the `.env` file. It can be used as a FastAPI dependency.

    Returns:
        Settings: The populated configuration object.
    """
    return Settings()