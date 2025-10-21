"""
Verification Script for Task 4.3: Audio Analysis Tools
Tests get_audio_features_batch functionality
"""

import json
import time
from app.services.spotify import SpotifyClient
from app.tools.spotify_tools import get_audio_features_batch

print("=" * 70)
print("TASK 4.3 VERIFICATION: Audio Analysis Tools")
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
print("Subtask 4.3.1: Audio Features Batch Tool")
print("=" * 70)

# Test 1: SpotifyClient has audio features methods
print("\n[Test 1] SpotifyClient Audio Features Methods")
spotify_client = SpotifyClient()
has_single_method = hasattr(spotify_client, 'get_audio_features')
has_batch_method = hasattr(spotify_client, 'get_audio_features_batch')
test("Audio features methods exist", 
     has_single_method and has_batch_method,
     f"get_audio_features: {has_single_method}, get_audio_features_batch: {has_batch_method}")

# Test 2: Get audio features for a single track
print("\n[Test 2] Single Track Audio Features")
try:
    # Search for a popular track first
    search_result = spotify_client.search("Blinding Lights The Weeknd", limit=1)
    if search_result.get("tracks", {}).get("items"):
        track = search_result["tracks"]["items"][0]
        track_id = track["id"]
        
        features = spotify_client.get_audio_features(track_id)
        
        has_features = features is not None
        has_energy = features.get("energy") is not None if has_features else False
        has_valence = features.get("valence") is not None if has_features else False
        has_tempo = features.get("tempo") is not None if has_features else False
        
        test("Single track features retrieved",
             has_features and has_energy and has_valence and has_tempo,
             f"Track: {track['name']}, Energy: {features.get('energy') if has_features else 'N/A'}, Valence: {features.get('valence') if has_features else 'N/A'}, Tempo: {features.get('tempo') if has_features else 'N/A'}")
        
        if has_features:
            print(f"  All features: {list(features.keys())}")
    else:
        test("Single track features retrieved", False, "Could not find test track")
except Exception as e:
    test("Single track features retrieved", False, f"Error: {e}")

# Test 3: Batch processing (10 tracks)
print("\n[Test 3] Batch Processing - 10 Tracks")
try:
    # Search for multiple tracks
    search_result = spotify_client.search("workout motivation", limit=10)
    tracks = search_result.get("tracks", {}).get("items", [])
    track_ids = [track["id"] for track in tracks]
    
    start_time = time.time()
    features_dict = spotify_client.get_audio_features_batch(track_ids)
    elapsed = time.time() - start_time
    
    success = len(features_dict) == len(track_ids)
    test("Batch 10 tracks",
         success,
         f"Retrieved {len(features_dict)}/{len(track_ids)} features in {elapsed:.2f}s")
    
    # Verify features structure
    if features_dict:
        sample_id = list(features_dict.keys())[0]
        sample_features = features_dict[sample_id]
        required_fields = ["energy", "valence", "danceability", "tempo", "acousticness", 
                          "instrumentalness", "liveness", "speechiness"]
        has_all_fields = all(field in sample_features for field in required_fields)
        test("All 8 core features present",
             has_all_fields,
             f"Sample track features: {list(sample_features.keys())[:8]}")
        
except Exception as e:
    test("Batch 10 tracks", False, f"Error: {e}")

# Test 4: Batch processing (150 tracks - multiple batches)
print("\n[Test 4] Batch Processing - 150 Tracks (Multi-batch)")
try:
    # Search for many tracks
    all_track_ids = []
    for query in ["workout", "chill", "party"]:
        search_result = spotify_client.search(query, limit=50)
        tracks = search_result.get("tracks", {}).get("items", [])
        all_track_ids.extend([track["id"] for track in tracks])
    
    # Take first 150
    test_track_ids = all_track_ids[:150]
    
    start_time = time.time()
    features_dict = spotify_client.get_audio_features_batch(test_track_ids)
    elapsed = time.time() - start_time
    
    # Should process in 2 batches (100 + 50)
    success = len(features_dict) >= 145  # Allow for a few missing features
    test("Batch 150 tracks (2 batches)",
         success,
         f"Retrieved {len(features_dict)}/{len(test_track_ids)} features in {elapsed:.2f}s (~{elapsed/2:.2f}s per batch)")
    
except Exception as e:
    test("Batch 150 tracks", False, f"Error: {e}")

