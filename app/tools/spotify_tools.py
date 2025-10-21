"""
Spotify Tools for Agent 2 (Music Discovery Agent)
Provides tools for searching Spotify and analyzing audio features
"""

import logging
import json
from typing import Dict, Any, List, Optional
from langchain.tools import Tool
from app.services.spotify import SpotifyClient
from app.config.settings import settings

logger = logging.getLogger(__name__)


# Mood to Spotify search query mapping
MOOD_TO_QUERY_MAP = {
    # Positive, high energy
    "happy": ["feel good", "upbeat", "cheerful", "joyful"],
    "energetic": ["workout", "pump up", "high energy", "motivational"],
    "excited": ["party", "celebration", "upbeat", "festive"],
    "euphoric": ["euphoric", "blissful", "ecstatic", "uplifting"],
    
    # Positive, low energy
    "calm": ["peaceful", "relaxing", "chill", "ambient"],
    "peaceful": ["meditation", "zen", "tranquil", "serene"],
    "content": ["easy listening", "mellow", "comfortable", "smooth"],
    "relaxed": ["lounge", "laid back", "easy", "soft"],
    
    # Negative, high energy
    "angry": ["aggressive", "intense", "metal", "hard rock"],
    "anxious": ["tense", "suspenseful", "dramatic", "intense"],
    "frustrated": ["intense", "aggressive", "powerful", "loud"],
    
    # Negative, low energy
    "sad": ["melancholy", "emotional", "heartbreak", "somber"],
    "melancholic": ["sad songs", "emotional", "reflective", "moody"],
    "depressed": ["downtempo", "melancholic", "blue", "somber"],
    "lonely": ["emotional", "introspective", "longing", "heartfelt"],
    
    # Neutral/Complex
    "nostalgic": ["throwback", "classic", "retro", "memories"],
    "romantic": ["love songs", "romantic", "intimate", "passionate"],
    "contemplative": ["introspective", "thoughtful", "reflective", "deep"],
    "focused": ["concentration", "study", "focus", "instrumental"],
    "dreamy": ["ethereal", "atmospheric", "dreamy", "ambient"],
}


# Context to genre/style mapping
CONTEXT_TO_STYLE_MAP = {
    "workout": ["workout", "gym", "fitness", "running"],
    "gym": ["workout", "fitness", "gym", "training"],
    "running": ["running", "cardio", "jogging", "exercise"],
    "studying": ["study", "concentration", "focus", "instrumental"],
    "work": ["focus", "productivity", "concentration", "background"],
    "party": ["party", "dance", "club", "upbeat"],
    "sleep": ["sleep", "lullaby", "calm", "peaceful"],
    "relaxing": ["chill", "relaxing", "calm", "easy listening"],
    "meditation": ["meditation", "zen", "mindfulness", "ambient"],
    "morning": ["morning", "wake up", "energizing", "fresh"],
    "evening": ["evening", "sunset", "mellow", "relaxed"],
    "night": ["night", "late night", "chill", "ambient"],
    "driving": ["road trip", "driving", "cruising", "highway"],
    "cooking": ["cooking", "jazz", "easy listening", "background"],
    "cleaning": ["cleaning", "upbeat", "energizing", "motivation"],
}


def generate_search_queries(mood_data: Dict[str, Any]) -> List[str]:
    """
    Generate Spotify search queries based on mood data
    
    Args:
        mood_data: Dictionary with mood information from Agent 1
            - primary_mood: Main mood (e.g., "happy", "sad")
            - energy_level: 1-10 scale
            - context: Activity context (e.g., "workout", "studying")
            - mood_tags: Additional mood descriptors
    
    Returns:
        List of search query strings
    """
    queries = []
    
    primary_mood = mood_data.get("primary_mood", "").lower()
    energy_level = mood_data.get("energy_level", 5)
    context = mood_data.get("context", "").lower()
    mood_tags = mood_data.get("mood_tags", [])
    
    # Add queries based on primary mood
    if primary_mood in MOOD_TO_QUERY_MAP:
        queries.extend(MOOD_TO_QUERY_MAP[primary_mood])
    
    # Add queries based on context
    if context in CONTEXT_TO_STYLE_MAP:
        queries.extend(CONTEXT_TO_STYLE_MAP[context])
    
    # Add energy-based queries
    if energy_level >= 8:
        queries.extend(["high energy", "intense", "powerful"])
    elif energy_level >= 6:
        queries.extend(["upbeat", "energetic", "lively"])
    elif energy_level <= 3:
        queries.extend(["slow", "calm", "peaceful"])
    
    # Add mood tag queries (limit to top 2)
    for tag in mood_tags[:2]:
        if isinstance(tag, str):
            queries.append(tag.lower())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_queries = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            unique_queries.append(q)
    
    # Limit to top 5 queries
    return unique_queries[:5]


