"""
Test script for Agent 3 (Playlist Curator).
"""

import json
from app.agents.curator_agent import create_curator_agent

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

# Mood data
mood_data = {
    "primary_mood": "happy",
    "energy_level": 8,
    "emotional_intensity": 7,
    "context": "general",
    "mood_tags": ["joyful", "upbeat", "positive"]
}

# User context (optional)
user_context = {
    "favorite_artists": ["Joy Makers"],
    "favorite_genres": ["pop", "dance"],
    "recent_artists": []
}

print("=" * 80)
print("AGENT 3: PLAYLIST CURATOR TEST")
print("=" * 80)

print(f"\nInput Data:")
print(f"   Candidate Tracks: {len(candidate_tracks)}")
print(f"   Mood: {mood_data['primary_mood']} (energy: {mood_data['energy_level']}/10)")
print(f"   Desired Playlist Size: 8 tracks")

print(f"\nCreating Playlist Curator Agent...")
agent = create_curator_agent()

print(f"\nCurating playlist...")
print("-" * 80)

result = agent.curate_playlist(
    candidate_tracks=candidate_tracks,
    mood_data=mood_data,
    user_context=user_context,
    desired_count=8
)

print("-" * 80)

if result.get('error'):
    print(f"\nError: {result['error']}")
else:
    playlist = result.get('playlist', [])
    explanation = result.get('explanation', '')
    metrics = result.get('diversity_metrics', {})
    execution_time = result.get('execution_time', 0)
    
    print(f"\nPlaylist Curation Complete!")
    print(f"   Execution Time: {execution_time:.2f}s")
    print(f"   Agent Steps: {result.get('intermediate_steps_count', 0)}")
    
    print(f"\nCurated Playlist ({len(playlist)} tracks):")
    for i, track in enumerate(playlist, 1):
        print(f"   {i:2d}. {track['name']:<25} by {track['artists'][0]['name']:<20}")
    
    print(f"\nDiversity Metrics:")
    print(f"   Unique Artists: {metrics.get('unique_artists', 'N/A')}")
    print(f"   Tempo Mean: {metrics.get('tempo_mean', 'N/A')} BPM")
    print(f"   Tempo Std Dev: {metrics.get('tempo_std', 'N/A')} BPM")
    print(f"   Energy Std Dev: {metrics.get('energy_std', 'N/A')}")
    print(f"   Diversity Score: {metrics.get('diversity_score', 'N/A')}/100")
    
    print(f"\nExplanation:")
    print(f"   \"{explanation}\"")
    
    # Verify agent used tools in correct order
    strategy = result.get('curation_strategy', {})
    tools_used = strategy.get('tools_used', [])
    
    print(f"\nTools Used:")
    for i, tool in enumerate(tools_used, 1):
        print(f"   {i}. {tool}")
    
    expected_order = ["rank_tracks_by_relevance", "optimize_diversity", "generate_explanation"]
    if tools_used == expected_order:
        print(f"\nAgent used tools in correct order!")
    else:
        print(f"\nAgent tool order differs from expected")
        print(f"   Expected: {expected_order}")
        print(f"   Actual: {tools_used}")

print(f"\n{'=' * 80}")
print("AGENT 3 TEST COMPLETE")
print("=" * 80)
