# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings,SettingsConfigDict   


class Settings(BaseSettings):
    class Config:
        env_file=".env"
    APP_NAME:str
    VERSION:str
    OPEN_API_KEYS:str