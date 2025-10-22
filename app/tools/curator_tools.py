"""
Curator Tools for Agent 3 (Playlist Curator).

This module provides tools for track ranking, diversity optimization,
and explanation generation for playlist curation.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from app.config.settings import settings

logger = logging.getLogger(__name__)


def rank_tracks_by_relevance(input_str: str) -> str:
    """
    Rank tracks by relevance to mood and user preferences.

    Scoring algorithm (0-100):
    - Audio feature match to mood: 40% weight
    - User preference alignment: 30% weight
    - Track popularity: 20% weight
    - Novelty/diversity: 10% weight

    Args:
        input_str: JSON string OR dictionary string containing:
            - tracks_json: JSON string of tracks with audio features
            - mood_data_json: JSON string of mood data from Agent 1
            - user_context_json: Optional JSON string of user context/preferences

    Returns:
        JSON string of ranked tracks with relevance scores
    """
    try:
        logger.info("Ranking tracks by relevance to mood")

        # Parse input - handle both formats
        if isinstance(input_str, dict):
            # Already parsed
            input_data = input_str
        else:
            # Try to parse as JSON
            try:
                input_data = json.loads(input_str)
            except:
                # If not JSON, assume it's the tracks_json directly (backward compat)
                logger.warning("Could not parse input as JSON, using as tracks_json")
                return json.dumps({"error": "Invalid input format"})

        # Extract parameters
        tracks_json = input_data.get("tracks_json", input_data.get("ranked_tracks_json", "[]"))
        mood_data_json = input_data.get("mood_data_json", "{}")
        user_context_json = input_data.get("user_context_json", "{}")

        # Parse JSON strings
        tracks = json.loads(tracks_json) if isinstance(tracks_json, str) else tracks_json
        mood_data = (
            json.loads(mood_data_json) if isinstance(mood_data_json, str) else mood_data_json
        )
        user_context = (
            json.loads(user_context_json)
            if isinstance(user_context_json, str)
            else user_context_json
        )

        logger.info(
            f"Ranking {len(tracks)} tracks for mood: {mood_data.get('primary_mood', 'unknown')}"
        )

        # Extract mood requirements
        primary_mood = mood_data.get("primary_mood", "neutral")
        energy_level = mood_data.get("energy_level", 5)
        mood_tags = mood_data.get("mood_tags", [])

        # Get user preferences
        favorite_artists = user_context.get("favorite_artists", [])
        favorite_genres = user_context.get("favorite_genres", [])

        ranked_tracks = []

        for track in tracks:
            # Calculate relevance score components
            audio_score = _calculate_audio_feature_score(track, mood_data)
            preference_score = _calculate_preference_score(track, user_context)
            popularity_score = _calculate_popularity_score(track)
            novelty_score = _calculate_novelty_score(track, user_context)

            # Weighted sum
            total_score = (
                audio_score * 0.40
                + preference_score * 0.30
                + popularity_score * 0.20
                + novelty_score * 0.10
            )

            # Add score to track
            track_with_score = track.copy()
            track_with_score["relevance_score"] = round(total_score, 2)
            track_with_score["score_breakdown"] = {
                "audio_match": round(audio_score, 2),
                "user_preference": round(preference_score, 2),
                "popularity": round(popularity_score, 2),
                "novelty": round(novelty_score, 2),
            }

            ranked_tracks.append(track_with_score)

        # Sort by relevance score (descending)
        ranked_tracks.sort(key=lambda x: x["relevance_score"], reverse=True)

        logger.info(
            f"Ranked tracks - Top score: {ranked_tracks[0]['relevance_score']:.2f}, "
            f"Bottom score: {ranked_tracks[-1]['relevance_score']:.2f}"
        )
        logger.info(f"Top 5 tracks: {[t['name'] for t in ranked_tracks[:5]]}")

        return json.dumps(ranked_tracks, indent=2)

    except Exception as e:
        logger.error(f"Error ranking tracks: {e}")
        return json.dumps({"error": str(e)})


def _calculate_audio_feature_score(track: Dict[str, Any], mood_data: Dict[str, Any]) -> float:
    """
    Calculate how well track's audio features match the mood requirements.

    Returns score 0-100.
    """
    try:
        # Get mood requirements
        primary_mood = mood_data.get("primary_mood", "neutral")
        energy_level = mood_data.get("energy_level", 5) / 10.0  # Normalize to 0-1

        # Define mood-to-feature mappings
        mood_requirements = {
            "happy": {"energy": 0.7, "valence": 0.8, "tempo": 120},
            "excited": {"energy": 0.9, "valence": 0.8, "tempo": 130},
            "energetic": {"energy": 0.9, "valence": 0.7, "tempo": 130},
            "calm": {"energy": 0.3, "valence": 0.5, "tempo": 80},
            "relaxed": {"energy": 0.3, "valence": 0.6, "tempo": 75},
            "focused": {"energy": 0.5, "valence": 0.5, "tempo": 100},
            "sad": {"energy": 0.3, "valence": 0.2, "tempo": 70},
            "melancholy": {"energy": 0.3, "valence": 0.3, "tempo": 75},
            "angry": {"energy": 0.9, "valence": 0.3, "tempo": 140},
            "neutral": {"energy": 0.5, "valence": 0.5, "tempo": 100},
        }

        target_features = mood_requirements.get(primary_mood.lower(), mood_requirements["neutral"])

        # Get track features (with defaults for missing data)
        track_energy = track.get("energy", 0.5)
        track_valence = track.get("valence", 0.5)
        track_tempo = track.get("tempo", 100)

        # Calculate distance for each feature (lower = better match)
        energy_distance = abs(track_energy - target_features["energy"])
        valence_distance = abs(track_valence - target_features["valence"])
        tempo_distance = abs(track_tempo - target_features["tempo"]) / 200.0  # Normalize tempo

        # Convert distance to similarity score (0-100)
        # Perfect match = 0 distance = 100 score
        energy_score = (1 - energy_distance) * 100
        valence_score = (1 - valence_distance) * 100
        tempo_score = (1 - min(tempo_distance, 1.0)) * 100

        # Average the scores
        audio_score = (energy_score + valence_score + tempo_score) / 3

        return max(0, min(100, audio_score))

    except Exception as e:
        logger.warning(f"Error calculating audio feature score: {e}")
        return 50.0  # Default middle score


def _calculate_preference_score(track: Dict[str, Any], user_context: Dict[str, Any]) -> float:
    """
    Calculate how well track matches user preferences.

    Returns score 0-100.
    """
    try:
        score = 50.0  # Base score

        # Check favorite artists
        favorite_artists = user_context.get("favorite_artists", [])
        track_artists = track.get("artists", [])

        if favorite_artists and track_artists:
            for artist in track_artists:
                if artist.get("name", "").lower() in [fa.lower() for fa in favorite_artists]:
                    score += 30  # Big bonus for favorite artist
                    break

        # Check favorite genres
        favorite_genres = user_context.get("favorite_genres", [])
        track_genres = track.get("genres", [])

        if favorite_genres and track_genres:
            for genre in track_genres:
                if genre.lower() in [fg.lower() for fg in favorite_genres]:
                    score += 20  # Bonus for matching genre
                    break

        return max(0, min(100, score))

    except Exception as e:
        logger.warning(f"Error calculating preference score: {e}")
        return 50.0


def _calculate_popularity_score(track: Dict[str, Any]) -> float:
    """
    Calculate score based on track popularity.

    Balance popular tracks with niche discoveries.
    Returns score 0-100.
    """
    try:
        # Spotify popularity is 0-100
        popularity = track.get("popularity", 50)

        # Slightly favor popular tracks but not too heavily
        # Sweet spot is 60-80 popularity
        if 60 <= popularity <= 80:
            score = 100
        elif popularity > 80:
            score = 90  # Very popular, slight penalty
        elif popularity < 40:
            score = 70  # Niche, moderate penalty
        else:
            score = 85  # Moderate popularity

        return score

    except Exception as e:
        logger.warning(f"Error calculating popularity score: {e}")
        return 50.0


def _calculate_novelty_score(track: Dict[str, Any], user_context: Dict[str, Any]) -> float:
    """
    Calculate novelty score - reward new discoveries.

    Returns score 0-100.
    """
    try:
        score = 70.0  # Base score

        # Check if artist is new to user
        recent_artists = user_context.get("recent_artists", [])
        track_artists = track.get("artists", [])

        if track_artists and recent_artists:
            is_new_artist = True
            for artist in track_artists:
                if artist.get("name", "").lower() in [ra.lower() for ra in recent_artists]:
                    is_new_artist = False
                    break

            if is_new_artist:
                score += 30  # Bonus for new artist discovery

        return max(0, min(100, score))

    except Exception as e:
        logger.warning(f"Error calculating novelty score: {e}")
        return 70.0


# Create LangChain Tool wrapper
rank_tracks_tool = Tool(
    name="rank_tracks_by_relevance",
    func=rank_tracks_by_relevance,
    description="""Rank tracks by relevance to mood and user preferences.

    Input: Three JSON strings:
    1. tracks_json: List of tracks with audio features
    2. mood_data_json: Mood data from Agent 1
    3. user_context_json: (Optional) User preferences and history

    Returns: JSON string of tracks sorted by relevance score (0-100).
    Each track includes relevance_score and score_breakdown.

    Use this tool FIRST to identify the most relevant tracks for the mood.""",
)


def optimize_diversity(input_str: str) -> str:
    """
    Optimize playlist diversity while maintaining relevance.

    Applies diversity constraints:
    - Maximum 2 songs per artist
    - Tempo variety (spread across tempo range)
    - Energy curve (smooth transitions, no sudden jumps)
    - Good flow progression

    Args:
        input_str: JSON string OR dictionary string containing:
            - ranked_tracks_json: JSON string of ranked tracks (from rank_tracks_by_relevance)
            - desired_count: Number of tracks to include in final playlist (default 30)

    Returns:
        JSON string of optimized playlist with diversity metrics
    """
    try:
        # Parse input - handle both formats
        if isinstance(input_str, dict):
            input_data = input_str
        else:
            try:
                input_data = json.loads(input_str)
            except:
                # Backward compat: assume it's the ranked_tracks_json directly
                input_data = {"ranked_tracks_json": input_str, "desired_count": 30}

        # Extract parameters
        ranked_tracks_json = input_data.get("ranked_tracks_json", "[]")
        desired_count = input_data.get("desired_count", 30)

        # Ensure desired_count is an integer
        if isinstance(desired_count, str):
            desired_count = int(desired_count)

        logger.info(f"Optimizing diversity for playlist of {desired_count} tracks")

        # Parse ranked tracks - handle various formats
        if isinstance(ranked_tracks_json, str):
            try:
                ranked_tracks = json.loads(ranked_tracks_json)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse ranked_tracks_json: {e}")
                return json.dumps({"error": f"Invalid JSON: {str(e)}"})
        else:
            ranked_tracks = ranked_tracks_json

        if not ranked_tracks:
            logger.warning("No tracks provided for diversity optimization")
            return json.dumps({"error": "No tracks provided"})

        # Apply diversity constraints
        selected_tracks = _apply_diversity_constraints(ranked_tracks, desired_count)

        # Reorder tracks for smooth energy flow
        optimized_playlist = _optimize_energy_flow(selected_tracks)

        # Calculate diversity metrics
        diversity_metrics = _calculate_diversity_metrics(optimized_playlist)

        logger.info(f"Optimized playlist: {len(optimized_playlist)} tracks")
        logger.info(
            f"Diversity metrics: {diversity_metrics['unique_artists']} unique artists, "
            f"tempo std={diversity_metrics['tempo_std']:.1f}, "
            f"energy std={diversity_metrics['energy_std']:.3f}"
        )

        result = {
            "playlist": optimized_playlist,
            "diversity_metrics": diversity_metrics,
            "track_count": len(optimized_playlist),
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(f"Error optimizing diversity: {e}")
        return json.dumps({"error": str(e)})


def _apply_diversity_constraints(
    tracks: List[Dict[str, Any]], desired_count: int
) -> List[Dict[str, Any]]:
    """
    Select tracks while respecting diversity constraints.

    Constraints:
    - Maximum 2 songs per artist
    - Tempo variety across the playlist
    """
    selected = []
    artist_count = {}
    tempo_ranges = {"slow": 0, "medium": 0, "fast": 0}  # <90 BPM  # 90-120 BPM  # >120 BPM

    for track in tracks:
        if len(selected) >= desired_count:
            break

        # Check artist constraint
        artists = track.get("artists", [])
        if artists:
            # Handle both dict format (e.g. {'name': 'Artist'}) and string format (e.g. 'Artist')
            if isinstance(artists[0], dict):
                artist_name = artists[0].get("name", "Unknown")
            else:
                artist_name = str(artists[0])

            artist_count_current = artist_count.get(artist_name, 0)

            if artist_count_current >= 2:
                # Skip this track, artist already has 2 songs
                continue

            # Add track
            selected.append(track)
            artist_count[artist_name] = artist_count_current + 1

            # Update tempo distribution
            tempo = track.get("tempo", 100)
            if tempo < 90:
                tempo_ranges["slow"] += 1
            elif tempo <= 120:
                tempo_ranges["medium"] += 1
            else:
                tempo_ranges["fast"] += 1
        else:
            # No artist info, just add it
            selected.append(track)

    # If we didn't reach desired count, relax constraints
    if len(selected) < desired_count:
        logger.info(f"Relaxing artist constraint to reach {desired_count} tracks")

        for track in tracks:
            if len(selected) >= desired_count:
                break

            # Check if track already in selected
            if track not in selected:
                selected.append(track)

    logger.info(f"Selected {len(selected)} tracks with diversity constraints")
    logger.info(f"Artist constraint: Max 2 per artist applied")
    logger.info(
        f"Tempo distribution: Slow={tempo_ranges['slow']}, "
        f"Medium={tempo_ranges['medium']}, Fast={tempo_ranges['fast']}"
    )

    return selected


def _optimize_energy_flow(tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reorder tracks to create smooth energy progression.

    Strategy:
    - Start with medium-high energy
    - Create gentle curves (up and down)
    - Avoid sudden jumps
    - End with satisfying energy level
    """
    if not tracks:
        return tracks

    # Sort by energy for easier arrangement
    tracks_by_energy = sorted(tracks, key=lambda t: t.get("energy", 0.5))

    # Create energy curve
    optimized = []

    # Start with medium-high energy (60-70th percentile)
    start_idx = int(len(tracks_by_energy) * 0.6)
    optimized.append(tracks_by_energy[start_idx])
    remaining = [t for i, t in enumerate(tracks_by_energy) if i != start_idx]

    # Alternate between slightly higher and lower energy
    current_energy = optimized[0].get("energy", 0.5)

    while remaining and len(optimized) < len(tracks):
        # Find track with energy close to current (within 0.15)
        best_track = None
        best_distance = float("inf")

        for track in remaining:
            track_energy = track.get("energy", 0.5)
            distance = abs(track_energy - current_energy)

            if distance < best_distance:
                best_distance = distance
                best_track = track

        if best_track:
            optimized.append(best_track)
            remaining.remove(best_track)
            current_energy = best_track.get("energy", 0.5)
        else:
            # Fallback: just add first remaining
            optimized.append(remaining[0])
            current_energy = remaining[0].get("energy", 0.5)
            remaining.pop(0)

    logger.info(f"Optimized energy flow for {len(optimized)} tracks")

    return optimized


