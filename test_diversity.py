"""
Test script for diversity optimization tool.
"""

import json
from app.tools.curator_tools import rank_tracks_by_relevance, optimize_diversity

# Create a larger sample set with some repeated artists
sample_tracks = []

# Add tracks from various artists
artists_tracks = [
    ("Feel Good Band", [
        {"name": "Happy Song 1", "energy": 0.8, "valence": 0.9, "tempo": 125, "popularity": 75},
        {"name": "Happy Song 2", "energy": 0.75, "valence": 0.85, "tempo": 120, "popularity": 70},
        {"name": "Happy Song 3", "energy": 0.78, "valence": 0.88, "tempo": 122, "popularity": 72}
    ]),
    ("Relaxation Artists", [
        {"name": "Calm Vibes 1", "energy": 0.3, "valence": 0.6, "tempo": 80, "popularity": 60},
        {"name": "Calm Vibes 2", "energy": 0.25, "valence": 0.55, "tempo": 75, "popularity": 55},
        {"name": "Calm Vibes 3", "energy": 0.28, "valence": 0.58, "tempo": 78, "popularity": 58}
    ]),
    ("Gym Beats", [
        {"name": "Workout 1", "energy": 0.95, "valence": 0.7, "tempo": 135, "popularity": 85},
        {"name": "Workout 2", "energy": 0.92, "valence": 0.68, "tempo": 130, "popularity": 80}
    ]),
    ("Study Sounds", [
        {"name": "Focus 1", "energy": 0.5, "valence": 0.5, "tempo": 95, "popularity": 55},
        {"name": "Focus 2", "energy": 0.48, "valence": 0.52, "tempo": 92, "popularity": 52}
    ]),
    ("Pop Star", [
        {"name": "Hit Song 1", "energy": 0.7, "valence": 0.8, "tempo": 115, "popularity": 90},
        {"name": "Hit Song 2", "energy": 0.72, "valence": 0.82, "tempo": 118, "popularity": 88}
    ]),
    ("Indie Band", [
        {"name": "Alternative 1", "energy": 0.6, "valence": 0.65, "tempo": 100, "popularity": 45}
    ]),
    ("Electronic Artist", [
        {"name": "EDM Track 1", "energy": 0.88, "valence": 0.75, "tempo": 128, "popularity": 78}
    ]),
    ("Jazz Musician", [
        {"name": "Smooth Jazz", "energy": 0.4, "valence": 0.6, "tempo": 85, "popularity": 50}
    ])
]

track_id = 1
for artist_name, tracks in artists_tracks:
    for track_data in tracks:
        track = {
            "id": f"track{track_id}",
            "name": track_data["name"],
            "artists": [{"name": artist_name}],
            **{k: v for k, v in track_data.items() if k != "name"}
        }
        sample_tracks.append(track)
        track_id += 1

print(f"Created {len(sample_tracks)} sample tracks from {len(artists_tracks)} artists\n")

# Test 1: Rank tracks for happy mood
print("=" * 80)
print("TEST 1: Diversity Optimization for 10 tracks")
print("=" * 80)

mood_data = {
    "primary_mood": "happy",
    "energy_level": 7,
    "emotional_intensity": 7,
    "mood_tags": ["joyful", "upbeat"]
}

# First, rank the tracks
ranked_json = rank_tracks_by_relevance(
    json.dumps(sample_tracks),
    json.dumps(mood_data)
)

print("\n📊 Ranking complete")

# Then optimize diversity
result_json = optimize_diversity(ranked_json, desired_count=10)
result = json.loads(result_json)

playlist = result['playlist']
metrics = result['diversity_metrics']

print(f"\n✅ Optimized playlist with {len(playlist)} tracks\n")

print("Selected tracks:")
for i, track in enumerate(playlist, 1):
    print(f"{i:2d}. {track['name']:<20} by {track['artists'][0]['name']:<20} "
          f"[Energy: {track['energy']:.2f}, Tempo: {int(track['tempo'])} BPM]")

print(f"\n📈 Diversity Metrics:")
print(f"   Unique Artists: {metrics['unique_artists']}")
print(f"   Tempo Mean: {metrics['tempo_mean']} BPM")
print(f"   Tempo Std Dev: {metrics['tempo_std']} BPM")
print(f"   Energy Mean: {metrics['energy_mean']}")
print(f"   Energy Std Dev: {metrics['energy_std']}")
print(f"   Diversity Score: {metrics['diversity_score']:.2f}/100")

# Check artist constraint
artist_counts = {}
for track in playlist:
    artist = track['artists'][0]['name']
    artist_counts[artist] = artist_counts.get(artist, 0) + 1

print(f"\n🎤 Artist Distribution:")
for artist, count in sorted(artist_counts.items(), key=lambda x: -x[1]):
    print(f"   {artist}: {count} track(s)")

max_artist_count = max(artist_counts.values())
if max_artist_count <= 2:
    print(f"\n✅ Artist constraint satisfied (max {max_artist_count} per artist)")
else:
    print(f"\n⚠️  Artist constraint relaxed (max {max_artist_count} per artist)")

# Test 2: Larger playlist
print("\n\n" + "=" * 80)
print("TEST 2: Diversity Optimization for 15 tracks")
print("=" * 80)

result_json = optimize_diversity(ranked_json, desired_count=15)
result = json.loads(result_json)

playlist = result['playlist']
metrics = result['diversity_metrics']

print(f"\n✅ Optimized playlist with {len(playlist)} tracks")

print(f"\n📈 Diversity Metrics:")
print(f"   Unique Artists: {metrics['unique_artists']}")
print(f"   Tempo Std Dev: {metrics['tempo_std']} BPM (target: >20)")
print(f"   Energy Std Dev: {metrics['energy_std']} (target: >0.15)")
print(f"   Diversity Score: {metrics['diversity_score']:.2f}/100 (target: >70)")

# Check diversity targets
checks = []
checks.append(("Unique Artists ≥ 10", metrics['unique_artists'] >= 10))
checks.append(("Tempo Variety > 20 BPM", metrics['tempo_std'] > 20))
checks.append(("Energy Variety > 0.15", metrics['energy_std'] > 0.15))
checks.append(("Diversity Score > 70", metrics['diversity_score'] > 70))

print(f"\n✅ Diversity Quality Checks:")
for check, passed in checks:
    status = "✓" if passed else "✗"
    print(f"   {status} {check}")

all_passed = all(c[1] for c in checks)
if all_passed:
    print(f"\n🎉 All diversity targets met!")
else:
    print(f"\n⚠️  Some diversity targets not met (expected with limited sample data)")

print("\n" + "=" * 80)
print("✅ DIVERSITY OPTIMIZATION TESTS COMPLETE")
print("=" * 80)
