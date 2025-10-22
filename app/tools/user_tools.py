"""
User context tools for retrieving user preferences and history.
"""

import json
import logging
from typing import Any, Dict, Optional

from langchain.tools import Tool
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import MoodEntry, PlaylistRecommendation, User

logger = logging.getLogger(__name__)


def get_user_context(user_id: str, db: Session) -> str:
    """
    Retrieve user context including preferences and mood history.

    Args:
        user_id: User ID as string (will be converted to int)
        db: Database session

    Returns:
        JSON string with user context data
    """

    try:
        user_id_int = int(user_id)
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return json.dumps({"error": "Invalid user_id format"})

    logger.info(f"Retrieving context for user {user_id_int}")

    try:
        # Get user
        user = db.query(User).filter(User.id == user_id_int).first()

        if not user:
            logger.warning(f"User {user_id_int} not found")
            return json.dumps(
                {"user_exists": False, "message": "User not found, using default preferences"}
            )

        # Get recent mood entries (last 10)
        recent_moods = (
            db.query(MoodEntry)
            .filter(MoodEntry.user_id == user_id_int)
            .order_by(desc(MoodEntry.created_at))
            .limit(10)
            .all()
        )

        # Get recent playlists (last 5)
        recent_playlists = (
            db.query(PlaylistRecommendation)
            .filter(PlaylistRecommendation.user_id == user_id_int)
            .order_by(desc(PlaylistRecommendation.created_at))
            .limit(5)
            .all()
        )

        # Analyze mood patterns
        mood_history = []
        mood_counts = {}
        for mood in recent_moods:
            mood_history.append(
                {
                    "emotion": mood.detected_emotion,
                    "confidence": mood.confidence_score,
                    "time_of_day": mood.time_of_day,
                    "date": mood.created_at.isoformat(),
                }
            )
            mood_counts[mood.detected_emotion] = mood_counts.get(mood.detected_emotion, 0) + 1

        # Find most common mood
        most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else None

        # Analyze playlist feedback
        playlist_feedback = []
        avg_feedback = None
        feedback_scores = []

        for playlist in recent_playlists:
            if playlist.feedback_score:
                feedback_scores.append(playlist.feedback_score)
                playlist_feedback.append(
                    {
                        "name": playlist.playlist_name,
                        "mood": (
                            playlist.mood_entry.detected_emotion
                            if playlist.mood_entry
                            else "unknown"
                        ),
                        "feedback": playlist.feedback_score,
                        "listened": playlist.was_listened,
                    }
                )

        if feedback_scores:
            avg_feedback = sum(feedback_scores) / len(feedback_scores)

        # Build context
        context = {
            "user_exists": True,
            "username": user.username,
            "has_spotify": bool(user.spotify_access_token),
            "mood_history": {
                "total_entries": len(recent_moods),
                "most_common_mood": most_common_mood,
                "recent_moods": mood_history[:5],  # Last 5 moods
            },
            "playlist_preferences": {
                "total_playlists": len(recent_playlists),
                "average_feedback": round(avg_feedback, 2) if avg_feedback else None,
                "recent_feedback": playlist_feedback[:3],  # Last 3 with feedback
            },
            "preferences": {
                "typical_mood": most_common_mood,
                "engagement_level": "high" if len(recent_moods) > 5 else "low",
            },
        }

        logger.info(
            f"Retrieved context for user {user_id_int}: {most_common_mood} mood, {len(recent_moods)} entries"
        )
        return json.dumps(context)

    except Exception as e:
        logger.error(f"Error retrieving user context: {e}")
        return json.dumps({"error": str(e), "user_exists": False})


def create_get_user_context_tool(db: Session) -> Tool:
    """
    Create a LangChain Tool for getting user context.

    Args:
        db: Database session to use for queries

    Returns:
        LangChain Tool instance
    """

    def get_context_wrapper(user_id: str) -> str:
        return get_user_context(user_id, db)

    return Tool(
        name="get_user_context",
        func=get_context_wrapper,
        description="""
        Retrieve user context including mood history and playlist preferences.
        Input: User ID as a string.
        Output: JSON with user's mood patterns, common moods, playlist feedback, and preferences.
        Use this tool to understand the user's historical preferences and patterns before making recommendations.
        """,
    )
