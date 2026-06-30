# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file=".env"
    APP_NAME:str
    VERSION:str
    OPEN_API_KEYS:str
    FILE_DEFAULT_CHUNK_SIZE:int = 1024 * 1024  # 1 MB