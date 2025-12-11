from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Organization Management Service"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MONGO_URL: str
    MASTER_DB_NAME: str = "master_metadata"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()