def search_spotify_by_mood(mood_data_json: str) -> str:
    """
    Search Spotify for tracks based on mood data
    
    This tool takes mood data from Agent 1 and searches Spotify
    for relevant tracks. It generates multiple search queries based
    on the mood, energy level, and context, then returns a curated
    list of tracks.
    
    Args:
        mood_data_json: JSON string with mood data from Agent 1
            Example: {"primary_mood": "happy", "energy_level": 8, 
                     "context": "workout", "mood_tags": ["motivated"]}
    
    Returns:
        JSON string with search results containing track information
    """
    try:
        # Parse mood data
        mood_data = json.loads(mood_data_json)
        logger.info(f"Searching Spotify for mood: {mood_data.get('primary_mood')}")
        
        # Generate search queries
        queries = generate_search_queries(mood_data)
        logger.info(f"Generated {len(queries)} search queries: {queries}")
        
        # Initialize Spotify client
        spotify_client = SpotifyClient()
        
        # Collect tracks from multiple queries
        all_tracks = []
        track_ids_seen = set()
        
        # Search with each query
        for query in queries:
            try:
                # Search for tracks (limit per query)
                result = spotify_client.search(
                    query=query,
                    search_type="track",
                    limit=20,  # 20 tracks per query
                    market="US"
                )
                
                # Extract tracks
                if "tracks" in result and "items" in result["tracks"]:
                    for track in result["tracks"]["items"]:
                        track_id = track.get("id")
                        
                        # Skip duplicates
                        if track_id in track_ids_seen:
                            continue
                        
                        track_ids_seen.add(track_id)
                        
                        # Extract relevant track info
                        track_info = {
                            "id": track_id,
                            "name": track["name"],
                            "artist": track["artists"][0]["name"],
                            "artists": [a["name"] for a in track["artists"]],
                            "album": track["album"]["name"],
                            "uri": track["uri"],
                            "preview_url": track.get("preview_url"),
                            "duration_ms": track.get("duration_ms"),
                            "popularity": track.get("popularity", 0),
                            "explicit": track.get("explicit", False),
                            "external_url": track["external_urls"].get("spotify", ""),
                            "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                        }
                        
                        all_tracks.append(track_info)
                        
                        # Stop if we have enough tracks
                        if len(all_tracks) >= 100:
                            break
                
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {e}")
                continue
            
            # Stop if we have enough tracks
            if len(all_tracks) >= 100:
                break
        
        # Sort by popularity and limit to 50-100 tracks
        all_tracks.sort(key=lambda x: x["popularity"], reverse=True)
        final_tracks = all_tracks[:100]
        
        logger.info(f"Found {len(final_tracks)} tracks for mood '{mood_data.get('primary_mood')}'")
        
        # Return results as JSON
        result = {
            "success": True,
            "mood_data": mood_data,
            "queries_used": queries,
            "total_tracks": len(final_tracks),
            "tracks": final_tracks
        }
        
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in mood_data: {e}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    except Exception as e:
        error_msg = f"Error searching Spotify: {e}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})


def get_audio_features_batch(track_ids_json: str) -> str:
    """
    Get audio features for a batch of tracks
    
    Audio features include:
    - energy: 0.0-1.0 (intensity and activity)
    - valence: 0.0-1.0 (musical positiveness/happiness)
    - danceability: 0.0-1.0 (how suitable for dancing)
    - tempo: BPM (beats per minute)
    - acousticness: 0.0-1.0 (confidence the track is acoustic)
    - instrumentalness: 0.0-1.0 (predicts if track has no vocals)
    - speechiness: 0.0-1.0 (presence of spoken words)
    - liveness: 0.0-1.0 (presence of audience)
    - loudness: dB (overall loudness)
    
    Args:
        track_ids_json: JSON string with list of Spotify track IDs
            Example: ["track_id_1", "track_id_2", ...]
    
    Returns:
        JSON string with audio features for each track
    """
    try:
        # Parse track IDs
        track_ids = json.loads(track_ids_json)
        
        if not isinstance(track_ids, list):
            return json.dumps({
                "success": False,
                "error": "track_ids must be a list"
            })
        
        logger.info(f"Getting audio features for {len(track_ids)} tracks")
        
        # Initialize Spotify client
        spotify_client = SpotifyClient()
        
        # Get audio features in batches (handled internally by client)
        features_dict = spotify_client.get_audio_features_batch(track_ids)
        
        # Convert dict to list format for response
        all_features = list(features_dict.values())
        
        logger.info(f"Retrieved audio features for {len(all_features)} tracks")
        
        # Return results
        result = {
            "success": True,
            "total_tracks": len(track_ids),
            "features_retrieved": len(all_features),
            "audio_features": all_features
        }
        
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in track_ids: {e}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    except Exception as e:
        error_msg = f"Error getting audio features: {e}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})


def get_mood_filtering_criteria(mood_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate filtering criteria based on mood data
    
    Args:
        mood_data: Mood data from Agent 1
        
    Returns:
        Dictionary with target audio feature values and tolerance
    """
    primary_mood = mood_data.get("primary_mood", "").lower()
    energy_level = mood_data.get("energy_level", 5)
    emotional_intensity = mood_data.get("emotional_intensity", 5)
    
    # Default criteria
    criteria = {
        "target_energy": None,
        "target_valence": None,
        "target_danceability": None,
        "target_tempo": None,
        "target_instrumentalness": None,
        "tolerance": 0.3
    }
    
    # Mood-specific criteria
    if primary_mood in ["happy", "excited", "euphoric"]:
        criteria["target_energy"] = 0.7 + (energy_level / 50)  # 0.7-0.9
        criteria["target_valence"] = 0.6 + (emotional_intensity / 50)  # 0.6-0.8
        criteria["target_danceability"] = 0.6
        
    elif primary_mood in ["energetic", "motivated"]:
        criteria["target_energy"] = 0.8 + (energy_level / 50)  # 0.8-1.0
        criteria["target_tempo"] = 120 + (energy_level * 8)  # 120-200 BPM
        criteria["target_danceability"] = 0.7
        
    elif primary_mood in ["calm", "peaceful", "relaxed"]:
        criteria["target_energy"] = 0.3 - (energy_level / 100)  # 0.2-0.4
        criteria["target_valence"] = 0.5
        criteria["target_tempo"] = 60 + (energy_level * 4)  # 60-100 BPM
        
    elif primary_mood in ["focused", "concentrating"]:
        criteria["target_energy"] = 0.4
        criteria["target_instrumentalness"] = 0.5  # Prefer instrumental
        criteria["target_valence"] = 0.5
        criteria["tolerance"] = 0.4  # More flexible
        
    elif primary_mood in ["sad", "melancholic", "depressed"]:
        criteria["target_valence"] = 0.2 + (emotional_intensity / 50)  # 0.2-0.4
        criteria["target_energy"] = 0.3
        criteria["target_tempo"] = 60 + (energy_level * 3)  # 60-90 BPM
        
    elif primary_mood in ["angry", "frustrated"]:
        criteria["target_energy"] = 0.9
        criteria["target_valence"] = 0.3
        criteria["target_tempo"] = 140 + (energy_level * 6)  # 140-200 BPM
    
    # Adjust tolerance based on emotional intensity
    if emotional_intensity >= 8:
        criteria["tolerance"] = 0.2  # Stricter matching for intense emotions
    elif emotional_intensity <= 3:
        criteria["tolerance"] = 0.4  # More flexible for mild emotions
    
    return criteria


def filter_tracks_by_audio_features(
    tracks_and_features_json: str,
    target_energy: Optional[float] = None,
    target_valence: Optional[float] = None,
    target_danceability: Optional[float] = None,
    tolerance: float = 0.3
) -> str:
    """
    Filter and rank tracks based on audio features matching target values
    
    Args:
        tracks_and_features_json: JSON with tracks and their audio features
        target_energy: Target energy level (0.0-1.0)
        target_valence: Target valence/happiness (0.0-1.0)
        target_danceability: Target danceability (0.0-1.0)
        tolerance: Acceptable difference from target (default 0.3)
    
    Returns:
        JSON string with filtered and ranked tracks
    """
    try:
        data = json.loads(tracks_and_features_json)
        
        tracks = data.get("tracks", [])
        features_map = {f["id"]: f for f in data.get("audio_features", [])}
        
        filtered_tracks = []
        
        for track in tracks:
            track_id = track.get("id")
            features = features_map.get(track_id)
            
            if not features:
                continue
            
            # Calculate match score
            score = 0.0
            comparisons = 0
            
            if target_energy is not None:
                energy_diff = abs(features.get("energy", 0.5) - target_energy)
                if energy_diff <= tolerance:
                    score += (1.0 - energy_diff)
                    comparisons += 1
            
            if target_valence is not None:
                valence_diff = abs(features.get("valence", 0.5) - target_valence)
                if valence_diff <= tolerance:
                    score += (1.0 - valence_diff)
                    comparisons += 1
            
            if target_danceability is not None:
                dance_diff = abs(features.get("danceability", 0.5) - target_danceability)
                if dance_diff <= tolerance:
                    score += (1.0 - dance_diff)
                    comparisons += 1
            
            if comparisons > 0:
                avg_score = score / comparisons
                
                # Add track with features and score
                filtered_tracks.append({
                    **track,
                    "audio_features": features,
                    "match_score": avg_score
                })
        
        # Sort by match score
        filtered_tracks.sort(key=lambda x: x["match_score"], reverse=True)
        
        logger.info(f"Filtered to {len(filtered_tracks)} matching tracks")
        
        return json.dumps({
            "success": True,
            "total_matches": len(filtered_tracks),
            "tracks": filtered_tracks
        }, indent=2)
        
    except Exception as e:
        error_msg = f"Error filtering tracks: {e}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})


def filter_tracks_by_mood_criteria(tracks_json: str, mood_data_json: str) -> str:
    """
    Filter tracks based on mood-derived criteria
    
    This is a higher-level function that automatically determines
    filtering criteria from mood data.
    
    Args:
        tracks_json: JSON string with track list
        mood_data_json: JSON string with mood data from Agent 1
        
    Returns:
        JSON string with filtered and ranked tracks
    """
    try:
        tracks = json.loads(tracks_json)
        mood_data = json.loads(mood_data_json)
        
        # Get mood-based criteria
        criteria = get_mood_filtering_criteria(mood_data)
        
        logger.info(f"Filtering tracks with criteria: {criteria}")
        
        # For now, filter by popularity and explicit content
        # (since audio features may not be available)
        filtered_tracks = []
        
        for track in tracks:
            # Basic filtering
            popularity = track.get("popularity", 0)
            explicit = track.get("explicit", False)
            
            # Skip very unpopular tracks
            if popularity < 20:
                continue
            
            # Apply mood-specific rules
            primary_mood = mood_data.get("primary_mood", "").lower()
            
            # Skip explicit tracks for calm/peaceful moods
            if primary_mood in ["calm", "peaceful", "focused"] and explicit:
                continue
            
            # Calculate basic score (can be enhanced with audio features)
            score = popularity / 100.0  # 0.0-1.0 scale
            
            filtered_tracks.append({
                **track,
                "match_score": score
            })
        
        # Sort by score
        filtered_tracks.sort(key=lambda x: x["match_score"], reverse=True)
        
        logger.info(f"Filtered {len(filtered_tracks)} tracks from {len(tracks)} total")
        
        return json.dumps({
            "success": True,
            "total_input": len(tracks),
            "total_matches": len(filtered_tracks),
            "criteria": criteria,
            "tracks": filtered_tracks
        }, indent=2)
        
    except Exception as e:
        error_msg = f"Error filtering tracks by mood: {e}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})


# LangChain Tool wrappers
search_spotify_tool = Tool(
    name="search_spotify_by_mood",
    func=search_spotify_by_mood,
    description="""
    Search Spotify for tracks based on mood data.
    
    Input: JSON string with mood data containing:
    - primary_mood: Main mood (e.g., "happy", "sad", "energetic")
    - energy_level: Energy level 1-10
    - context: Activity context (e.g., "workout", "studying")
    - mood_tags: List of additional mood descriptors
    
    Output: JSON string with tracks matching the mood (50-100 tracks)
    
    Example input:
    {"primary_mood": "happy", "energy_level": 8, "context": "workout", "mood_tags": ["motivated"]}
    """
)

audio_features_tool = Tool(
    name="get_audio_features_batch",
    func=get_audio_features_batch,
    description="""
    Get audio features for a batch of Spotify tracks.
    
    Audio features include energy, valence (happiness), danceability, tempo, etc.
    
    Input: JSON string with list of Spotify track IDs
    Example: ["track_id_1", "track_id_2", "track_id_3"]
    
    Output: JSON string with audio features for each track
    """
)

filter_tracks_tool = Tool(
    name="filter_tracks_by_audio_features",
    func=filter_tracks_by_audio_features,
    description="""
    Filter and rank tracks based on audio features.
    
    Matches tracks to target energy, valence, and danceability values.
    
    Input: JSON string with tracks and audio features, plus optional targets
    
    Output: JSON string with filtered and ranked tracks by match score
    """
)

mood_filter_tool = Tool(
    name="filter_tracks_by_mood_criteria",
    func=filter_tracks_by_mood_criteria,
    description="""
    Filter tracks based on mood-derived criteria.
    
    Automatically determines filtering criteria from mood data and applies
    appropriate filters (popularity, explicit content, etc.)
    
    Input: Two JSON strings - tracks list and mood data
    
    Output: JSON string with filtered and ranked tracks
    
    Example:
    tracks_json='[{"id": "abc", "name": "Track", "popularity": 75}]'
    mood_data_json='{"primary_mood": "calm", "energy_level": 3}'
    """
)
