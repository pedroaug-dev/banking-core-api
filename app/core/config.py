from enum import Enum
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvironmentOption(str, Enum):
    """Application environment options"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings(BaseSettings):
    """
    Global Application settings
    Loaded from environment variables with .env fallback
    """

    # Pydantic Settings Configuration
    model_config =SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application Information
    PROJECT_NAME: str = "Nexus Bank Core API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: EnvironmentOption = EnvironmentOption.DEVELOPMENT
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Security
    JWT_SECRET_KEY: str = Field(
        default="YOUR_LOCAL_DEV_SECRET_KEY_HERE",
        description="Secret key for JWT token signing",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "nexus_bank_db"

    @property
    def ASYNC_DATABASE_URI(self) -> str:
        """
        Construct Asynchronous database URI for SQLAlchemy
        Format: postgresql+asyncpg://user:password@host:port/database
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis Cache Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    @property
    def REDIS_URI(self) -> str:
        """
        Construct Redis connection URI
        Format: redis://:password@host:port/db
        """
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


# Global Settings Singleton
settings = Settings()