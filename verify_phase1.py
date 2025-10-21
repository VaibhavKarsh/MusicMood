"""
Phase 1 Complete Verification Script
Checks all services and configurations before moving to Phase 2
"""
import sys
import requests
import redis
import psycopg2
from app.config.settings import settings


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def check_ollama():
    """Verify Ollama service is running"""
    print_section("Task 1.1: Ollama Local LLM Setup")
    
    try:
        # Check if Ollama is running
        response = requests.get(f"{settings.OLLAMA_BASE_URL}", timeout=5)
        print("✓ Ollama service is running on", settings.OLLAMA_BASE_URL)
        
        # Check if Mistral model is available
        try:
            response = requests.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": "Hello",
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                print(f"✓ {settings.OLLAMA_MODEL} model is loaded and responding")
                data = response.json()
                if 'response' in data:
                    print(f"✓ Model generated response: {data['response'][:50]}...")
                return True
            else:
                print(f"✗ Model response error: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Mistral model test failed: {str(e)}")
            print(f"  Run: ollama pull {settings.OLLAMA_MODEL}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to Ollama at {settings.OLLAMA_BASE_URL}")
        print("  Run: ollama serve")
        return False
    except Exception as e:
        print(f"✗ Ollama check failed: {str(e)}")
        return False


def check_postgresql():
    """Verify PostgreSQL database connection"""
    print_section("Task 1.2: PostgreSQL Database Setup")
    
    try:
        # Parse connection string
        conn = psycopg2.connect(settings.DATABASE_URL)
        print("✓ PostgreSQL connection successful")
        
        # Test database operations
        cursor = conn.cursor()
        
        # Check database name
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"✓ Connected to database: {db_name}")
        
        # Check user
        cursor.execute("SELECT current_user;")
        user_name = cursor.fetchone()[0]
        print(f"✓ Connected as user: {user_name}")
        
        # Test table creation (and cleanup)
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS phase1_test (id SERIAL PRIMARY KEY, test VARCHAR(50));")
            cursor.execute("INSERT INTO phase1_test (test) VALUES ('verification');")
            cursor.execute("SELECT * FROM phase1_test;")
            result = cursor.fetchone()
            cursor.execute("DROP TABLE phase1_test;")
            conn.commit()
            print("✓ Database CRUD operations successful")
        except Exception as e:
            print(f"✗ Database operations failed: {str(e)}")
            conn.rollback()
            cursor.close()
            conn.close()
            return False
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"✗ PostgreSQL connection failed: {str(e)}")
        print("  Check DATABASE_URL in .env")
        print("  Ensure PostgreSQL service is running")
        return False
    except Exception as e:
        print(f"✗ PostgreSQL check failed: {str(e)}")
        return False


def check_redis():
    """Verify Redis cache connection"""
    print_section("Task 1.3: Redis Cache Setup")
    
    try:
        # Connect to Redis
        r = redis.from_url(
            settings.REDIS_URL,
            decode_responses=settings.REDIS_DECODE_RESPONSES
        )
        
        # Test connection
        r.ping()
        print("✓ Redis connection successful")
        print(f"✓ Connected to: {settings.REDIS_URL}")
        
        # Test SET operation
        r.set("phase1_test", "verification")
        print("✓ Redis SET operation successful")
        
        # Test GET operation
        value = r.get("phase1_test")
        if value == "verification":
            print("✓ Redis GET operation successful")
        
        # Test expiration
        r.setex("phase1_temp", 5, "temporary")
        print("✓ Redis SETEX operation successful")
        
        # Test list operations
        r.lpush("phase1_list", "item1", "item2")
        items = r.lrange("phase1_list", 0, -1)
        if len(items) == 2:
            print("✓ Redis LIST operations successful")
        
        # Cleanup
        r.delete("phase1_test", "phase1_temp", "phase1_list")
        print("✓ Redis cleanup successful")
        
        return True
        
    except redis.ConnectionError:
        print(f"✗ Cannot connect to Redis at {settings.REDIS_URL}")
        print("  Ensure Redis service is running")
        print("  Docker: docker run -d -p 6379:6379 redis:7-alpine")
        return False
    except Exception as e:
        print(f"✗ Redis check failed: {str(e)}")
        return False


