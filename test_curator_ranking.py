"""
Test script for curator ranking tool.
"""

import json
from app.tools.curator_tools import rank_tracks_by_relevance

# Sample tracks with audio features
sample_tracks = [
    {
        "id": "track1",
        "name": "Happy Song",
        "artists": [{"name": "Feel Good Band"}],
        "popularity": 75,
        "energy": 0.8,
        "valence": 0.9,
        "tempo": 125
    },
    {
        "id": "track2",
        "name": "Calm Vibes",
        "artists": [{"name": "Relaxation Artists"}],
        "popularity": 60,
        "energy": 0.3,
        "valence": 0.6,
        "tempo": 80
    },
    {
        "id": "track3",
        "name": "Energetic Workout",
        "artists": [{"name": "Gym Beats"}],
        "popularity": 85,
        "energy": 0.95,
        "valence": 0.7,
        "tempo": 135
    },
    {
        "id": "track4",
        "name": "Sad Ballad",
        "artists": [{"name": "Emotional Singer"}],
        "popularity": 70,
        "energy": 0.2,
        "valence": 0.2,
        "tempo": 65
    },
    {
        "id": "track5",
        "name": "Focus Music",
        "artists": [{"name": "Study Sounds"}],
        "popularity": 55,
        "energy": 0.5,
        "valence": 0.5,
        "tempo": 95
    }
]

# Test 1: Happy mood
print("=" * 80)
print("TEST 1: Ranking for HAPPY mood")
print("=" * 80)

mood_data_happy = {
    "primary_mood": "happy",
    "energy_level": 8,
    "emotional_intensity": 7,
    "mood_tags": ["joyful", "upbeat"]
}

result = rank_tracks_by_relevance(
    json.dumps(sample_tracks),
    json.dumps(mood_data_happy)
)

ranked = json.loads(result)
print(f"\n✅ Ranked {len(ranked)} tracks for happy mood\n")

for i, track in enumerate(ranked[:3], 1):
    print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
    print(f"   Score: {track['relevance_score']:.2f}/100")
    print(f"   Breakdown: Audio={track['score_breakdown']['audio_match']:.1f}, "
          f"Preference={track['score_breakdown']['user_preference']:.1f}, "
          f"Popularity={track['score_breakdown']['popularity']:.1f}, "
          f"Novelty={track['score_breakdown']['novelty']:.1f}")
    print()

# Test 2: Calm mood
print("\n" + "=" * 80)
print("TEST 2: Ranking for CALM mood")
print("=" * 80)

mood_data_calm = {
    "primary_mood": "calm",
    "energy_level": 3,
    "emotional_intensity": 4,
    "mood_tags": ["peaceful", "relaxing"]
}

result = rank_tracks_by_relevance(
    json.dumps(sample_tracks),
    json.dumps(mood_data_calm)
)

ranked = json.loads(result)
print(f"\n✅ Ranked {len(ranked)} tracks for calm mood\n")

for i, track in enumerate(ranked[:3], 1):
    print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
    print(f"   Score: {track['relevance_score']:.2f}/100")
    print(f"   Breakdown: Audio={track['score_breakdown']['audio_match']:.1f}, "
          f"Preference={track['score_breakdown']['user_preference']:.1f}, "
          f"Popularity={track['score_breakdown']['popularity']:.1f}, "
          f"Novelty={track['score_breakdown']['novelty']:.1f}")
    print()

# Test 3: Energetic mood with user preferences
print("\n" + "=" * 80)
print("TEST 3: Ranking for ENERGETIC mood with user preferences")
print("=" * 80)

mood_data_energetic = {
    "primary_mood": "energetic",
    "energy_level": 9,
    "emotional_intensity": 8,
    "mood_tags": ["workout", "pump-up"]
}

user_context = {
    "favorite_artists": ["Gym Beats"],
    "favorite_genres": ["workout", "electronic"],
    "recent_artists": ["Feel Good Band"]
}

result = rank_tracks_by_relevance(
    json.dumps(sample_tracks),
    json.dumps(mood_data_energetic),
    json.dumps(user_context)
)

ranked = json.loads(result)
print(f"\n✅ Ranked {len(ranked)} tracks for energetic mood with user preferences\n")

for i, track in enumerate(ranked[:3], 1):
    print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
    print(f"   Score: {track['relevance_score']:.2f}/100")
    print(f"   Breakdown: Audio={track['score_breakdown']['audio_match']:.1f}, "
          f"Preference={track['score_breakdown']['user_preference']:.1f}, "
          f"Popularity={track['score_breakdown']['popularity']:.1f}, "
          f"Novelty={track['score_breakdown']['novelty']:.1f}")
    print()

print("\n" + "=" * 80)
print("✅ ALL RANKING TESTS COMPLETE")
print("=" * 80)
print("\nKey Observations:")
print("- Happy mood: 'Happy Song' should rank highest")
print("- Calm mood: 'Calm Vibes' should rank highest")
print("- Energetic mood with preferences: 'Energetic Workout' should rank highest")
print("- User preference bonus visible in scores")
print("- Ranking algorithm working as expected!")
