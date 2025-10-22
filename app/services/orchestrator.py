"""
Multi-Agent Orchestrator

Coordinates the execution of all three agents in sequence:
1. Agent 1: Mood Understanding Agent
2. Agent 2: Music Discovery (Spotify Integration)
3. Agent 3: Playlist Curator

This orchestrator manages the data flow between agents and provides
a unified interface for end-to-end playlist generation.
"""

import logging
import time
from typing import Dict, Any, Optional

from app.agents.mood_agent import create_mood_agent
from app.tools.spotify_tools import search_spotify_by_mood
from app.services.curator_simple import curate_playlist_simple

logger = logging.getLogger(__name__)

# Cache agent instance
_mood_agent_cache = None


def generate_playlist_with_agents(
    user_input: str,
    user_id: Optional[str] = None,
    desired_count: int = 30
) -> Dict[str, Any]:
    """
    Generate a personalized playlist using the 3-agent pipeline.

    Pipeline:
    1. Agent 1 (Mood Understanding): Analyzes user input → mood_data
    2. Agent 2 (Music Discovery): Searches Spotify → candidate_tracks
    3. Agent 3 (Playlist Curator): Curates final playlist → final_playlist + explanation

    Args:
        user_input: Natural language mood description from user
        user_id: Optional user ID for personalization
        desired_count: Number of tracks in final playlist (default 30)

    Returns:
        Dictionary containing:
        - playlist: List of curated tracks
        - explanation: Natural language explanation
        - mood_data: Original mood analysis
        - diversity_metrics: Playlist diversity statistics
        - execution_times: Performance breakdown by agent
        - total_execution_time: Total pipeline time
    """
    pipeline_start_time = time.time()

    result = {
        "success": False,
        "playlist": [],
        "explanation": "",
        "mood_data": {},
        "diversity_metrics": {},
        "execution_times": {},
        "total_execution_time": 0,
        "pipeline_steps": []
    }

    try:
        logger.info("=" * 80)
        logger.info("MULTI-AGENT ORCHESTRATION STARTED")
        logger.info(f"User Input: {user_input}")
        logger.info(f"User ID: {user_id}")
        logger.info(f"Desired Count: {desired_count}")
        logger.info("=" * 80)

        # ================================================================
        # AGENT 1: MOOD UNDERSTANDING
        # ================================================================
        logger.info("\n[AGENT 1] Mood Understanding Agent - Starting...")
        agent1_start = time.time()

        try:
            # Get or create mood agent (cached)
            global _mood_agent_cache
            if _mood_agent_cache is None:
                _mood_agent_cache = create_mood_agent()
            mood_agent = _mood_agent_cache

            mood_result = mood_agent.analyze_mood(user_input, user_id=user_id)

            if mood_result.get('error'):
                logger.error(f"Agent 1 error: {mood_result['error']}")
                result['error'] = f"Mood analysis failed: {mood_result['error']}"
                return result

            mood_data = mood_result.get('mood_data', {})
            agent1_time = time.time() - agent1_start

            result['mood_data'] = mood_data
            result['execution_times']['agent1_mood_understanding'] = round(agent1_time, 2)
            result['pipeline_steps'].append('agent1_mood_understanding')

            logger.info(f"[AGENT 1] Complete in {agent1_time:.2f}s")
            logger.info(f"[AGENT 1] Mood: {mood_data.get('primary_mood')} (energy: {mood_data.get('energy_level')}/10)")

        except Exception as e:
            logger.error(f"[AGENT 1] Error: {e}")
            result['error'] = f"Agent 1 failed: {str(e)}"
            return result

        # ================================================================
        # AGENT 2: MUSIC DISCOVERY (SPOTIFY)
        # ================================================================
        logger.info("\n[AGENT 2] Music Discovery (Spotify) - Starting...")
        agent2_start = time.time()

        try:
            # Use Spotify search tool to find candidate tracks
            import json
            from app.tools.spotify_tools import get_audio_features_batch

            search_result_json = search_spotify_by_mood(json.dumps(mood_data))
            search_result = json.loads(search_result_json)

            if search_result.get('error'):
                logger.error(f"Agent 2 error: {search_result['error']}")
                result['error'] = f"Music discovery failed: {search_result['error']}"
                return result

            candidate_tracks = search_result.get('tracks', [])
            logger.info(f"[AGENT 2] Found {len(candidate_tracks)} candidate tracks")

            if len(candidate_tracks) == 0:
                result['error'] = "No tracks found for this mood"
                return result

            # Enrich tracks with audio features (PREMIUM FEATURE - requires Spotify Premium API access)
            logger.info(f"[AGENT 2] Fetching audio features from Spotify API (Premium Feature)...")
            track_ids = [track['id'] for track in candidate_tracks]
            features_result_json = get_audio_features_batch(json.dumps(track_ids))
            features_result = json.loads(features_result_json)

            if features_result.get('error'):
                # Audio features unavailable - this is a premium feature
                logger.warning(f"[AGENT 2] Audio features API unavailable - Premium feature required")
                logger.warning(f"[AGENT 2] Error: {features_result.get('error')}")
                result['premium_feature_required'] = True
                result['premium_feature_message'] = (
                    "Advanced playlist curation with audio analysis (tempo, energy, mood matching) "
                    "requires Spotify Premium API access. Upgrade to Premium for AI-powered mood matching."
                )
            else:
                features_map = {f['id']: f for f in features_result.get('audio_features', [])}

                # Merge audio features into candidate tracks
                enriched_tracks = []
                for track in candidate_tracks:
                    features = features_map.get(track['id'])
                    if features:
                        # Add audio features to track
                        track.update({
                            'tempo': features.get('tempo'),
                            'energy': features.get('energy'),
                            'valence': features.get('valence'),
                            'danceability': features.get('danceability'),
                            'acousticness': features.get('acousticness'),
                            'instrumentalness': features.get('instrumentalness'),
                            'loudness': features.get('loudness'),
                            'speechiness': features.get('speechiness'),
                        })
                    enriched_tracks.append(track)

                candidate_tracks = enriched_tracks
                logger.info(f"[AGENT 2] ✓ Enriched {len(enriched_tracks)} tracks with audio features")

            agent2_time = time.time() - agent2_start

            result['candidate_tracks_count'] = len(candidate_tracks)
            result['execution_times']['agent2_music_discovery'] = round(agent2_time, 2)
            result['pipeline_steps'].append('agent2_music_discovery')

            logger.info(f"[AGENT 2] Complete in {agent2_time:.2f}s")

        except Exception as e:
            logger.error(f"[AGENT 2] Error: {e}")
            result['error'] = f"Agent 2 failed: {str(e)}"
            return result

        # ================================================================
        # AGENT 3: PLAYLIST CURATOR
        # ================================================================
        logger.info("\n[AGENT 3] Playlist Curator - Starting...")
        agent3_start = time.time()

        try:
            # Get user context (placeholder for now)
            user_context = {
                "user_id": user_id or "anonymous",
                "favorite_artists": [],
                "favorite_genres": [],
                "recent_artists": []
            }

            # Curate playlist using simplified curator
            curation_result = curate_playlist_simple(
                candidate_tracks=candidate_tracks,
                mood_data=mood_data,
                user_context=user_context,
                desired_count=min(desired_count, len(candidate_tracks))
            )

            # Check for curation errors
            if curation_result.get('error'):
                logger.error(f"Agent 3 error: {curation_result['error']}")
                result['error'] = f"Playlist curation failed: {curation_result['error']}"
                return result
                return result

            agent3_time = time.time() - agent3_start

            result['playlist'] = curation_result.get('playlist', [])
            result['explanation'] = curation_result.get('explanation', '')
            result['diversity_metrics'] = curation_result.get('diversity_metrics', {})
            result['execution_times']['agent3_playlist_curator'] = round(agent3_time, 2)
            result['pipeline_steps'].append('agent3_playlist_curator')

            logger.info(f"[AGENT 3] Complete in {agent3_time:.2f}s")
            logger.info(f"[AGENT 3] Curated {len(result['playlist'])} tracks")

        except Exception as e:
            logger.error(f"[AGENT 3] Error: {e}")
            result['error'] = f"Agent 3 failed: {str(e)}"
            return result

        # ================================================================
        # PIPELINE COMPLETE
        # ================================================================
        total_time = time.time() - pipeline_start_time
        result['total_execution_time'] = round(total_time, 2)
        result['success'] = True

        logger.info("\n" + "=" * 80)
        logger.info("MULTI-AGENT ORCHESTRATION COMPLETE")
        logger.info(f"Total Execution Time: {total_time:.2f}s")
        logger.info(f"Agent 1: {result['execution_times']['agent1_mood_understanding']:.2f}s")
        logger.info(f"Agent 2: {result['execution_times']['agent2_music_discovery']:.2f}s")
        logger.info(f"Agent 3: {result['execution_times']['agent3_playlist_curator']:.2f}s")
        logger.info(f"Final Playlist: {len(result['playlist'])} tracks")
        logger.info(f"Diversity Score: {result['diversity_metrics'].get('diversity_score', 0):.1f}/100")
        logger.info("=" * 80)

        return result

    except Exception as e:
        logger.error(f"Orchestration error: {e}")
        total_time = time.time() - pipeline_start_time
        result['error'] = f"Pipeline failed: {str(e)}"
        result['total_execution_time'] = round(total_time, 2)
        return result


def generate_playlist_with_error_handling(
    user_input: str,
    user_id: Optional[str] = None,
    desired_count: int = 30
) -> Dict[str, Any]:
    """
    Generate playlist with comprehensive error handling and fallbacks.

    This wrapper provides additional error handling around the main
    orchestration function.
    """
    try:
        return generate_playlist_with_agents(user_input, user_id, desired_count)
    except Exception as e:
        logger.error(f"Fatal orchestration error: {e}")
        return {
            "success": False,
            "error": f"Fatal error: {str(e)}",
            "playlist": [],
            "explanation": "Unable to generate playlist due to a system error.",
            "total_execution_time": 0
        }
