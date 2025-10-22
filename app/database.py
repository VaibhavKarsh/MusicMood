"""
Database module - Compatibility wrapper for app.db.database
This module provides backward compatibility for imports.
"""

from app.db.database import SessionLocal, close_db, engine, get_db, get_db_context, init_db
from app.models.base import Base

__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "get_db_context",
    "init_db",
    "close_db",
    "Base",
]
