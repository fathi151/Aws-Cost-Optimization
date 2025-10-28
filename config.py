"""
Configuration Management Module
Centralized configuration for the FinOps Chatbot
"""

import os
import logging
from typing import Any, Dict, Optional
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class"""

    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

    # Mistral AI Configuration
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small")

    # ChromaDB Configuration
    CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./data/chromadb")
    CHROMADB_COLLECTION_PREFIX = os.getenv("CHROMADB_COLLECTION_PREFIX", "finops")

    # Flask Configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///finops.db")
    DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False") == "True"

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/finops.log")

    # Data Processing Configuration
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour

    # Scheduler Configuration
    ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "True") == "True"
    SYNC_INTERVAL_HOURS = int(os.getenv("SYNC_INTERVAL_HOURS", 24))
    SYNC_HOUR = int(os.getenv("SYNC_HOUR", 0))
    SYNC_MINUTE = int(os.getenv("SYNC_MINUTE", 0))

    # Analytics Configuration
    ANOMALY_DETECTION_METHOD = os.getenv("ANOMALY_DETECTION_METHOD", "isolation_forest")
    ANOMALY_THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", 2.0))
    FORECAST_DAYS = int(os.getenv("FORECAST_DAYS", 30))
    CONFIDENCE_LEVEL = float(os.getenv("CONFIDENCE_LEVEL", 0.95))

    # API Configuration
    API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", 100))
    API_RATE_LIMIT_WINDOW = int(os.getenv("API_RATE_LIMIT_WINDOW", 3600))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Security Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-key-change-in-production")
    JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", 86400))  # 24 hours

    # Feature Flags
    ENABLE_ADVANCED_ANALYTICS = os.getenv("ENABLE_ADVANCED_ANALYTICS", "True") == "True"
    ENABLE_FORECASTING = os.getenv("ENABLE_FORECASTING", "True") == "True"
    ENABLE_ANOMALY_DETECTION = os.getenv("ENABLE_ANOMALY_DETECTION", "True") == "True"
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "True") == "True"

    # Notification Configuration
    ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "False") == "True"
    NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")
    NOTIFICATION_WEBHOOK = os.getenv("NOTIFICATION_WEBHOOK", "")

    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration
        
        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "AWS_REGION",
            "MISTRAL_API_KEY",
        ]

        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field, None):
                missing_fields.append(field)

        if missing_fields:
            logger.warning(f"Missing configuration fields: {missing_fields}")
            return False

        logger.info("Configuration validated successfully")
        return True

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert configuration to dictionary
        
        Returns:
            Dictionary of configuration values
        """
        config_dict = {}
        for key in dir(cls):
            if not key.startswith("_") and key.isupper():
                value = getattr(cls, key)
                # Don't include sensitive information
                if key in ["AWS_SECRET_ACCESS_KEY", "MISTRAL_API_KEY", "SECRET_KEY", "JWT_SECRET"]:
                    value = "***REDACTED***"
                config_dict[key] = value

        return config_dict


class DevelopmentConfig(Config):
    """Development configuration"""
    FLASK_DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""
    FLASK_DEBUG = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    FLASK_DEBUG = True
    LOG_LEVEL = "DEBUG"


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration based on environment
    
    Args:
        env: Environment name (development, production, testing)
    
    Returns:
        Configuration object
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_class = config_map.get(env, DevelopmentConfig)
    logger.info(f"Using {env} configuration")
    return config_class()


# Default configuration instance
config = get_config()
