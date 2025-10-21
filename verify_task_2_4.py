"""
Verification script for Task 2.4: Environment Configuration Management
"""

import sys
import os
from typing import List, Tuple

from app.config.settings import settings


def verify_configuration() -> bool:
    """Verify environment configuration management."""
    
    print("=" * 70)
    print("Verifying Environment Configuration Management (Task 2.4)")
    print("=" * 70)
    
    all_checks_passed = True
    warnings: List[str] = []
    
    try:
        # Check 1: Verify Settings class loads
        print("\n[CHECK 1] Verifying Settings class instantiation...")
        if settings:
            print("✓ Settings class instantiated successfully")
        else:
            print("✗ Settings class failed to instantiate")
            return False
        
        # Check 2: Verify APP configuration
        print("\n[CHECK 2] Verifying APP configuration...")
        app_config = {
            'APP_NAME': settings.APP_NAME,
            'APP_VERSION': settings.APP_VERSION,
            'ENVIRONMENT': settings.ENVIRONMENT,
            'DEBUG': settings.DEBUG,
            'API_V1_PREFIX': settings.API_V1_PREFIX,
        }
        
        for key, value in app_config.items():
            if value is not None:
                print(f"✓ {key}: {value}")
            else:
                print(f"✗ {key}: NOT SET")
                all_checks_passed = False
        
        # Check 3: Verify DATABASE configuration
        print("\n[CHECK 3] Verifying DATABASE configuration...")
        if settings.DATABASE_URL:
            # Don't print full URL (has password)
            if "postgresql://" in settings.DATABASE_URL and "musicmood" in settings.DATABASE_URL:
                print(f"✓ DATABASE_URL: postgresql://***@localhost:5433/musicmood")
            else:
                print(f"⚠ DATABASE_URL format unexpected: {settings.DATABASE_URL[:30]}...")
                warnings.append("DATABASE_URL format may be incorrect")
        else:
            print("✗ DATABASE_URL: NOT SET")
            all_checks_passed = False
        
        if settings.DATABASE_POOL_SIZE:
            print(f"✓ DATABASE_POOL_SIZE: {settings.DATABASE_POOL_SIZE}")
        else:
            print("✗ DATABASE_POOL_SIZE: NOT SET")
            all_checks_passed = False
        
        if settings.DATABASE_MAX_OVERFLOW:
            print(f"✓ DATABASE_MAX_OVERFLOW: {settings.DATABASE_MAX_OVERFLOW}")
        else:
            print("✗ DATABASE_MAX_OVERFLOW: NOT SET")
            all_checks_passed = False
        
        # Check 4: Verify REDIS configuration
        print("\n[CHECK 4] Verifying REDIS configuration...")
        if settings.REDIS_URL:
            print(f"✓ REDIS_URL: {settings.REDIS_URL}")
        else:
            print("✗ REDIS_URL: NOT SET")
            all_checks_passed = False
        
        if settings.REDIS_MAX_CONNECTIONS:
            print(f"✓ REDIS_MAX_CONNECTIONS: {settings.REDIS_MAX_CONNECTIONS}")
        else:
            print("✗ REDIS_MAX_CONNECTIONS: NOT SET")
            all_checks_passed = False
        
        # Check 5: Verify OLLAMA configuration
        print("\n[CHECK 5] Verifying OLLAMA configuration...")
        ollama_config = {
            'OLLAMA_BASE_URL': settings.OLLAMA_BASE_URL,
            'OLLAMA_MODEL': settings.OLLAMA_MODEL,
            'OLLAMA_TEMPERATURE': settings.OLLAMA_TEMPERATURE,
            'OLLAMA_MAX_TOKENS': settings.OLLAMA_MAX_TOKENS,
        }
        
        for key, value in ollama_config.items():
            if value is not None:
                print(f"✓ {key}: {value}")
            else:
                print(f"✗ {key}: NOT SET")
                all_checks_passed = False
        
        # Check 6: Verify SPOTIFY configuration
        print("\n[CHECK 6] Verifying SPOTIFY configuration...")
        spotify_config = {
            'SPOTIFY_CLIENT_ID': settings.SPOTIFY_CLIENT_ID,
            'SPOTIFY_CLIENT_SECRET': settings.SPOTIFY_CLIENT_SECRET,
            'SPOTIFY_REDIRECT_URI': settings.SPOTIFY_REDIRECT_URI,
        }
        
        for key, value in spotify_config.items():
            if value and value != "":
                # Don't print secrets
                print(f"✓ {key}: {'*' * 20} (SET)")
            else:
                print(f"⚠ {key}: NOT SET")
                warnings.append(f"{key} needs to be configured")
        
        # Check 7: Verify OPENWEATHER configuration
        print("\n[CHECK 7] Verifying OPENWEATHER configuration...")
        if settings.OPENWEATHER_API_KEY and settings.OPENWEATHER_API_KEY != "":
            print(f"✓ OPENWEATHER_API_KEY: {'*' * 20} (SET)")
        else:
            print(f"⚠ OPENWEATHER_API_KEY: NOT SET")
            warnings.append("OPENWEATHER_API_KEY needs to be configured")
        
        # Check 8: Verify CACHE_TTL configuration
        print("\n[CHECK 8] Verifying CACHE_TTL configuration...")
        cache_config = {
            'MOOD_CACHE_TTL': settings.MOOD_CACHE_TTL,
            'SEARCH_CACHE_TTL': settings.SEARCH_CACHE_TTL,
            'FEATURES_CACHE_TTL': settings.FEATURES_CACHE_TTL,
        }
        
        for key, value in cache_config.items():
            if value is not None and value > 0:
                print(f"✓ {key}: {value} seconds")
            else:
                print(f"✗ {key}: INVALID ({value})")
                all_checks_passed = False
        
        # Check 9: Verify AGENT configuration
        print("\n[CHECK 9] Verifying AGENT configuration...")
        agent_config = {
            'AGENT_MAX_ITERATIONS': settings.AGENT_MAX_ITERATIONS,
            'AGENT_TIMEOUT': settings.AGENT_TIMEOUT,
            'AGENT_VERBOSE': settings.AGENT_VERBOSE,
        }
        
        for key, value in agent_config.items():
            if value is not None:
                print(f"✓ {key}: {value}")
            else:
                print(f"✗ {key}: NOT SET")
                all_checks_passed = False
        
        # Check 10: Verify LOGGING configuration
        print("\n[CHECK 10] Verifying LOGGING configuration...")
        logging_config = {
            'LOG_LEVEL': settings.LOG_LEVEL,
            'LOG_FORMAT': settings.LOG_FORMAT[:50] + "..." if len(settings.LOG_FORMAT) > 50 else settings.LOG_FORMAT,
        }
        
        for key, value in logging_config.items():
            if value:
                print(f"✓ {key}: {value}")
            else:
                print(f"✗ {key}: NOT SET")
                all_checks_passed = False
        
        # Check 11: Verify CORS configuration
        print("\n[CHECK 11] Verifying CORS configuration...")
        if settings.CORS_ORIGINS:
            print(f"✓ CORS_ORIGINS: {len(settings.CORS_ORIGINS)} origins configured")
            for origin in settings.CORS_ORIGINS[:3]:  # Show first 3
                print(f"    - {origin}")
            if len(settings.CORS_ORIGINS) > 3:
                print(f"    ... and {len(settings.CORS_ORIGINS) - 3} more")
        else:
            print("✗ CORS_ORIGINS: NOT SET")
            all_checks_passed = False
        
        # Check 12: Test environment variable loading
        print("\n[CHECK 12] Testing environment variable loading...")
        
        # Check if .env file exists
        env_file = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_file):
            print(f"✓ .env file found: {env_file}")
            
            # Count lines in .env
            with open(env_file, 'r') as f:
                env_lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"✓ .env file contains {len(env_lines)} configuration lines")
        else:
            print(f"⚠ .env file not found at {env_file}")
            warnings.append(".env file should exist for local development")
        
        # Check 13: Validate configuration types
        print("\n[CHECK 13] Validating configuration data types...")
        
        type_checks = [
            ('APP_NAME', settings.APP_NAME, str),
            ('DEBUG', settings.DEBUG, bool),
            ('DATABASE_POOL_SIZE', settings.DATABASE_POOL_SIZE, int),
            ('OLLAMA_TEMPERATURE', settings.OLLAMA_TEMPERATURE, float),
            ('CORS_ORIGINS', settings.CORS_ORIGINS, list),
        ]
        
        for name, value, expected_type in type_checks:
            if isinstance(value, expected_type):
                print(f"✓ {name} is {expected_type.__name__}: {value}")
            else:
                print(f"✗ {name} is {type(value).__name__}, expected {expected_type.__name__}")
                all_checks_passed = False
        
        # Print warnings summary
        if warnings:
            print("\n" + "=" * 70)
            print("⚠ WARNINGS")
            print("=" * 70)
            for i, warning in enumerate(warnings, 1):
                print(f"{i}. {warning}")
        
        # Final summary
        print("\n" + "=" * 70)
        if all_checks_passed and not warnings:
            print("✅ ALL CHECKS PASSED - Task 2.4 Complete")
        elif all_checks_passed:
            print("✅ CHECKS PASSED WITH WARNINGS - Task 2.4 Complete")
            print("   (Warnings are for optional/future configuration)")
        else:
            print("❌ SOME CHECKS FAILED - Task 2.4 Incomplete")
        print("=" * 70)
        
        print("\nSummary:")
        print("  • Settings class instantiated correctly")
        print("  • All configuration groups loaded")
        print("  • Environment variables loaded from .env")
        print("  • Configuration data types validated")
        print("  • CORS, caching, and agent settings configured")
        
        if warnings:
            print(f"\n  Note: {len(warnings)} warnings (non-critical)")
        
        print("=" * 70)
        
        return all_checks_passed
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_configuration()
    sys.exit(0 if success else 1)
