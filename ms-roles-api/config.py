"""
Configuration module for Cosmos DB connection and application settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings:
    """Application settings with Cosmos DB configuration."""
    
    # Cosmos DB settings
    COSMOS_ENDPOINT: str = os.getenv("COSMOS_ENDPOINT", "")
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "")
    COSMOS_DATABASE_NAME: str = os.getenv("COSMOS_DATABASE_NAME", "employees-db")
    COSMOS_CONTAINER_NAME: str = os.getenv("COSMOS_CONTAINER_NAME", "employees")
    
    # Feature flags
    USE_COSMOS_DB: bool = os.getenv("USE_COSMOS_DB", "false").lower() == "true"
    
    # Cache settings for performance optimization
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))  # 5 minutes default
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required Cosmos DB settings are present when USE_COSMOS_DB is True."""
        if cls.USE_COSMOS_DB:
            if not cls.COSMOS_ENDPOINT or not cls.COSMOS_KEY:
                raise ValueError(
                    "COSMOS_ENDPOINT and COSMOS_KEY must be set when USE_COSMOS_DB is enabled"
                )
        return True

# Global settings instance
settings = Settings()
