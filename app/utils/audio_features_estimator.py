"""
Audio Features Estimator

Fallback for when Spotify audio features API is unavailable (403 errors).
Estimates audio features based on available track metadata.

Note: These are approximations and won't be as accurate as real audio features,
but allow the system to function when the API endpoint is restricted.
"""

import logging
import hashlib
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def estimate_audio_features(track: Dict[str, Any]) -> Dict[str, float]:
    """
    Estimate audio features from track metadata when API is unavailable.

    Uses heuristics based on:
    - Track name (keywords indicate mood/energy)
    - Artist name (consistent for pseudo-randomness)
    - Popularity (correlates with energy/danceability)
    - Duration (longer tracks often calmer/less energetic)
    - Explicit flag (correlates with higher energy)

    Args:
        track: Track dictionary with metadata

    Returns:
        Dictionary with estimated audio features
    """
    name = track.get('name', '').lower()
    artist = track.get('artist', '').lower()
    popularity = track.get('popularity', 50)
    duration_ms = track.get('duration_ms', 180000)  # Default 3 minutes
    explicit = track.get('explicit', False)

    # Generate pseudo-random but deterministic values based on track ID
    # This ensures same track always gets same estimates
    track_id = track.get('id', '')
    seed = int(hashlib.md5(track_id.encode()).hexdigest()[:8], 16) if track_id else 0

    # Base values (will be adjusted)
    energy = 0.5
    valence = 0.5
    danceability = 0.5
    tempo = 120.0
    acousticness = 0.3
    instrumentalness = 0.1
    speechiness = 0.05
    loudness = -8.0

    # Adjust based on popularity (popular tracks tend to be more energetic/danceable)
    pop_factor = popularity / 100.0
    energy += (pop_factor - 0.5) * 0.3
    danceability += (pop_factor - 0.5) * 0.2

    # Adjust based on duration (longer tracks often calmer)
    duration_minutes = duration_ms / 60000.0
    if duration_minutes > 5:
        energy -= 0.15
        acousticness += 0.1
        instrumentalness += 0.1
    elif duration_minutes < 2.5:
        energy += 0.1
        danceability += 0.1

    # Adjust based on explicit flag
    if explicit:
        energy += 0.1
        speechiness += 0.05

    # Keyword-based adjustments for energy and valence
    high_energy_keywords = ['energetic', 'party', 'dance', 'pump', 'hype', 'wild', 'crazy',
                             'rage', 'boom', 'fire', 'beast', 'power', 'hard', 'heavy']
    low_energy_keywords = ['calm', 'peaceful', 'quiet', 'soft', 'gentle', 'chill', 'relax',
                            'sleep', 'ambient', 'slow', 'serene', 'tranquil', 'meditation']

    happy_keywords = ['happy', 'joy', 'celebrate', 'party', 'fun', 'smile', 'love', 'good',
                       'feel good', 'sunshine', 'bright', 'cheerful', 'upbeat']
    sad_keywords = ['sad', 'tears', 'cry', 'lonely', 'broken', 'hurt', 'pain', 'goodbye',
                     'lost', 'dark', 'empty', 'alone', 'blue', 'melancholy']

    # Check name and artist for keywords
    combined_text = f"{name} {artist}"

    for keyword in high_energy_keywords:
        if keyword in combined_text:
            energy += 0.1
            tempo += 10
            danceability += 0.05
            break  # Only apply once

    for keyword in low_energy_keywords:
        if keyword in combined_text:
            energy -= 0.15
            tempo -= 15
            acousticness += 0.15
            instrumentalness += 0.1
            break

    for keyword in happy_keywords:
        if keyword in combined_text:
            valence += 0.2
            danceability += 0.1
            break

    for keyword in sad_keywords:
        if keyword in combined_text:
            valence -= 0.2
            energy -= 0.1
            acousticness += 0.1
            break

    # Use deterministic pseudo-random variation based on track ID
    # This adds variety while keeping same track consistent
    variation = ((seed % 1000) / 1000.0 - 0.5) * 0.2  # +/- 10%
    energy += variation
    valence += variation * 0.8
    danceability += variation * 0.6

    # Add tempo variation
    tempo_variation = ((seed % 500) / 500.0 - 0.5) * 40  # +/- 20 BPM
    tempo += tempo_variation

    # Clamp all values to valid ranges
    energy = max(0.0, min(1.0, energy))
    valence = max(0.0, min(1.0, valence))
    danceability = max(0.0, min(1.0, danceability))
    acousticness = max(0.0, min(1.0, acousticness))
    instrumentalness = max(0.0, min(1.0, instrumentalness))
    speechiness = max(0.0, min(1.0, speechiness))
    tempo = max(60.0, min(200.0, tempo))
    loudness = max(-20.0, min(0.0, loudness))

    return {
        'energy': round(energy, 3),
        'valence': round(valence, 3),
        'danceability': round(danceability, 3),
        'tempo': round(tempo, 1),
        'acousticness': round(acousticness, 3),
        'instrumentalness': round(instrumentalness, 3),
        'speechiness': round(speechiness, 3),
        'loudness': round(loudness, 1),
    }


def enrich_tracks_with_estimated_features(tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enrich a list of tracks with estimated audio features.

    Args:
        tracks: List of track dictionaries

    Returns:
        List of tracks with added audio feature estimates
    """
    enriched = []

    for track in tracks:
        # Skip if already has audio features
        if track.get('tempo') is not None and track.get('energy') is not None:
            enriched.append(track)
            continue

        # Estimate features
        features = estimate_audio_features(track)

        # Add to track
        track_with_features = track.copy()
        track_with_features.update(features)

        enriched.append(track_with_features)

    logger.info(f"Estimated audio features for {len(enriched)} tracks")

    return enriched
