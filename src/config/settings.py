"""Application settings and configuration"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application
    app_name: str = "Intelli-Credit Engine"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/intellicredit"
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "intellicredit-documents"
    
    # OCR Configuration
    textract_enabled: bool = True
    ocr_confidence_threshold: float = 0.85
    
    # Cross-Verification Thresholds
    revenue_variance_threshold: float = 10.0  # percentage
    
    # API Keys (for external services)
    google_search_api_key: Optional[str] = None
    google_search_engine_id: Optional[str] = None
    ecourts_api_key: Optional[str] = None
    mca_api_key: Optional[str] = None
    
    # Processing Configuration
    max_document_size_mb: int = 100
    processing_timeout_minutes: int = 30
    
    # Security
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


# Global settings instance
settings = Settings()
