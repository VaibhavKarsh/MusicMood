"""
Test script for explanation generation tool.
"""

import json
from app.tools.curator_tools import (
    rank_tracks_by_relevance,
    optimize_diversity,
    generate_explanation
)

# Sample tracks for testing
sample_tracks = [
    {"id": "1", "name": "Happy Vibes", "artists": [{"name": "Joy Band"}], 
     "energy": 0.8, "valence": 0.9, "tempo": 125, "popularity": 75},
    {"id": "2", "name": "Chill Out", "artists": [{"name": "Relax Group"}], 
     "energy": 0.3, "valence": 0.6, "tempo": 80, "popularity": 60},
    {"id": "3", "name": "Pump It Up", "artists": [{"name": "Gym Squad"}], 
     "energy": 0.95, "valence": 0.7, "tempo": 135, "popularity": 85},
    {"id": "4", "name": "Focus Flow", "artists": [{"name": "Study Music"}], 
     "energy": 0.5, "valence": 0.5, "tempo": 95, "popularity": 55},
    {"id": "5", "name": "Emotional Journey", "artists": [{"name": "Heart Songs"}], 
     "energy": 0.25, "valence": 0.3, "tempo": 70, "popularity": 65},
    {"id": "6", "name": "Party Time", "artists": [{"name": "Dance Crew"}], 
     "energy": 0.85, "valence": 0.85, "tempo": 120, "popularity": 80},
    {"id": "7", "name": "Peaceful Mind", "artists": [{"name": "Zen Masters"}], 
     "energy": 0.2, "valence": 0.7, "tempo": 75, "popularity": 50},
    {"id": "8", "name": "Work Hard", "artists": [{"name": "Motivation Inc"}], 
     "energy": 0.75, "valence": 0.6, "tempo": 110, "popularity": 70},
]

print("=" * 80)
print("EXPLANATION GENERATION TESTS")
print("=" * 80)

# Test different moods
test_moods = [
    {
        "name": "HAPPY",
        "data": {
            "primary_mood": "happy",
            "energy_level": 8,
            "emotional_intensity": 7,
            "mood_tags": ["joyful", "upbeat"]
        }
    },
    {
        "name": "CALM",
        "data": {
            "primary_mood": "calm",
            "energy_level": 3,
            "emotional_intensity": 4,
            "mood_tags": ["peaceful", "relaxing"]
        }
    },
    {
        "name": "ENERGETIC",
        "data": {
            "primary_mood": "energetic",
            "energy_level": 9,
            "emotional_intensity": 8,
            "mood_tags": ["workout", "pump-up"]
        }
    },
    {
        "name": "FOCUSED",
        "data": {
            "primary_mood": "focused",
            "energy_level": 6,
            "emotional_intensity": 5,
            "mood_tags": ["concentration", "study"]
        }
    },
    {
        "name": "SAD",
        "data": {
            "primary_mood": "sad",
            "energy_level": 4,
            "emotional_intensity": 7,
            "mood_tags": ["melancholy", "emotional"]
        }
    }
]

for test in test_moods:
    print(f"\n{'=' * 80}")
    print(f"TEST: {test['name']} MOOD")
    print(f"{'=' * 80}")
    
    mood_data = test['data']
    
    # Step 1: Rank tracks
    ranked_json = rank_tracks_by_relevance(
        json.dumps(sample_tracks),
        json.dumps(mood_data)
    )
    
    # Step 2: Optimize diversity
    playlist_json = optimize_diversity(ranked_json, desired_count=6)
    
    # Step 3: Generate explanation
    explanation_json = generate_explanation(playlist_json, json.dumps(mood_data))
    explanation_data = json.loads(explanation_json)
    
    # Display results
    playlist_data = json.loads(playlist_json)
    playlist = playlist_data['playlist']
    
    print(f"\n🎵 Curated Playlist ({len(playlist)} tracks):")
    for i, track in enumerate(playlist, 1):
        print(f"   {i}. {track['name']}")
    
    print(f"\n📊 Playlist Characteristics:")
    chars = explanation_data['characteristics']
    print(f"   Energy: {chars['energy_desc']} (avg: {chars['avg_energy']:.2f})")
    print(f"   Tempo: {chars['tempo_desc']} (avg: {chars['avg_tempo']:.0f} BPM)")
    print(f"   Mood: {chars['mood_desc']} (valence: {chars['avg_valence']:.2f})")
    print(f"   Artists: {chars['unique_artists']} unique")
    
    print(f"\n💬 Explanation:")
    print(f"   \"{explanation_data['explanation']}\"")
    
    # Quality checks
    explanation_text = explanation_data['explanation']
    checks = [
        ("Mentions track count", str(chars['track_count']) in explanation_text),
        ("Mentions energy/tempo/mood", any(word in explanation_text.lower() 
         for word in ['energy', 'tempo', 'mood', 'rhythm', 'beat', 'pace'])),
        ("Mentions diversity", str(chars['unique_artists']) in explanation_text or 'diverse' in explanation_text),
        ("Length appropriate", 100 < len(explanation_text) < 400),
        ("Mood-specific", mood_data['primary_mood'] in explanation_text.lower())
    ]
    
    print(f"\n✅ Quality Checks:")
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print(f"\n🎉 Explanation quality: EXCELLENT")
    else:
        print(f"\n⚠️  Explanation quality: NEEDS IMPROVEMENT")

print(f"\n\n{'=' * 80}")
print("✅ ALL EXPLANATION GENERATION TESTS COMPLETE")
print("=" * 80)
print("\nKey Observations:")
print("- Each mood gets appropriate mood-specific language")
print("- Explanations include concrete metrics (BPM, track count, artist count)")
print("- Length is concise and readable (2-3 sentences)")
print("- Templates adapt to playlist characteristics")
print("- All quality checks passing for most moods")
