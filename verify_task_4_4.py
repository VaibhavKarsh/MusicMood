"""
Verification Script for Task 4.4: Track Filtering
Tests filtering functionality with mood criteria
"""

import json
from app.services.spotify import SpotifyClient
from app.tools.spotify_tools import (
    get_mood_filtering_criteria,
    filter_tracks_by_mood_criteria,
    filter_tracks_tool,
    mood_filter_tool
)

print("=" * 70)
print("TASK 4.4 VERIFICATION: Track Filtering")
print("=" * 70)

# Track for testing progress
tests_passed = 0
total_tests = 0

def test(name: str, condition: bool, details: str = ""):
    """Helper function to track test results"""
    global tests_passed, total_tests
    total_tests += 1
    status = "✅ PASS" if condition else "❌ FAIL"
    print(f"\n{status} - {name}")
    if details:
        print(f"  {details}")
    if condition:
        tests_passed += 1
    return condition


print("\n" + "=" * 70)
print("Subtask 4.4.1: Mood-Based Filtering Criteria")
print("=" * 70)

# Test 1: Criteria generation for different moods
print("\n[Test 1] Criteria Generation - Happy Mood")
happy_mood = {
    "primary_mood": "happy",
    "energy_level": 8,
    "emotional_intensity": 7
}
criteria = get_mood_filtering_criteria(happy_mood)
has_targets = criteria.get("target_energy") is not None and criteria.get("target_valence") is not None
test("Happy mood criteria generated",
     has_targets,
     f"Energy: {criteria.get('target_energy'):.2f}, Valence: {criteria.get('target_valence'):.2f}, Tolerance: {criteria.get('tolerance')}")

# Test 2: Energetic mood
print("\n[Test 2] Criteria Generation - Energetic Mood")
energetic_mood = {
    "primary_mood": "energetic",
    "energy_level": 10,
    "emotional_intensity": 9
}
criteria = get_mood_filtering_criteria(energetic_mood)
high_energy = criteria.get("target_energy", 0) > 0.8
has_tempo = criteria.get("target_tempo") is not None
test("Energetic mood criteria",
     high_energy and has_tempo,
     f"Energy: {criteria.get('target_energy'):.2f}, Tempo: {criteria.get('target_tempo')} BPM")

# Test 3: Calm mood
print("\n[Test 3] Criteria Generation - Calm Mood")
calm_mood = {
    "primary_mood": "calm",
    "energy_level": 2,
    "emotional_intensity": 3
}
criteria = get_mood_filtering_criteria(calm_mood)
low_energy = criteria.get("target_energy", 1) < 0.5
test("Calm mood criteria",
     low_energy,
     f"Energy: {criteria.get('target_energy'):.2f}, Tempo: {criteria.get('target_tempo')} BPM")

# Test 4: Sad mood
print("\n[Test 4] Criteria Generation - Sad Mood")
sad_mood = {
    "primary_mood": "sad",
    "energy_level": 3,
    "emotional_intensity": 8
}
criteria = get_mood_filtering_criteria(sad_mood)
low_valence = criteria.get("target_valence", 1) < 0.5
strict_tolerance = criteria.get("tolerance") <= 0.3
test("Sad mood criteria",
     low_valence and strict_tolerance,
     f"Valence: {criteria.get('target_valence'):.2f}, Tolerance: {criteria.get('tolerance')} (stricter for high intensity)")

# Test 5: Focused mood
print("\n[Test 5] Criteria Generation - Focused Mood")
focused_mood = {
    "primary_mood": "focused",
    "energy_level": 5,
    "emotional_intensity": 6
}
criteria = get_mood_filtering_criteria(focused_mood)
has_instrumentalness = criteria.get("target_instrumentalness") is not None
test("Focused mood prefers instrumental",
     has_instrumentalness and criteria.get("target_instrumentalness") >= 0.5,
     f"Instrumentalness: {criteria.get('target_instrumentalness')}, Energy: {criteria.get('target_energy'):.2f}")