def _calculate_diversity_metrics(playlist: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate diversity metrics for the playlist.
    """
    if not playlist:
        return {"unique_artists": 0, "tempo_std": 0, "energy_std": 0, "diversity_score": 0}

    # Count unique artists
    unique_artists = set()
    for track in playlist:
        artists = track.get("artists", [])
        if artists:
            # Handle both dict format and string format
            if isinstance(artists[0], dict):
                unique_artists.add(artists[0].get("name", "Unknown"))
            else:
                unique_artists.add(str(artists[0]))

    # Calculate tempo statistics
    tempos = [track.get("tempo", 100) for track in playlist]
    tempo_mean = sum(tempos) / len(tempos)
    tempo_variance = sum((t - tempo_mean) ** 2 for t in tempos) / len(tempos)
    tempo_std = tempo_variance**0.5

    # Calculate energy statistics
    energies = [track.get("energy", 0.5) for track in playlist]
    energy_mean = sum(energies) / len(energies)
    energy_variance = sum((e - energy_mean) ** 2 for e in energies) / len(energies)
    energy_std = energy_variance**0.5

    # Calculate overall diversity score (0-100)
    # Based on: unique artists (40%), tempo variety (30%), energy variety (30%)
    artist_score = min(100, (len(unique_artists) / len(playlist)) * 100 * 1.5)
    tempo_score = min(100, tempo_std * 3)  # Good diversity = >20 BPM std
    energy_score = min(100, energy_std * 300)  # Good diversity = >0.15 std

    diversity_score = artist_score * 0.40 + tempo_score * 0.30 + energy_score * 0.30

    return {
        "unique_artists": len(unique_artists),
        "tempo_mean": round(tempo_mean, 1),
        "tempo_std": round(tempo_std, 1),
        "energy_mean": round(energy_mean, 3),
        "energy_std": round(energy_std, 3),
        "diversity_score": round(diversity_score, 2),
    }


# Create LangChain Tool wrapper
optimize_diversity_tool = Tool(
    name="optimize_diversity",
    func=optimize_diversity,
    description="""Optimize playlist diversity while maintaining relevance.

    Input: Two parameters:
    1. ranked_tracks_json: JSON string of ranked tracks (from rank_tracks_by_relevance)
    2. desired_count: Number of tracks for final playlist (default 30)

    Applies constraints:
    - Maximum 2 songs per artist
    - Tempo variety across playlist
    - Smooth energy curve (no sudden jumps)
    - Good flow progression

    Returns: JSON with optimized playlist and diversity metrics.

    Use this tool SECOND after ranking to build the final diverse playlist.""",
)


def generate_explanation(input_str: str) -> str:
    """
    Generate natural language explanation for playlist choices.

    Analyzes playlist characteristics and uses LLM to create a concise,
    helpful explanation of why these tracks match the user's mood.

    Args:
        input_str: JSON string OR dictionary string containing:
            - playlist_json: JSON string of final playlist (from optimize_diversity)
            - mood_data_json: JSON string of original mood data from Agent 1

    Returns:
        Natural language explanation (2-3 sentences)
    """
    try:
        logger.info("Generating playlist explanation")

        # Parse input - handle both formats
        if isinstance(input_str, dict):
            input_data = input_str
        else:
            try:
                input_data = json.loads(input_str)
            except:
                return json.dumps({"error": "Invalid input format"})

        # Extract parameters
        playlist_json = input_data.get("playlist_json", "{}")
        mood_data_json = input_data.get("mood_data_json", "{}")

        # Parse inputs
        playlist_data = (
            json.loads(playlist_json) if isinstance(playlist_json, str) else playlist_json
        )

        # Handle both direct playlist and wrapped format
        if isinstance(playlist_data, dict) and "playlist" in playlist_data:
            playlist = playlist_data["playlist"]
            diversity_metrics = playlist_data.get("diversity_metrics", {})
        else:
            playlist = playlist_data
            diversity_metrics = _calculate_diversity_metrics(playlist)

        mood_data = (
            json.loads(mood_data_json) if isinstance(mood_data_json, str) else mood_data_json
        )

        # Analyze playlist characteristics
        characteristics = _analyze_playlist_characteristics(playlist, diversity_metrics)

        # Generate explanation using template
        explanation = _generate_explanation_from_template(mood_data, characteristics)

        logger.info(f"Generated explanation: {explanation[:100]}...")

        return json.dumps(
            {"explanation": explanation, "characteristics": characteristics}, indent=2
        )

    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        return json.dumps({"error": str(e)})


def _analyze_playlist_characteristics(
    playlist: List[Dict[str, Any]], diversity_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze key characteristics of the playlist.
    """
    if not playlist:
        return {}

    # Calculate average energy
    energies = [track.get("energy", 0.5) for track in playlist]
    avg_energy = sum(energies) / len(energies)

    # Calculate average tempo
    tempos = [track.get("tempo", 100) for track in playlist]
    avg_tempo = sum(tempos) / len(tempos)

    # Calculate average valence
    valences = [track.get("valence", 0.5) for track in playlist]
    avg_valence = sum(valences) / len(valences)

    # Get top artists
    artist_counts = {}
    for track in playlist:
        artists = track.get("artists", [])
        if artists:
            # Handle both dict format and string format
            if isinstance(artists[0], dict):
                artist_name = artists[0].get("name", "Unknown")
            else:
                artist_name = str(artists[0])
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

    top_artists = sorted(artist_counts.items(), key=lambda x: -x[1])[:3]

    # Determine energy level description
    if avg_energy > 0.7:
        energy_desc = "high-energy"
    elif avg_energy > 0.4:
        energy_desc = "moderate-energy"
    else:
        energy_desc = "low-energy"

    # Determine tempo description
    if avg_tempo > 120:
        tempo_desc = "upbeat"
    elif avg_tempo > 90:
        tempo_desc = "mid-tempo"
    else:
        tempo_desc = "slow-paced"

    # Determine mood description
    if avg_valence > 0.6:
        mood_desc = "positive and uplifting"
    elif avg_valence > 0.4:
        mood_desc = "balanced"
    else:
        mood_desc = "emotional and reflective"

    return {
        "avg_energy": round(avg_energy, 2),
        "avg_tempo": round(avg_tempo, 1),
        "avg_valence": round(avg_valence, 2),
        "energy_desc": energy_desc,
        "tempo_desc": tempo_desc,
        "mood_desc": mood_desc,
        "unique_artists": diversity_metrics.get("unique_artists", len(artist_counts)),
        "top_artists": [artist for artist, _ in top_artists],
        "track_count": len(playlist),
    }


def _generate_explanation_from_template(
    mood_data: Dict[str, Any], characteristics: Dict[str, Any]
) -> str:
    """
    Generate explanation using mood-specific templates.
    """
    primary_mood = mood_data.get("primary_mood", "neutral").lower()
    energy_level = mood_data.get("energy_level", 5)

    # Get characteristics
    energy_desc = characteristics.get("energy_desc", "moderate-energy")
    tempo_desc = characteristics.get("tempo_desc", "mid-tempo")
    mood_desc = characteristics.get("mood_desc", "balanced")
    unique_artists = characteristics.get("unique_artists", 0)
    track_count = characteristics.get("track_count", 0)
    avg_tempo = characteristics.get("avg_tempo", 100)

    # Mood-specific templates
    templates = {
        "happy": f"I've curated {track_count} {energy_desc} tracks with {tempo_desc} rhythms to match your happy mood. "
        f"This playlist features {unique_artists} diverse artists with {mood_desc} vibes, "
        f"averaging {int(avg_tempo)} BPM to keep your positive energy flowing.",
        "excited": f"This {track_count}-track playlist brings the excitement with {energy_desc}, {tempo_desc} beats! "
        f"Featuring {unique_artists} different artists, these {mood_desc} tracks "
        f"will fuel your enthusiasm and keep the energy high.",
        "energetic": f"I've assembled {track_count} {energy_desc} tracks perfect for your energetic mood. "
        f"With {unique_artists} diverse artists and an average tempo of {int(avg_tempo)} BPM, "
        f"this playlist will power you through any activity.",
        "calm": f"This {track_count}-track collection offers {energy_desc}, {tempo_desc} music to help you relax. "
        f"Featuring {unique_artists} artists, these {mood_desc} tracks average {int(avg_tempo)} BPM, "
        f"creating the perfect peaceful atmosphere.",
        "relaxed": f"I've selected {track_count} {energy_desc} tracks from {unique_artists} artists to enhance your relaxation. "
        f"These {tempo_desc}, {mood_desc} songs create a soothing flow perfect for unwinding.",
        "focused": f"This {track_count}-track playlist is designed to enhance concentration with {energy_desc}, {tempo_desc} music. "
        f"Featuring {unique_artists} diverse artists, these {mood_desc} tracks maintain a steady {int(avg_tempo)} BPM "
        f"to help you stay in the zone.",
        "sad": f"I've curated {track_count} {energy_desc} tracks to honor your current mood. "
        f"With {unique_artists} thoughtful artists, these {mood_desc} songs provide comfort "
        f"while allowing you to process your emotions.",
        "melancholy": f"This {track_count}-track collection embraces melancholy with {energy_desc}, {tempo_desc} selections. "
        f"Featuring {unique_artists} artists, these {mood_desc} tracks offer cathartic beauty "
        f"at a reflective {int(avg_tempo)} BPM.",
        "angry": f"I've assembled {track_count} {energy_desc} tracks to channel your intensity. "
        f"These {tempo_desc} songs from {unique_artists} artists deliver {mood_desc} power, "
        f"averaging {int(avg_tempo)} BPM to match your fierce energy.",
    }

    # Get template for mood (or use neutral default)
    explanation = templates.get(primary_mood)

    if not explanation:
        # Default template
        explanation = (
            f"I've curated {track_count} tracks featuring {unique_artists} diverse artists "
            f"to match your {primary_mood} mood. These {energy_desc}, {tempo_desc} selections "
            f"create a {mood_desc} atmosphere perfect for your current state."
        )

    return explanation


# Create LangChain Tool wrapper
generate_explanation_tool = Tool(
    name="generate_explanation",
    func=generate_explanation,
    description="""Generate natural language explanation for playlist.

    Input: Two JSON strings:
    1. playlist_json: Final playlist (from optimize_diversity)
    2. mood_data_json: Original mood data from Agent 1

    Analyzes playlist characteristics:
    - Average energy, tempo, valence
    - Artist diversity
    - Mood match quality

    Returns: JSON with concise 2-3 sentence explanation of why these tracks
    match the user's mood and what makes the playlist special.

    Use this tool LAST to explain your curation choices to the user.""",
)
