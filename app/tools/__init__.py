"""
Tools package for LangChain agents.
Contains tools for mood analysis, user context, and Spotify interaction.
"""

from app.tools.mood_tools import get_mood_description, parse_mood_tool, parse_mood_with_llm
from app.tools.spotify_tools import (
    audio_features_tool,
    filter_tracks_by_audio_features,
    filter_tracks_tool,
    generate_search_queries,
    get_audio_features_batch,
    search_spotify_by_mood,
    search_spotify_tool,
)
from app.tools.user_tools import create_get_user_context_tool, get_user_context

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
