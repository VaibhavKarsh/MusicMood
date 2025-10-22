"""
Playlist Service - Business logic for playlist management

Handles saving, retrieving, and managing playlists in the database
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.playlist_recommendation import PlaylistRecommendation
from app.models.mood_entry import MoodEntry
from app.models.user import User

logger = logging.getLogger(__name__)


def get_time_of_day() -> str:
    """
    Determine time of day based on current hour.
    
    Returns:
        Time period: morning, afternoon, evening, or night
    """
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def ensure_user_exists(db: Session, user_id: str) -> User:
    """
    Ensure user exists in database, create if not.
    
    Args:
        db: Database session
        user_id: User identifier (email or username)
        
    Returns:
        User object
    """
    # Try to find user by email or username
    user = db.query(User).filter(
        (User.email == user_id) | (User.username == user_id)
    ).first()
    
    if not user:
        # Create anonymous user with a dummy password hash
        user = User(
            username=user_id,
            email=f"{user_id}@anonymous.local" if "@" not in user_id else user_id,
            hashed_password="anonymous_no_auth",  # Dummy hash for anonymous users
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created new user: {user_id} (ID: {user.id})")
    
    return user


def save_mood_entry(
    db: Session,
    user: User,
    mood_text: str,
    mood_data: Dict[str, Any]
) -> MoodEntry:
    """
    Save mood entry to database.
    
    Args:
        db: Database session
        user: User object
        mood_text: Original user input text
        mood_data: Parsed mood data from Agent 1
        
    Returns:
        Created MoodEntry object
    """
    mood_entry = MoodEntry(
        user_id=user.id,
        mood_text=mood_text,
        detected_emotion=mood_data.get('primary_mood', 'unknown'),
        emotion_scores={
            'energy_level': mood_data.get('energy_level', 0),
            'emotional_intensity': mood_data.get('emotional_intensity', 0)
        },
        confidence_score=mood_data.get('emotional_intensity', 0) / 10.0,  # Normalize to 0-1
        time_of_day=get_time_of_day(),
        activity_context=mood_data.get('context', 'general')
    )
    
    db.add(mood_entry)
    db.commit()
    db.refresh(mood_entry)
    
    logger.info(f"Saved mood entry: {mood_entry.id} (emotion: {mood_entry.detected_emotion})")
    
    return mood_entry


def save_playlist_recommendation(
    db: Session,
    user: User,
    mood_entry: MoodEntry,
    playlist_data: Dict[str, Any]
) -> PlaylistRecommendation:
    """
    Save playlist recommendation to database.
    
    Args:
        db: Database session
        user: User object
        mood_entry: Associated mood entry
        playlist_data: Playlist data from orchestrator
        
    Returns:
        Created PlaylistRecommendation object
    """
    # Extract track data
    tracks = playlist_data.get('playlist', [])
    track_ids = [track.get('id') for track in tracks]
    track_details = [
        {
            'id': track.get('id'),
            'name': track.get('name'),
            'artist': track.get('artist'),
            'album': track.get('album'),
            'duration_ms': track.get('duration_ms'),
            'spotify_url': track.get('spotify_url'),
            'preview_url': track.get('preview_url')
        }
        for track in tracks
    ]
    
    # Generate playlist name from mood
    mood = mood_entry.detected_emotion
    playlist_name = f"{mood.capitalize()} Vibes - {datetime.now().strftime('%b %d, %Y')}"
    
    # Create playlist recommendation
    playlist_rec = PlaylistRecommendation(
        user_id=user.id,
        mood_entry_id=mood_entry.id,
        playlist_name=playlist_name,
        description=playlist_data.get('explanation', 'AI-generated playlist based on your mood'),
        track_ids=track_ids,
        track_details=track_details,
        genre_distribution={},  # Could be populated from track data
        audio_features_avg=playlist_data.get('diversity_metrics', {}),
        reasoning=playlist_data.get('explanation', ''),
        agent_used='multi_agent_orchestrator',
        feedback_score=None,
        was_listened=False,
        spotify_playlist_id=None
    )
    
    db.add(playlist_rec)
    db.commit()
    db.refresh(playlist_rec)
    
    logger.info(f"Saved playlist: {playlist_rec.id} (tracks: {len(track_ids)})")
    
    return playlist_rec


def save_playlist_result(
    db: Session,
    user_id: str,
    user_input: str,
    playlist_result: Dict[str, Any]
) -> Optional[PlaylistRecommendation]:
    """
    Save complete playlist generation result to database.
    
    Args:
        db: Database session
        user_id: User identifier
        user_input: Original user mood input
        playlist_result: Complete result from orchestrator
        
    Returns:
        Created PlaylistRecommendation object or None if save failed
    """
    try:
        # Only save successful playlists with tracks
        if not playlist_result.get('success') or not playlist_result.get('playlist'):
            logger.warning("Skipping database save - playlist generation incomplete")
            return None
        
        # Ensure user exists
        user = ensure_user_exists(db, user_id)
        
        # Save mood entry
        mood_entry = save_mood_entry(
            db=db,
            user=user,
            mood_text=user_input,
            mood_data=playlist_result.get('mood_data', {})
        )
        
        # Save playlist recommendation
        playlist_rec = save_playlist_recommendation(
            db=db,
            user=user,
            mood_entry=mood_entry,
            playlist_data=playlist_result
        )
        
        logger.info(f"✓ Successfully saved playlist generation result to database")
        
        return playlist_rec
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save playlist result to database: {e}", exc_info=True)
        return None
