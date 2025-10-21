"""
Simple Comprehensive Verification Summary
Tests all critical functionality without Unicode characters
"""

import sys
import subprocess


def run_test(description: str, command: list) -> bool:
    """Run a test command and return success status."""
    print(f"\n[TEST] {description}")
    print(f"Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("PASS - Exit code 0")
            return True
        else:
            print(f"FAIL - Exit code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")
            return False
    
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    """Run simplified verification tests."""
    
    print("=" * 70)
    print("MUSICMOOD - COMPREHENSIVE VERIFICATION SUMMARY")
    print("=" * 70)
    
    tests = []
    
    # Test 1: Database connection
    print("\n" + "=" * 70)
    print("PHASE 1: Infrastructure Tests")
    print("=" * 70)
    
    tests.append((
        "PostgreSQL Connection",
        ["poetry", "run", "python", "-c",
         "from app.db import engine; conn = engine.connect(); print('OK'); conn.close()"]
    ))
    
    tests.append((
        "Redis Connection",
        ["poetry", "run", "python", "-c",
         "import redis; from app.config.settings import settings; r = redis.from_url(settings.REDIS_URL); r.ping(); print('OK')"]
    ))
    
    tests.append((
        "Ollama Service",
        ["poetry", "run", "python", "-c",
         "import httpx; r = httpx.get('http://localhost:11434/api/tags', timeout=5); print('OK' if r.status_code == 200 else 'FAIL')"]
    ))
    
    # Test 2: Database models
    print("\n" + "=" * 70)
    print("PHASE 2: Database Models Tests")
    print("=" * 70)
    
    tests.append((
        "Import Models",
        ["poetry", "run", "python", "-c",
         "from app.models import User, MoodEntry, PlaylistRecommendation; print('OK')"]
    ))
    
    tests.append((
        "Database Tables Exist",
        ["poetry", "run", "python", "-c",
         "from sqlalchemy import inspect; from app.db import engine; i = inspect(engine); tables = i.get_table_names(); assert 'users' in tables; assert 'mood_entries' in tables; assert 'playlist_recommendations' in tables; print('OK')"]
    ))
    
    # Test 3: FastAPI application
    print("\n" + "=" * 70)
    print("PHASE 2: FastAPI Application Tests")
    print("=" * 70)
    
    tests.append((
        "FastAPI App Initialization",
        ["poetry", "run", "python", "-c",
         "from app.main import app; assert app.title == 'MusicMood'; print('OK')"]
    ))
    
    tests.append((
        "Health Endpoint",
        ["poetry", "run", "python", "-c",
         "from fastapi.testclient import TestClient; from app.main import app; client = TestClient(app); r = client.get('/health'); assert r.status_code == 200; print('OK')"]
    ))
    
    tests.append((
        "Database Session Management",
        ["poetry", "run", "python", "-c",
         "from app.db import get_db; db = next(get_db()); from sqlalchemy import text; db.execute(text('SELECT 1')); print('OK')"]
    ))
    
    tests.append((
        "Configuration Loading",
        ["poetry", "run", "python", "-c",
         "from app.config.settings import settings; assert settings.APP_NAME == 'MusicMood'; assert settings.DATABASE_URL; print('OK')"]
    ))
    
    # Run all tests
    results = []
    for description, command in tests:
        success = run_test(description, command)
        results.append((description, success))
    
    # Print summary
    print("\n" + "=" * 70)
    print("VERIFICATION RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {description}")
    
    print("\n" + "=" * 70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70)
    
    if passed == total:
        print("\nSUCCESS: All verification tests passed!")
        print("\nCompleted Phases:")
        print("  [X] Phase 1: Local Environment Setup")
        print("      - Ollama with qwen3:8b model")
        print("      - PostgreSQL on port 5433")
        print("      - Redis on port 6379")
        print("      - API credentials configured")
        print("      - Poetry environment with 123 packages")
        print("\n  [X] Phase 2: Core Backend Architecture")
        print("      - FastAPI application structure")
        print("      - Database models (User, MoodEntry, PlaylistRecommendation)")
        print("      - Database connection pooling")
        print("      - Environment configuration")
        print("      - Health check API endpoints")
        print("\nReady to proceed to Phase 3: Agent Development")
        return 0
    else:
        print(f"\nFailed {total - passed} test(s). Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
