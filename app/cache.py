"""
Redis cache module
Provides centralized Redis client for caching operations
"""

import redis

from app.config.settings import settings

# Create Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=settings.REDIS_DECODE_RESPONSES,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
)

__all__ = ["redis_client"]
