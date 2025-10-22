"""
Pydantic models for API request/response validation
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# ============================================================================
# REQUEST MODELS
# ============================================================================


class GeneratePlaylistRequest(BaseModel):
    """Request model for generating a playlist"""

    user_input: str = Field(
        ...,
        description="Natural language mood description",
        min_length=1,
        max_length=500,
        examples=["I'm feeling happy and energetic today!", "Need focus music for work"],
    )

    user_id: Optional[str] = Field(
        default="anonymous", description="User ID for personalization (optional)", max_length=100
    )

    desired_count: int = Field(
        default=30, description="Number of tracks in final playlist", ge=5, le=50
    )

    @field_validator("user_input")
    @classmethod
    def validate_user_input(cls, v: str) -> str:
        """Validate user input is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError("User input cannot be empty")
        return v.strip()


class FeedbackRequest(BaseModel):
    """Request model for user feedback on playlists"""

    playlist_id: str = Field(..., description="ID of the playlist")
    user_id: str = Field(..., description="ID of the user providing feedback")
    rating: int = Field(..., description="Rating 1-5", ge=1, le=5)
    feedback_text: Optional[str] = Field(
        None, description="Optional text feedback", max_length=1000
    )
    liked_tracks: Optional[List[str]] = Field(
        default=[], description="List of track IDs user liked"
    )
    disliked_tracks: Optional[List[str]] = Field(
        default=[], description="List of track IDs user disliked"
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================


class TrackMetadata(BaseModel):
    """Track metadata model"""

    id: str
    name: str
    artist: str
    artists: List[str]
    album: str
    uri: str
    preview_url: Optional[str] = None
    duration_ms: int
    popularity: int
    explicit: bool
    external_url: str
    image_url: Optional[str] = None
    relevance_score: Optional[float] = None


class DiversityMetrics(BaseModel):
    """Diversity metrics model"""

    unique_artists: Optional[int] = None
    tempo_mean: Optional[float] = None
    tempo_std: Optional[float] = None
    energy_mean: Optional[float] = None
    energy_std: Optional[float] = None
    diversity_score: Optional[float] = None
    track_count: Optional[int] = None
    curation_method: Optional[str] = None


class MoodData(BaseModel):
    """Mood analysis data model"""

    primary_mood: str
    energy_level: int
    emotional_intensity: int
    context: str
    mood_tags: List[str]


class ExecutionTimes(BaseModel):
    """Execution time breakdown model"""

    agent1_mood_understanding: Optional[float] = None
    agent2_music_discovery: Optional[float] = None
    agent3_playlist_curator: Optional[float] = None


class GeneratePlaylistResponse(BaseModel):
    """Response model for playlist generation"""

    success: bool
    playlist: List[TrackMetadata]
    explanation: str
    mood_data: MoodData
    diversity_metrics: DiversityMetrics
    execution_times: ExecutionTimes
    total_execution_time: float
    pipeline_steps: List[str]
    candidate_tracks_count: Optional[int] = None
    premium_feature_required: Optional[bool] = None
    premium_feature_message: Optional[str] = None
    error: Optional[str] = None


class PlaylistSummary(BaseModel):
    """Summary of a saved playlist"""

    id: str
    user_id: str
    created_at: str
    mood: str
    track_count: int
    explanation: str
    tracks: Optional[List[Dict[str, Any]]] = None  # Full track details


class UserPlaylistsResponse(BaseModel):
    """Response model for user's playlists"""

    user_id: str
    playlists: List[PlaylistSummary]
    total_count: int


class MoodHistoryEntry(BaseModel):
    """Mood history entry model"""

    timestamp: str
    primary_mood: str
    energy_level: int
    user_input: str
    playlist_id: Optional[str] = None


class MoodHistoryResponse(BaseModel):
    """Response model for mood history"""

    user_id: str
    history: List[MoodHistoryEntry]
    total_count: int


class FeedbackResponse(BaseModel):
    """Response model for feedback submission"""

    success: bool
    message: str
    feedback_id: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response model"""

    status: str
    version: str
    environment: str
    services: Dict[str, str]


class ErrorResponse(BaseModel):
    """Standard error response model"""

    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None
