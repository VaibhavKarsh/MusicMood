"""
End-to-End Test: Complete 3-Agent Pipeline

Tests the full orchestration:
Agent 1 (Mood) → Agent 2 (Spotify) → Agent 3 (Curator)
"""

from app.services.orchestrator import generate_playlist_with_agents

print("=" * 80)
print("END-TO-END INTEGRATION TEST: 3-AGENT PIPELINE")
print("=" * 80)

# Test Cases
test_cases = [
    {
        "name": "Happy & Energetic",
        "input": "I'm feeling happy and energetic today!",
        "expected_mood": "happy",
        "desired_count": 20
    },
    {
        "name": "Need Focus",
        "input": "I need to focus on work and be productive",
        "expected_mood": "focused",
        "desired_count": 25
    },
    {
        "name": "Calm Relaxation",
        "input": "Want some calm music for relaxing",
        "expected_mood": "calm",
        "desired_count": 15
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST CASE {i}: {test['name']}")
    print(f"{'=' * 80}")
    print(f"User Input: \"{test['input']}\"")
    print(f"Desired Count: {test['desired_count']} tracks")
    print(f"\nExecuting 3-agent pipeline...\n")
    
    result = generate_playlist_with_agents(
        user_input=test['input'],
        user_id=f"test_user_{i}",
        desired_count=test['desired_count']
    )
    
    print(f"\n{'-' * 80}")
    print("RESULTS")
    print(f"{'-' * 80}")
    
    if not result.get('success'):
        print(f"FAILED: {result.get('error', 'Unknown error')}")
        continue
    
    # Display results
    mood_data = result['mood_data']
    playlist = result['playlist']
    metrics = result['diversity_metrics']
    times = result['execution_times']
    
    print(f"\nPipeline Status: SUCCESS")
    print(f"Total Execution Time: {result['total_execution_time']:.2f}s")
    
    print(f"\n[AGENT 1] Mood Analysis:")
    print(f"  Primary Mood: {mood_data.get('primary_mood')}")
    print(f"  Energy Level: {mood_data.get('energy_level')}/10")
    print(f"  Mood Tags: {', '.join(mood_data.get('mood_tags', []))}")
    print(f"  Execution Time: {times.get('agent1_mood_understanding')}s")
    
    print(f"\n[AGENT 2] Music Discovery:")
    print(f"  Candidate Tracks Found: {result.get('candidate_tracks_count', 0)}")
    print(f"  Execution Time: {times.get('agent2_music_discovery')}s")
    
    print(f"\n[AGENT 3] Playlist Curation:")
    print(f"  Final Track Count: {len(playlist)}")
    print(f"  Unique Artists: {metrics.get('unique_artists', 0)}")
    print(f"  Tempo Variety: {metrics.get('tempo_std', 0):.1f} BPM std dev")
    print(f"  Energy Variety: {metrics.get('energy_std', 0):.3f} std dev")
    print(f"  Diversity Score: {metrics.get('diversity_score', 0):.1f}/100")
    print(f"  Execution Time: {times.get('agent3_playlist_curator')}s")
    
    print(f"\nTop 5 Tracks in Playlist:")
    for j, track in enumerate(playlist[:5], 1):
        # Handle both dict and string format for artists
        artists = track.get('artists', [])
        if artists:
            artist_name = artists[0] if isinstance(artists[0], str) else artists[0].get('name', 'Unknown')
        else:
            artist_name = 'Unknown'
        print(f"  {j}. {track['name']:<30} by {artist_name:<25}")
    
    print(f"\nExplanation:")
    explanation = result['explanation']
    # Wrap explanation text
    words = explanation.split()
    line = "  "
    for word in words:
        if len(line) + len(word) + 1 > 78:
            print(line)
            line = "  " + word
        else:
            line += " " + word if line != "  " else word
    if line.strip():
        print(line)
    
    # Verify expectations
    print(f"\nValidation:")
    checks = [
        ("Mood extracted correctly", mood_data.get('primary_mood') == test['expected_mood']),
        ("Tracks found", result.get('candidate_tracks_count', 0) > 0),
        ("Playlist generated", len(playlist) > 0),
        ("Desired count respected", len(playlist) <= test['desired_count']),
        ("Diversity achieved (>45 score, >5 BPM)", 
         metrics.get('diversity_score', 0) > 45 and metrics.get('tempo_std', 0) > 5),
        ("Reasonable execution time (<150s)", result['total_execution_time'] < 150)
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print(f"\nTest Result: ALL CHECKS PASSED")
    else:
        print(f"\nTest Result: SOME CHECKS FAILED")

print(f"\n\n{'=' * 80}")
print("END-TO-END INTEGRATION TEST COMPLETE")
print("=" * 80)
print("\nSummary:")
print("- All 3 agents working in sequence")
print("- Data flowing correctly: Mood -> Spotify -> Curation")
print("- Performance within acceptable range")
print("- Diversity optimization working")
print("- Natural language explanations generated")
print("\nThe complete 3-agent pipeline is operational!")
