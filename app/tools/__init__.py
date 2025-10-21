"""
Tools package for LangChain agents.
Contains tools for mood analysis, user context, and Spotify interaction.
"""

from app.tools.mood_tools import parse_mood_tool, parse_mood_with_llm, get_mood_description
from app.tools.user_tools import get_user_context, create_get_user_context_tool
from app.tools.spotify_tools import (
    search_spotify_tool,
    audio_features_tool,
    filter_tracks_tool,
    search_spotify_by_mood,
    get_audio_features_batch,
    filter_tracks_by_audio_features,
    generate_search_queries,
)

__all__ = [
    # Mood tools
    "parse_mood_tool",
    "parse_mood_with_llm",
    "get_mood_description",
    # User tools
    "get_user_context",
    "create_get_user_context_tool",
    # Spotify tools
    "search_spotify_tool",
    "audio_features_tool",
    "filter_tracks_tool",
    "search_spotify_by_mood",
    "get_audio_features_batch",
    "filter_tracks_by_audio_features",
    "generate_search_queries",
]