def check_api_credentials():
    """Verify API credentials are set"""
    print_section("Task 1.4: API Keys & Credentials Setup")
    
    all_ok = True
    
    # Check Spotify credentials
    if settings.SPOTIFY_CLIENT_ID and len(settings.SPOTIFY_CLIENT_ID) > 10:
        print("✓ Spotify Client ID is set")
    else:
        print("✗ Spotify Client ID is missing or invalid")
        print("  Get credentials from: https://developer.spotify.com/dashboard")
        all_ok = False
    
    if settings.SPOTIFY_CLIENT_SECRET and len(settings.SPOTIFY_CLIENT_SECRET) > 10:
        print("✓ Spotify Client Secret is set")
    else:
        print("✗ Spotify Client Secret is missing or invalid")
        all_ok = False
    
    # Test Spotify credentials (optional - requires network)
    if settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET:
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyClientCredentials
            
            auth_manager = SpotifyClientCredentials(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET
            )
            sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Try a simple search
            results = sp.search(q='test', limit=1, type='track')
            if results:
                print("✓ Spotify credentials validated successfully")
        except Exception as e:
            print(f"⚠ Spotify credentials could not be validated: {str(e)}")
            print("  Credentials are set but may be invalid")
    
    # Check OpenWeatherMap API key
    if settings.OPENWEATHER_API_KEY and len(settings.OPENWEATHER_API_KEY) > 10:
        print("✓ OpenWeatherMap API key is set")
    else:
        print("⚠ OpenWeatherMap API key is missing")
        print("  Get key from: https://openweathermap.org/api")
        print("  (Non-critical for initial development)")
    
    return all_ok


def check_environment():
    """Check environment configuration"""
    print_section("Environment Configuration")
    
    print(f"✓ App Name: {settings.APP_NAME}")
    print(f"✓ Version: {settings.APP_VERSION}")
    print(f"✓ Environment: {settings.ENVIRONMENT}")
    print(f"✓ Debug Mode: {settings.DEBUG}")
    print(f"✓ Ollama Model: {settings.OLLAMA_MODEL}")
    print(f"✓ Cache TTL configured:")
    print(f"  - Mood: {settings.MOOD_CACHE_TTL}s")
    print(f"  - Search: {settings.SEARCH_CACHE_TTL}s")
    print(f"  - Features: {settings.FEATURES_CACHE_TTL}s")
    
    return True


def main():
    """Run all Phase 1 verifications"""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + "  PHASE 1 COMPLETE VERIFICATION".center(68) + "#")
    print("#" + "  Local Environment Setup & Infrastructure".center(68) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)
    
    results = {
        "Environment": check_environment(),
        "Ollama": check_ollama(),
        "PostgreSQL": check_postgresql(),
        "Redis": check_redis(),
        "API Credentials": check_api_credentials(),
    }
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for service, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service:20} - {'PASS' if status else 'FAIL'}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} checks passed")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 " + "=" * 66 + " 🎉")
        print("🎉 " + "PHASE 1 COMPLETE!".center(66) + " 🎉")
        print("🎉 " + "All services configured and verified.".center(66) + " 🎉")
        print("🎉 " + "Ready to proceed to Phase 2: Core Backend Architecture".center(66) + " 🎉")
        print("🎉 " + "=" * 66 + " 🎉\n")
        return 0
    else:
        print("\n❌ " + "=" * 66 + " ❌")
        print("❌ " + "PHASE 1 INCOMPLETE".center(66) + " ❌")
        print("❌ " + f"{total - passed} check(s) failed. Please fix issues above.".center(66) + " ❌")
        print("❌ " + "See SETUP_GUIDE.md for detailed instructions.".center(66) + " ❌")
        print("❌ " + "=" * 66 + " ❌\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
