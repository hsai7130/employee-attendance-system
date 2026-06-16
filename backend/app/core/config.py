from functools import lru_cache
from typing import List

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Employee Attendance System"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    SQLALCHEMY_DATABASE_URI: str = "YOUR_RAILWAY_DATABASE_URL"
    JWT_SECRET_KEY: str = "change_this_secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
    AUDIT_LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return self.BACKEND_CORS_ORIGINS


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
