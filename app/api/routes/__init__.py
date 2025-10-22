"""
API Routes Package

Contains all FastAPI route handlers organized by resource
"""

from app.api.routes.playlists import router as playlists_router

__all__ = ["playlists_router"]
