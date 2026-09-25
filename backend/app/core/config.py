import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "NutriScan AI API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./nutriscan.db"
    
    # JWT Auth
    JWT_SECRET: str = "super_secret_nutriscan_jwt_key_change_in_production_min32chars_secure"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days for mobile convenience
    
    # Multimodal AI Service
    AI_PROVIDER: str = "gemini"  # 'gemini', 'openai', or 'smart_mock'
    AI_API_KEY: str = ""
    AI_MODEL: str = "gemini-2.0-flash"
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["*"]
    
    # Image constraints
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