# Test 5: LangChain Tool wrapper
print("\n[Test 5] LangChain Tool Wrapper")
try:
    # Get some track IDs
    search_result = spotify_client.search("happy music", limit=5)
    tracks = search_result.get("tracks", {}).get("items", [])
    track_ids = [track["id"] for track in tracks]
    
    # Test the tool function
    track_ids_json = json.dumps(track_ids)
    result_json = get_audio_features_batch(track_ids_json)
    result = json.loads(result_json)
    
    success = result.get("success", False)
    features_retrieved = result.get("features_retrieved", 0)
    
    test("Tool wrapper works",
         success and features_retrieved == len(track_ids),
         f"Retrieved features for {features_retrieved}/{len(track_ids)} tracks via tool")
    
    # Check result structure
    has_audio_features = "audio_features" in result
    test("Tool returns proper structure",
         has_audio_features and isinstance(result["audio_features"], list),
         f"Result keys: {list(result.keys())}")
    
except Exception as e:
    test("Tool wrapper works", False, f"Error: {e}")

# Test 6: Features in correct ranges
print("\n[Test 6] Feature Value Ranges")
try:
    # Get features for a few tracks
    search_result = spotify_client.search("test track", limit=3)
    tracks = search_result.get("tracks", {}).get("items", [])
    track_ids = [track["id"] for track in tracks]
    
    features_dict = spotify_client.get_audio_features_batch(track_ids)
    
    if features_dict:
        sample_features = list(features_dict.values())[0]
        
        # Check 0-1 ranges
        energy_valid = 0 <= sample_features.get("energy", -1) <= 1
        valence_valid = 0 <= sample_features.get("valence", -1) <= 1
        danceability_valid = 0 <= sample_features.get("danceability", -1) <= 1
        acousticness_valid = 0 <= sample_features.get("acousticness", -1) <= 1
        
        # Check tempo range (reasonable BPM)
        tempo_valid = 40 <= sample_features.get("tempo", 0) <= 250
        
        all_valid = energy_valid and valence_valid and danceability_valid and acousticness_valid and tempo_valid
        
        test("Feature ranges valid",
             all_valid,
             f"Energy: {sample_features.get('energy')}, Valence: {sample_features.get('valence')}, Tempo: {sample_features.get('tempo')} BPM")
    else:
        test("Feature ranges valid", False, "No features retrieved")
        
except Exception as e:
    test("Feature ranges valid", False, f"Error: {e}")

# Test 7: Handle missing features
print("\n[Test 7] Error Handling - Missing Features")
try:
    # Test with invalid track ID
    invalid_ids = ["invalid123", "fake456"]
    features_dict = spotify_client.get_audio_features_batch(invalid_ids)
    
    # Should return empty dict or handle gracefully
    handled = isinstance(features_dict, dict) and len(features_dict) == 0
    
    test("Invalid track IDs handled",
         handled,
         f"Returned empty dict for invalid IDs: {features_dict}")
    
except Exception as e:
    # Should not raise exception
    test("Invalid track IDs handled", False, f"Raised exception: {e}")

# Test 8: Empty input handling
print("\n[Test 8] Error Handling - Empty Input")
try:
    features_dict = spotify_client.get_audio_features_batch([])
    
    # Should return empty dict
    handled = isinstance(features_dict, dict) and len(features_dict) == 0
    
    test("Empty track list handled",
         handled,
         "Returned empty dict for empty input")
    
except Exception as e:
    test("Empty track list handled", False, f"Error: {e}")

# Test 9: Performance check
print("\n[Test 9] Performance Metrics")
try:
    # Time a batch of 50 tracks
    search_result = spotify_client.search("popular music", limit=50)
    tracks = search_result.get("tracks", {}).get("items", [])
    track_ids = [track["id"] for track in tracks]
    
    start_time = time.time()
    features_dict = spotify_client.get_audio_features_batch(track_ids)
    elapsed = time.time() - start_time
    
    # Should be reasonably fast (< 3 seconds for 50 tracks)
    is_fast = elapsed < 3.0
    avg_per_track = elapsed / len(track_ids) if track_ids else 0
    
    test("Performance acceptable",
         is_fast,
         f"50 tracks in {elapsed:.2f}s ({avg_per_track:.3f}s per track)")
    
except Exception as e:
    test("Performance acceptable", False, f"Error: {e}")

print("\n" + "=" * 70)
print("VERIFICATION SUMMARY - TASK 4.3")
print("=" * 70)
print(f"Tests passed: {tests_passed}/{total_tests} ({100*tests_passed//total_tests}%)")

if tests_passed == total_tests:
    print("\n🎉 TASK 4.3 COMPLETE!")
    print("\n✅ Features Working:")
    print("  ✅ get_audio_features() - Single track")
    print("  ✅ get_audio_features_batch() - Multiple tracks")
    print("  ✅ Automatic batching (handles >100 tracks)")
    print("  ✅ LangChain tool wrapper")
    print("  ✅ All 8 audio features retrieved")
    print("  ✅ Feature ranges validated")
    print("  ✅ Error handling")
    print("  ✅ Performance optimized")
    print("\n📋 Ready for Task 4.4: Track Filtering")
else:
    print(f"\n⚠️  {total_tests - tests_passed} test(s) failed")
    print("Review errors above and fix issues")
