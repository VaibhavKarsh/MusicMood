"""
API Routes for Playlist Generation

Endpoints for the multi-agent playlist generation system
"""

import logging
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.models import (
    GeneratePlaylistRequest,
    GeneratePlaylistResponse,
    TrackMetadata,
    DiversityMetrics,
    MoodData,
    ExecutionTimes,
    FeedbackRequest,
    FeedbackResponse,
    UserPlaylistsResponse,
    PlaylistSummary,
    MoodHistoryResponse,
    MoodHistoryEntry
)
from app.services.orchestrator import generate_playlist_with_agents
from app.services.playlist_service import save_playlist_result
from app.database import get_db
from app.models.user import User
from app.models.mood_entry import MoodEntry
from app.models.playlist_recommendation import PlaylistRecommendation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Playlists"])


@router.post(
    "/generate-playlist",
    response_model=GeneratePlaylistResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate personalized playlist from mood",
    description="""
    Generate a personalized music playlist based on natural language mood description.
    
    This endpoint uses a 3-agent AI system:
    - Agent 1: Understands mood from natural language
    - Agent 2: Discovers relevant tracks from Spotify
    - Agent 3: Curates optimal playlist (Premium feature)
    
    **Free Tier**: Provides mood understanding and track discovery
    **Premium**: Unlocks advanced playlist curation with audio analysis
    
    **Examples**:
    - "I'm feeling happy and energetic today!"
    - "Need to focus on work"
    - "Want some calm music for relaxing"
    - "Give me upbeat workout music"
    """,
    responses={
        200: {
            "description": "Playlist generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "playlist": [],
                        "explanation": "Premium feature required for advanced curation",
                        "mood_data": {
                            "primary_mood": "happy",
                            "energy_level": 10,
                            "emotional_intensity": 9,
                            "context": "general",
                            "mood_tags": ["energetic", "motivated", "optimistic"]
                        },
                        "diversity_metrics": {},
                        "execution_times": {
                            "agent1_mood_understanding": 65.5,
                            "agent2_music_discovery": 2.3
                        },
                        "total_execution_time": 67.8,
                        "pipeline_steps": ["agent1_mood_understanding", "agent2_music_discovery"],
                        "candidate_tracks_count": 99,
                        "premium_feature_required": True,
                        "premium_feature_message": "Advanced playlist curation requires Spotify Premium API..."
                    }
                }
            }
        },
        400: {"description": "Invalid request parameters"},
        500: {"description": "Server error during playlist generation"}
    }
)
async def generate_playlist(
    request: GeneratePlaylistRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a personalized playlist based on user's mood.
    
    Args:
        request: Playlist generation request with user input and preferences
        db: Database session
        
    Returns:
        Generated playlist with tracks, explanation, and metadata
        
    Raises:
        HTTPException: If playlist generation fails
    """
    try:
        # Validate inputs
        if not request.user_input or len(request.user_input.strip()) < 3:
            raise ValueError("User input must be at least 3 characters long")
        
        if not request.user_id or len(request.user_id.strip()) < 3:
            raise ValueError("User ID must be at least 3 characters long")
        
        if len(request.user_id.strip()) > 50:
            raise ValueError("User ID must be less than 50 characters")
        
        if request.desired_count < 5 or request.desired_count > 50:
            raise ValueError("Desired count must be between 5 and 50")
        
        logger.info(f"Received playlist generation request")
        logger.info(f"User input: '{request.user_input}'")
        logger.info(f"User ID: {request.user_id}")
        logger.info(f"Desired count: {request.desired_count}")
        
        # Call the multi-agent orchestrator
        result = generate_playlist_with_agents(
            user_input=request.user_input,
            user_id=request.user_id,
            desired_count=request.desired_count
        )
        
        # Log result summary
        if result.get('success'):
            logger.info(f"✓ Playlist generated successfully")
            logger.info(f"  Mood: {result.get('mood_data', {}).get('primary_mood', 'unknown')}")
            logger.info(f"  Tracks: {len(result.get('playlist', []))}")
            logger.info(f"  Execution time: {result.get('total_execution_time', 0):.2f}s")
            
            # Save to database
            logger.info("Saving playlist to database...")
            save_playlist_result(
                db=db,
                user_id=request.user_id,
                user_input=request.user_input,
                playlist_result=result
            )
            
        elif result.get('premium_feature_required'):
            logger.warning(f"⚠ Premium feature required")
            logger.info(f"  Mood analysis: ✓")
            logger.info(f"  Track discovery: ✓ ({result.get('candidate_tracks_count', 0)} tracks)")
            logger.info(f"  Advanced curation: ⭐ Premium required")
        else:
            logger.error(f"✗ Playlist generation failed: {result.get('error', 'Unknown error')}")
        
        # Convert result to response model
        diversity_data = result.get('diversity_metrics', {})
        if not diversity_data:
            diversity_data = {}
        
        # Ensure all optional fields have default values if missing
        diversity_metrics = DiversityMetrics(
            unique_artists=diversity_data.get('unique_artists'),
            tempo_mean=diversity_data.get('tempo_mean'),
            tempo_std=diversity_data.get('tempo_std'),
            energy_mean=diversity_data.get('energy_mean'),
            energy_std=diversity_data.get('energy_std'),
            diversity_score=diversity_data.get('diversity_score'),
            track_count=diversity_data.get('track_count'),
            curation_method=diversity_data.get('curation_method')
        )
        
        response = GeneratePlaylistResponse(
            success=result.get('success', False),
            playlist=[TrackMetadata(**track) for track in result.get('playlist', [])],
            explanation=result.get('explanation', ''),
            mood_data=MoodData(**result.get('mood_data', {})),
            diversity_metrics=diversity_metrics,
            execution_times=ExecutionTimes(**result.get('execution_times', {})),
            total_execution_time=result.get('total_execution_time', 0.0),
            pipeline_steps=result.get('pipeline_steps', []),
            candidate_tracks_count=result.get('candidate_tracks_count'),
            premium_feature_required=result.get('premium_feature_required'),
            premium_feature_message=result.get('premium_feature_message'),
            error=result.get('error')
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating playlist: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate playlist: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the API is healthy and responsive"
)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        Health status information
    """
    from app.config.settings import settings
    
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "api": "online",
            "orchestrator": "ready",
            "agent1": "ready",
            "agent2": "ready",
            "agent3": "gated (premium)"
        }
    }