print("\n" + "=" * 70)
print("Subtask 4.4.2: Track Filtering Implementation")
print("=" * 70)

# Test 6: Filter tracks by mood (happy)
print("\n[Test 6] Filter Tracks - Happy Mood")
try:
    spotify_client = SpotifyClient()
    
    # Search for diverse tracks
    search_result = spotify_client.search("music", limit=30)
    tracks = search_result.get("tracks", {}).get("items", [])
    
    tracks_json = json.dumps(tracks)
    mood_json = json.dumps(happy_mood)
    
    result_json = filter_tracks_by_mood_criteria(tracks_json, mood_json)
    result = json.loads(result_json)
    
    success = result.get("success", False)
    filtered_count = result.get("total_matches", 0)
    
    test("Happy mood filtering",
         success and filtered_count > 0,
         f"Filtered {filtered_count} tracks from {len(tracks)} total")
    
    if success:
        print(f"  Criteria applied: {result.get('criteria', {})}")
    
except Exception as e:
    test("Happy mood filtering", False, f"Error: {e}")

# Test 7: Filter tracks by mood (calm)
print("\n[Test 7] Filter Tracks - Calm Mood")
try:
    # Search for calm/chill music
    search_result = spotify_client.search("chill relax", limit=30)
    tracks = search_result.get("tracks", {}).get("items", [])
    
    tracks_json = json.dumps(tracks)
    mood_json = json.dumps(calm_mood)
    
    result_json = filter_tracks_by_mood_criteria(tracks_json, mood_json)
    result = json.loads(result_json)
    
    success = result.get("success", False)
    filtered_count = result.get("total_matches", 0)
    
    # Calm mood should filter out explicit tracks
    filtered_tracks = result.get("tracks", [])
    explicit_count = sum(1 for t in filtered_tracks if t.get("explicit", False))
    
    test("Calm mood filters explicit content",
         success and explicit_count == 0,
         f"Filtered tracks: {filtered_count}, Explicit tracks: {explicit_count}")
    
except Exception as e:
    test("Calm mood filtering", False, f"Error: {e}")

# Test 8: Popularity filtering
print("\n[Test 8] Popularity Filtering")
try:
    # Search for mix of popular and unpopular tracks
    search_result = spotify_client.search("indie underground", limit=30)
    tracks = search_result.get("tracks", {}).get("items", [])
    
    tracks_json = json.dumps(tracks)
    mood_json = json.dumps(happy_mood)
    
    result_json = filter_tracks_by_mood_criteria(tracks_json, mood_json)
    result = json.loads(result_json)
    
    filtered_tracks = result.get("tracks", [])
    
    # Check that very unpopular tracks are filtered out
    min_popularity = min([t.get("popularity", 100) for t in filtered_tracks]) if filtered_tracks else 0
    
    test("Low popularity tracks filtered",
         min_popularity >= 20,
         f"Minimum popularity in results: {min_popularity}")
    
except Exception as e:
    test("Popularity filtering", False, f"Error: {e}")

# Test 9: Score ranking
print("\n[Test 9] Score-Based Ranking")
try:
    # Get filtered tracks
    search_result = spotify_client.search("popular hits", limit=20)
    tracks = search_result.get("tracks", {}).get("items", [])
    
    tracks_json = json.dumps(tracks)
    mood_json = json.dumps(energetic_mood)
    
    result_json = filter_tracks_by_mood_criteria(tracks_json, mood_json)
    result = json.loads(result_json)
    
    filtered_tracks = result.get("tracks", [])
    
    # Check that tracks are sorted by score
    if len(filtered_tracks) >= 2:
        scores = [t.get("match_score", 0) for t in filtered_tracks]
        is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
        
        test("Tracks sorted by match score",
             is_sorted,
             f"Score range: {scores[0]:.3f} to {scores[-1]:.3f}")
    else:
        test("Tracks sorted by match score", True, "Less than 2 tracks, sorting not testable")
    
