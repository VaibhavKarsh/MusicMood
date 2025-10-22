"""
Database connection and session management utilities.
"""

from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.config.settings import settings


# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Maximum overflow connections
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get database session.

    Yields:
        Session: SQLAlchemy database session

    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database session outside of FastAPI.

    Yields:
        Session: SQLAlchemy database session

    Example:
        with get_db_context() as db:
            users = db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """
    Event listener for database connections.
    Currently unused for PostgreSQL, but useful for SQLite.
    """
    pass


@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """
    Event listener when a connection is checked out from the pool.
    Useful for logging and monitoring.
    """
    pass


async def init_db():
    """
    Initialize database on application startup.
    Creates tables if they don't exist.

    Note: In production, use Alembic migrations instead.
    """
    # Import models to ensure they're registered
    from app.models import Base

    # Create tables (only for development/testing)
    # In production, use: alembic upgrade head
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)


async def close_db():
    """
    Close database connections on application shutdown.
    """
    engine.dispose()
