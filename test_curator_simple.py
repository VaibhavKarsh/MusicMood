"""
Test simplified curator (direct tool execution).
"""

from app.services.curator_simple import curate_playlist_simple

# Sample candidate tracks
candidate_tracks = [
    {"id": "1", "name": "Sunshine Day", "artists": [{"name": "Happy Folks"}], 
     "energy": 0.8, "valence": 0.9, "tempo": 125, "popularity": 75},
    {"id": "2", "name": "Feel Good Anthem", "artists": [{"name": "Joy Makers"}], 
     "energy": 0.75, "valence": 0.85, "tempo": 120, "popularity": 80},
    {"id": "3", "name": "Upbeat Groove", "artists": [{"name": "Happy Folks"}], 
     "energy": 0.78, "valence": 0.88, "tempo": 122, "popularity": 72},
    {"id": "4", "name": "Party Starter", "artists": [{"name": "Dance Kings"}], 
     "energy": 0.9, "valence": 0.85, "tempo": 128, "popularity": 85},
    {"id": "5", "name": "Good Vibes Only", "artists": [{"name": "Positive Crew"}], 
     "energy": 0.7, "valence": 0.8, "tempo": 115, "popularity": 70},
    {"id": "6", "name": "Smile More", "artists": [{"name": "Optimist Band"}], 
     "energy": 0.65, "valence": 0.75, "tempo": 110, "popularity": 65},
    {"id": "7", "name": "Happy Hour", "artists": [{"name": "Fun Times"}], 
     "energy": 0.82, "valence": 0.9, "tempo": 123, "popularity": 77},
    {"id": "8", "name": "Joyful Noise", "artists": [{"name": "Cheerful Sounds"}], 
     "energy": 0.76, "valence": 0.86, "tempo": 118, "popularity": 68},
    {"id": "9", "name": "Bright Side", "artists": [{"name": "Silver Linings"}], 
     "energy": 0.68, "valence": 0.78, "tempo": 112, "popularity": 62},
    {"id": "10", "name": "Celebrate Life", "artists": [{"name": "Joy Makers"}], 
     "energy": 0.85, "valence": 0.88, "tempo": 126, "popularity": 82},
]

mood_data = {
    "primary_mood": "happy",
    "energy_level": 8,
    "emotional_intensity": 7,
    "context": "general",
    "mood_tags": ["joyful", "upbeat", "positive"]
}

user_context = {
    "favorite_artists": ["Joy Makers"],
    "favorite_genres": ["pop", "dance"],
    "recent_artists": []
}

print("=" * 80)
print("SIMPLIFIED PLAYLIST CURATOR TEST")
print("=" * 80)

print(f"\nCurating playlist for {mood_data['primary_mood']} mood...")
print(f"Candidate tracks: {len(candidate_tracks)}")
print(f"Desired size: 8 tracks\n")

result = curate_playlist_simple(
    candidate_tracks=candidate_tracks,
    mood_data=mood_data,
    user_context=user_context,
    desired_count=8
)

if result.get('error'):
    print(f"ERROR: {result['error']}")
else:
    print(f"SUCCESS! Execution time: {result['execution_time']:.2f}s\n")
    
    playlist = result['playlist']
    print(f"Curated Playlist ({len(playlist)} tracks):")
    for i, track in enumerate(playlist, 1):
        print(f"  {i:2d}. {track['name']:<25} by {track['artists'][0]['name']:<20} "
              f"[Energy: {track['energy']:.2f}, Tempo: {int(track['tempo'])} BPM]")
    
    metrics = result['diversity_metrics']
    print(f"\nDiversity Metrics:")
    print(f"  Unique Artists: {metrics.get('unique_artists', 0)}")
    print(f"  Tempo Mean: {metrics.get('tempo_mean', 0)} BPM")
    print(f"  Tempo Std Dev: {metrics.get('tempo_std', 0)} BPM")
    print(f"  Energy Std Dev: {metrics.get('energy_std', 0):.3f}")
    print(f"  Diversity Score: {metrics.get('diversity_score', 0)}/100")
    
    print(f"\nExplanation:")
    print(f"  \"{result['explanation']}\"")
    
    print(f"\nSteps Completed:")
    for i, step in enumerate(result.get('steps_completed', []), 1):
        print(f"  {i}. {step}")

print(f"\n{'=' * 80}")
print("TEST COMPLETE")
print("=" * 80)