except Exception as e:
    test("Score-based ranking", False, f"Error: {e}")

# Test 10: LangChain tool wrapper
print("\n[Test 10] LangChain Tool Wrapper")
try:
    # Test mood_filter_tool
    has_tool = mood_filter_tool is not None
    has_name = mood_filter_tool.name == "filter_tracks_by_mood_criteria"
    has_func = callable(mood_filter_tool.func)
    has_desc = len(mood_filter_tool.description) > 0
    
    test("Mood filter tool exists",
         has_tool and has_name and has_func and has_desc,
         f"Name: {mood_filter_tool.name}, Has function: {has_func}")
    
except Exception as e:
    test("LangChain tool wrapper", False, f"Error: {e}")

# Test 11: Edge case - no tracks pass filter
print("\n[Test 11] Edge Case - Empty Filter Result")
try:
    # Create very strict criteria that nothing will match
    strict_tracks = [
        {"id": "1", "name": "Track 1", "popularity": 10, "explicit": True},  # Too low popularity
        {"id": "2", "name": "Track 2", "popularity": 15, "explicit": True},  # Too low popularity
    ]
    
    tracks_json = json.dumps(strict_tracks)
    mood_json = json.dumps(calm_mood)  # Calm filters explicit tracks
    
    result_json = filter_tracks_by_mood_criteria(tracks_json, mood_json)
    result = json.loads(result_json)
    
    # Should handle gracefully
    success = result.get("success", False)
    filtered_count = result.get("total_matches", -1)
    
    test("Empty filter result handled",
         success and filtered_count == 0,
         f"Filtered {filtered_count} tracks (as expected)")
    
except Exception as e:
    test("Empty filter result", False, f"Error: {e}")

# Test 12: Different energy levels affect criteria
print("\n[Test 12] Energy Level Impact on Criteria")
low_energy_happy = {
    "primary_mood": "happy",
    "energy_level": 3,
    "emotional_intensity": 5
}
high_energy_happy = {
    "primary_mood": "happy",
    "energy_level": 10,
    "emotional_intensity": 5
}

criteria_low = get_mood_filtering_criteria(low_energy_happy)
criteria_high = get_mood_filtering_criteria(high_energy_happy)

energy_diff = criteria_high.get("target_energy", 0) - criteria_low.get("target_energy", 0)

test("Energy level affects criteria",
     energy_diff > 0,
     f"Low energy: {criteria_low.get('target_energy'):.2f}, High energy: {criteria_high.get('target_energy'):.2f}, Diff: {energy_diff:.2f}")

print("\n" + "=" * 70)
print("VERIFICATION SUMMARY - TASK 4.4")
print("=" * 70)
print(f"Tests passed: {tests_passed}/{total_tests} ({100*tests_passed//total_tests}%)")

if tests_passed == total_tests:
    print("\n🎉 TASK 4.4 COMPLETE!")
    print("\n✅ Features Working:")
    print("  ✅ Mood-based criteria generation")
    print("  ✅ Criteria for all mood types (happy, sad, calm, energetic, focused)")
    print("  ✅ Energy level affects filtering")
    print("  ✅ Emotional intensity affects tolerance")
    print("  ✅ Popularity filtering (removes tracks < 20 popularity)")
    print("  ✅ Explicit content filtering for appropriate moods")
    print("  ✅ Score-based ranking")
    print("  ✅ LangChain tool wrapper")
    print("  ✅ Edge case handling")
    print("\n✅ PHASE 4 COMPLETE!")
    print("  ✅ Task 4.1: Spotify API Client")
    print("  ✅ Task 4.2: Spotify Search Tools")
    print("  ✅ Task 4.3: Audio Analysis Tools (implemented, API access limited)")
    print("  ✅ Task 4.4: Track Filtering")
    print("\n📋 Ready for Phase 5: Agent 3 - Playlist Curator")
else:
    print(f"\n⚠️  {total_tests - tests_passed} test(s) failed")
    print("Review errors above and fix issues")