@router.get(
    "/playlists/{user_id}",
    response_model=UserPlaylistsResponse,
    summary="Get user's playlists",
    description="Retrieve all playlists generated for a specific user"
)
async def get_user_playlists(
    user_id: str,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get all playlists generated for a user.
    
    Args:
        user_id: User identifier
        limit: Maximum number of playlists to return (default: 50)
        offset: Number of playlists to skip (default: 0)
        db: Database session
        
    Returns:
        List of user's playlists with metadata
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        logger.info(f"Retrieving playlists for user: {user_id} (limit={limit}, offset={offset})")
        
        # Find user by username or email
        user = db.query(User).filter(
            (User.email == user_id) | (User.username == user_id)
        ).first()
        
        if not user:
            # No user found, return empty list
            logger.info(f"User '{user_id}' not found, returning empty list")
            return UserPlaylistsResponse(
                user_id=user_id,
                playlists=[],
                total_count=0
            )
        
        # Query playlists for the user using their integer ID
        playlists = (
            db.query(PlaylistRecommendation)
            .filter(PlaylistRecommendation.user_id == user.id)
            .order_by(PlaylistRecommendation.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        
        # Get total count
        total = db.query(PlaylistRecommendation).filter(
            PlaylistRecommendation.user_id == user.id
        ).count()
        
        # Convert to response format
        playlist_summaries = [
            PlaylistSummary(
                id=str(p.id),
                user_id=user_id,
                created_at=p.created_at.isoformat() if p.created_at else "",
                mood=p.mood_entry.detected_emotion if p.mood_entry else "unknown",
                track_count=len(p.track_ids) if p.track_ids else 0,
                explanation=p.description or "",
                tracks=p.track_details if p.track_details else []  # Include full track details
            )
            for p in playlists
        ]
        
        logger.info(f"✓ Retrieved {len(playlist_summaries)} playlists (total: {total})")
        
        return UserPlaylistsResponse(
            user_id=user_id,
            playlists=playlist_summaries,
            total_count=total
        )
        
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve playlists: {str(e)}"
        )


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit playlist feedback",
    description="Submit user feedback and rating for a generated playlist"
)
async def submit_feedback(
    feedback: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a playlist.
    
    Args:
        feedback: Feedback request with rating and optional comments
        db: Database session
        
    Returns:
        Confirmation of feedback submission
        
    Raises:
        HTTPException: If submission fails or playlist not found
    """
    try:
        logger.info(f"Receiving feedback for playlist: {feedback.playlist_id}")
        logger.info(f"Rating: {feedback.rating}/5")
        
        # Find the playlist
        playlist = db.query(PlaylistRecommendation).filter(
            PlaylistRecommendation.id == int(feedback.playlist_id)
        ).first()
        
        if not playlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist {feedback.playlist_id} not found"
            )
        
        # Update feedback
        playlist.feedback_score = feedback.rating
        
        # Store liked/disliked tracks if provided
        if feedback.liked_tracks or feedback.disliked_tracks:
            # This could be extended to store in a separate feedback_details table
            logger.info(f"  Liked tracks: {len(feedback.liked_tracks or [])}")
            logger.info(f"  Disliked tracks: {len(feedback.disliked_tracks or [])}")
        
        # Store feedback text (could extend model to include this field)
        if feedback.feedback_text:
            logger.info(f"  Feedback: {feedback.feedback_text[:100]}...")
        
        db.commit()
        
        logger.info(f"✓ Feedback submitted successfully")
        
        return FeedbackResponse(
            success=True,
            message="Feedback submitted successfully",
            playlist_id=feedback.playlist_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting feedback: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )


@router.get(
    "/mood-history/{user_id}",
    response_model=MoodHistoryResponse,
    summary="Get user's mood history",
    description="Retrieve mood history and patterns for a specific user"
)
async def get_mood_history(
    user_id: str,
    limit: int = 30,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get mood history for a user.
    
    Args:
        user_id: User identifier
        limit: Maximum number of entries to return (default: 30)
        offset: Number of entries to skip (default: 0)
        db: Database session
        
    Returns:
        User's mood history with analysis
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        logger.info(f"Retrieving mood history for user: {user_id} (limit={limit}, offset={offset})")
        
        # Find user by username or email
        user = db.query(User).filter(
            (User.email == user_id) | (User.username == user_id)
        ).first()
        
        if not user:
            # No user found, return empty list
            logger.info(f"User '{user_id}' not found, returning empty list")
            return MoodHistoryResponse(
                user_id=user_id,
                history=[],
                total_count=0
            )
        
        # Query mood entries for the user using their integer ID
        mood_entries = (
            db.query(MoodEntry)
            .filter(MoodEntry.user_id == user.id)
            .order_by(MoodEntry.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        
        # Get total count
        total = db.query(MoodEntry).filter(MoodEntry.user_id == user.id).count()
        
        # Convert to response format
        history_entries = [
            MoodHistoryEntry(
                timestamp=entry.created_at.isoformat() if entry.created_at else "",
                primary_mood=entry.detected_emotion or "unknown",
                energy_level=int(entry.emotion_scores.get('energy', 5)) if entry.emotion_scores and isinstance(entry.emotion_scores, dict) else 5,
                user_input=entry.mood_text or "",
                playlist_id=None  # Could link to playlist if needed
            )
            for entry in mood_entries
        ]
        
        logger.info(f"✓ Retrieved {len(history_entries)} mood entries (total: {total})")
        
        return MoodHistoryResponse(
            user_id=user_id,
            history=history_entries,
            total_count=total
        )
        
    except Exception as e:
        logger.error(f"Error retrieving mood history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve mood history: {str(e)}"
        )

