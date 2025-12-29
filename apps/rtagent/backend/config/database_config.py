"""
PostgreSQL Database Configuration
==================================

Database connection configuration for PostgreSQL.
This module provides configuration for the Tool Registry platform's PostgreSQL database.
"""

import os
from typing import Optional


# ==============================================================================
# POSTGRESQL CONFIGURATION
# ==============================================================================

POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "artagent")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")

# Database URL (for SQLAlchemy and other ORMs)
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Connection pool settings
DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))

# Echo SQL queries (for debugging)
DB_ECHO: bool = os.getenv("DB_ECHO", "false").lower() == "true"


def get_database_url(async_driver: bool = False) -> str:
    """
    Get database URL for SQLAlchemy connection.
    
    Args:
        async_driver: If True, returns async driver URL (postgresql+asyncpg://),
                     otherwise returns sync driver URL (postgresql://)
    
    Returns:
        Database connection URL string
    """
    if async_driver:
        return DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    return DATABASE_URL


def get_connection_dict() -> dict:
    """
    Get database connection parameters as a dictionary.
    
    Returns:
        Dictionary with connection parameters (host, port, database, user, password)
    """
    return {
        "host": POSTGRES_HOST,
        "port": POSTGRES_PORT,
        "database": POSTGRES_DB,
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
    }


def validate_database_config() -> tuple[bool, Optional[str]]:
    """
    Validate database configuration.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not POSTGRES_HOST:
        return False, "POSTGRES_HOST is not configured"
    
    if not POSTGRES_DB:
        return False, "POSTGRES_DB is not configured"
    
    if not POSTGRES_USER:
        return False, "POSTGRES_USER is not configured"
    
    if not POSTGRES_PASSWORD:
        return False, "POSTGRES_PASSWORD is not configured"
    
    return True, None


if __name__ == "__main__":
    # Quick validation check
    is_valid, error = validate_database_config()
    
    if is_valid:
        print("✅ Database configuration is valid")
        print(f"Database URL: {DATABASE_URL}")
        print(f"Host: {POSTGRES_HOST}:{POSTGRES_PORT}")
        print(f"Database: {POSTGRES_DB}")
        print(f"User: {POSTGRES_USER}")
    else:
        print(f"❌ Database configuration is invalid: {error}")
