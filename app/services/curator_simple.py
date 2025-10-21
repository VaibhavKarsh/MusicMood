"""
Simplified Playlist Curator - Direct tool execution without ReAct agent complexity.

This provides a reliable curation pipeline by calling tools directly in sequence.
"""

import logging
from typing import Dict, Any, Optional, List
import json
import time

from app.tools.curator_tools import (
    rank_tracks_by_relevance,
    optimize_diversity,
    generate_explanation
)

logger = logging.getLogger(__name__)


def curate_playlist_simple(
    candidate_tracks: List[Dict[str, Any]],
    mood_data: Dict[str, Any],
    user_context: Optional[Dict[str, Any]] = None,
    desired_count: int = 30
) -> Dict[str, Any]:
    """
    Curate a playlist using direct tool execution (simplified, reliable).
    
    Args:
        candidate_tracks: List of track dictionaries with audio features
        mood_data: Mood data from Agent 1
        user_context: Optional user preferences and history
        desired_count: Number of tracks for final playlist (default 30)
        
    Returns:
        Dictionary with:
        - playlist: List of curated tracks
        - explanation: Natural language explanation
        - diversity_metrics: Diversity statistics
        - execution_time: Time taken to curate
    """
    start_time = time.time()
    
    try:
        # Handle candidate_tracks if it comes in as string
        if isinstance(candidate_tracks, str):
            candidate_tracks = json.loads(candidate_tracks)
        
        # Handle mood_data if it comes in as string
        if isinstance(mood_data, str):
            mood_data = json.loads(mood_data)
        
        # Check if tracks have audio features (premium feature)
        has_audio_features = any(
            track.get('tempo') is not None and track.get('energy') is not None 
            for track in candidate_tracks[:5]  # Check first 5 tracks
        )
        
        if not has_audio_features:
            logger.warning("[CURATOR] Audio features missing - Premium feature required for advanced curation")
            return {
                "success": False,
                "premium_feature_required": True,
                "error": "Audio features unavailable",
                "message": (
                    "Advanced playlist curation requires Spotify Premium API access for audio analysis. "
                    "Features like tempo matching, energy level optimization, and mood-based ranking "
                    "need audio features data (tempo, energy, valence, danceability). "
                    "Upgrade to Premium to unlock AI-powered playlist curation."
                ),
                "playlist": [],
                "explanation": "Premium feature required for advanced playlist curation.",
                "diversity_metrics": {},
                "execution_time": round(time.time() - start_time, 2)
            }
        
        logger.info(f"Curating playlist from {len(candidate_tracks)} candidates for mood: {mood_data.get('primary_mood')}")
        
        # Step 1: Rank tracks by relevance
        logger.info("Step 1: Ranking tracks by relevance...")
        rank_input = {
            "tracks_json": json.dumps(candidate_tracks),
            "mood_data_json": json.dumps(mood_data),
            "user_context_json": json.dumps(user_context or {})
        }
        
        ranked_result = rank_tracks_by_relevance(json.dumps(rank_input))
        
        # Parse ranked result
        try:
            ranked_data = json.loads(ranked_result)
            if isinstance(ranked_data, list):
                ranked_tracks = ranked_data
            elif isinstance(ranked_data, dict) and 'error' in ranked_data:
                logger.error(f"Ranking error: {ranked_data['error']}")
                return {
                    "error": ranked_data['error'],
                    "execution_time": round(time.time() - start_time, 2),
                    "playlist": [],
                    "explanation": "Failed to rank tracks."
                }
            else:
                ranked_tracks = ranked_data
        except Exception as e:
            logger.error(f"Error parsing ranked result: {e}")
            return {
                "error": str(e),
                "execution_time": round(time.time() - start_time, 2),
                "playlist": [],
                "explanation": "Failed to parse ranked tracks."
            }
        
        logger.info(f"Ranked {len(ranked_tracks)} tracks")
        
        # Step 2: Optimize for diversity
        logger.info(f"Step 2: Optimizing diversity for {desired_count} tracks...")
        
        diversity_input = {
            "ranked_tracks_json": json.dumps(ranked_tracks),
            "desired_count": desired_count
        }
        
        diversity_result = optimize_diversity(json.dumps(diversity_input))
        diversity_data = json.loads(diversity_result)
        
        playlist = diversity_data.get('playlist', [])
        diversity_metrics = diversity_data.get('diversity_metrics', {})
        
        logger.info(f"Optimized playlist with {len(playlist)} tracks")
        
        # Step 3: Generate explanation
        logger.info("Step 3: Generating explanation...")
        explanation_input = {
            "playlist_json": json.dumps(diversity_data),
            "mood_data_json": json.dumps(mood_data)
        }
        
        explanation_result = generate_explanation(json.dumps(explanation_input))
        explanation_data = json.loads(explanation_result)
        
        explanation = explanation_data.get('explanation', 'Curated playlist for your mood.')
        
        logger.info(f"Generated explanation: {explanation[:100]}...")
        
        execution_time = time.time() - start_time
        
        logger.info(f"Curation complete in {execution_time:.2f}s")
        
        return {
            "playlist": playlist,
            "explanation": explanation,
            "diversity_metrics": diversity_metrics,
            "track_count": len(playlist),
            "execution_time": round(execution_time, 2),
            "steps_completed": ["ranking", "diversity_optimization", "explanation_generation"]
        }
        
    except Exception as e:
        logger.error(f"Error curating playlist: {e}")
        execution_time = time.time() - start_time
        
        return {
            "error": str(e),
            "execution_time": round(execution_time, 2),
            "playlist": [],
            "explanation": "Failed to curate playlist due to an error."
        }
