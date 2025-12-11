# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    PROJECT_NAME: str = "Organization Management Service"
    API_V1_STR: str = "/api/v1"
    
    # Security Config (In production, load these from .env)
    SECRET_KEY: str = "super_secret_key_for_assignment_only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Config
    MONGO_URL: str = "mongodb+srv://sriKreeda:backendPass@cluster0.cbd9tlw.mongodb.net/?appName=Cluster0"
    MASTER_DB_NAME: str = "master_metadata"

    class Config:
        case_sensitive = True

settings = Settings()