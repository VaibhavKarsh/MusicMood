"""
Quick validation test for the complete 3-agent system
"""

from app.services.orchestrator import generate_playlist_with_agents

print("=" * 80)
print("FINAL VALIDATION TEST")
print("=" * 80)

result = generate_playlist_with_agents('Give me upbeat workout music', 'test_user', 10)

print("\n✅ RESULTS:")
print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")

if result.get('premium_feature_required'):
    print("\n" + "=" * 80)
    print("⭐ PREMIUM FEATURE REQUIRED")
    print("=" * 80)
    print(f"\n{result.get('premium_feature_message', 'Premium features needed')}")
    print(f"\nWhat's missing: Audio features API (tempo, energy, valence, danceability)")
    print(f"Why it's needed: Advanced mood-based playlist curation and optimization")
    print(f"How to unlock: Upgrade to Spotify Premium API access")
else:
    print(f"Playlist: {len(result['playlist'])} tracks")
    print(f"Unique Artists: {result['diversity_metrics'].get('unique_artists', 0)}")
    print(f"Diversity Score: {result['diversity_metrics'].get('diversity_score', 0):.1f}/100")
    print(f"Tempo Variety: {result['diversity_metrics'].get('tempo_std', 0):.1f} BPM std dev")
    print(f"Energy Variety: {result['diversity_metrics'].get('energy_std', 0):.3f} std dev")
    print(f"\nExplanation:\n  {result['explanation']}")

print(f"\nTotal Time: {result['total_execution_time']:.2f}s")

print("\n" + "=" * 80)
if result['success'] and len(result.get('playlist', [])) >= 8:
    print("✅ ALL SYSTEMS OPERATIONAL - FULL FEATURE ACCESS")
elif result.get('premium_feature_required'):
    print("⚠️  PREMIUM FEATURE REQUIRED - System working, upgrade needed for advanced features")
else:
    print("❌ SYSTEM CHECK FAILED")
print("=" * 80)
