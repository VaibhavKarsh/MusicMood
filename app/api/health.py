"""
Health check router for monitoring service status
"""

from datetime import datetime
from typing import Any, Dict

import httpx
import redis
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.db import get_db

router = APIRouter(tags=["health"])


async def check_database(db: Session) -> Dict[str, Any]:
    """Check database connectivity and health."""
    try:
        # Execute simple query
        result = db.execute(text("SELECT 1"))
        result.fetchone()

        # Get version
        version_result = db.execute(text("SELECT version()"))
        version = version_result.fetchone()[0].split(",")[0]

        # Count tables
        tables_result = db.execute(
            text(
                """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
            )
        )
        table_count = tables_result.fetchone()[0]

        return {
            "status": "healthy",
            "version": version,
            "tables": table_count,
            "response_time_ms": 0,  # Could add timing
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


async def check_redis() -> Dict[str, Any]:
    """Check Redis connectivity and health."""
    try:
        r = redis.from_url(
            settings.REDIS_URL,
            decode_responses=settings.REDIS_DECODE_RESPONSES,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )

        # Test connection
        r.ping()

        # Get info
        info = r.info()

        return {
            "status": "healthy",
            "version": info.get("redis_version", "unknown"),
            "connected_clients": info.get("connected_clients", 0),
            "used_memory_human": info.get("used_memory_human", "unknown"),
            "uptime_seconds": info.get("uptime_in_seconds", 0),
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


async def check_ollama() -> Dict[str, Any]:
    """Check Ollama service connectivity."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check if Ollama is running
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")

            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]

                # Check if configured model is available
                configured_model_available = any(
                    settings.OLLAMA_MODEL in name for name in model_names
                )

                return {
                    "status": "healthy",
                    "available_models": len(models),
                    "configured_model": settings.OLLAMA_MODEL,
                    "model_available": configured_model_available,
                    "all_models": model_names[:5],  # First 5 models
                }
            else:
                return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Comprehensive health check endpoint.

    Checks:
    - API service status
    - Database connectivity
    - Redis connectivity
    - Ollama service

    Returns:
        dict: Health status of all services
    """

    # Check all services
    db_health = await check_database(db)
    redis_health = await check_redis()
    ollama_health = await check_ollama()

    # Determine overall health
    all_healthy = (
        db_health["status"] == "healthy"
        and redis_health["status"] == "healthy"
        and ollama_health["status"] == "healthy"
    )

    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
        "services": {
            "api": {"status": "healthy", "uptime": "N/A"},  # Could add actual uptime tracking
            "database": db_health,
            "redis": redis_health,
            "ollama": ollama_health,
        },
    }


@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """
    Kubernetes liveness probe endpoint.
    Returns 200 if the service is running.
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Kubernetes readiness probe endpoint.
    Returns 200 if the service is ready to accept traffic.
    """

    # Check critical services
    db_health = await check_database(db)

    ready = db_health["status"] == "healthy"

    return {
        "status": "ready" if ready else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_health["status"],
    }
