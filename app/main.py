"""
MusicMood FastAPI Application
Main application entry point with middleware and route configuration
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("=" * 70)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info("=" * 70)

    # Initialize database
    from app.db import init_db
    await init_db()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("=" * 70)
    logger.info(f"Shutting down {settings.APP_NAME}")

    # Close database connections
    from app.db import close_db
    await close_db()
    logger.info("Database connections closed")

    logger.info("=" * 70)


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="A Production-Grade 3-Agent AI System for Mood-Based Music Recommendations",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,  # Disable in production
    redoc_url="/redoc" if settings.DEBUG else None,
)


# Configure CORS middleware (must be first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    """
    Log all HTTP requests and responses
    """
    logger.info(f"Request: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


# Exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for all unhandled exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Include API routers
from app.api import health_router
from app.api.routes.playlists import router as playlists_router

app.include_router(health_router)
app.include_router(playlists_router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else "disabled",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
