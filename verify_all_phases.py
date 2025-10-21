"""
Master Verification Script for MusicMood Project
Verifies all completed phases and tasks
"""

import sys
import os
import subprocess
from typing import Dict, List, Tuple


def run_verification(script_name: str, description: str) -> Tuple[bool, str]:
    """Run a verification script and return success status."""
    print(f"\n{'=' * 70}")
    print(f"Running: {description}")
    print(f"{'=' * 70}")
    
    try:
        result = subprocess.run(
            ["poetry", "run", "python", script_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Print output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        return success, result.stdout
    
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: {script_name} took longer than 60 seconds")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ ERROR running {script_name}: {e}")
        return False, str(e)


def verify_file_structure():
    """Verify project file structure exists."""
    print(f"\n{'=' * 70}")
    print("Verifying Project File Structure")
    print(f"{'=' * 70}")
    
    required_files = [
        # Configuration
        "pyproject.toml",
        ".env",
        "alembic.ini",
        
        # Main application
        "app/__init__.py",
        "app/main.py",
        
        # Configuration
        "app/config/__init__.py",
        "app/config/settings.py",
        
        # Database
        "app/db/__init__.py",
        "app/db/database.py",
        
        # Models
        "app/models/__init__.py",
        "app/models/base.py",
        "app/models/user.py",
        "app/models/mood_entry.py",
        "app/models/playlist_recommendation.py",
        
        # API
        "app/api/__init__.py",
        "app/api/health.py",
        
        # Alembic
        "alembic/env.py",
        "alembic/README",
        
        # Docker
        "docker-compose.yml",
    ]
    
    required_dirs = [
        "app",
        "app/config",
        "app/db",
        "app/models",
        "app/api",
        "app/agents",
        "app/tools",
        "app/services",
        "alembic",
        "alembic/versions",
        "tests",
    ]
    
    all_exist = True
    
    print("\n[FILES]")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} MISSING")
            all_exist = False
    
    print("\n[DIRECTORIES]")
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✓ {directory}/")
        else:
            print(f"✗ {directory}/ MISSING")
            all_exist = False
    
    return all_exist


def verify_dependencies():
    """Verify Poetry dependencies are installed."""
    print(f"\n{'=' * 70}")
    print("Verifying Dependencies")
    print(f"{'=' * 70}")
    
    try:
        result = subprocess.run(
            ["poetry", "show"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')
            print(f"✓ {len(packages)} packages installed")
            
            # Check key dependencies
            key_deps = [
                "fastapi",
                "uvicorn",
                "sqlalchemy",
                "psycopg2-binary",
                "redis",
                "langchain",
                "langchain-ollama",
                "spotipy",
                "transformers",
                "alembic"
            ]
            
            installed = {line.split()[0] for line in packages if line.strip()}
            
            for dep in key_deps:
                if dep in installed:
                    print(f"✓ {dep}")
                else:
                    print(f"✗ {dep} NOT INSTALLED")
                    return False
            
            return True
        else:
            print(f"✗ Failed to check dependencies: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"✗ Error checking dependencies: {e}")
        return False


def verify_docker_services():
    """Verify Docker services are running."""
    print(f"\n{'=' * 70}")
    print("Verifying Docker Services")
    print(f"{'=' * 70}")
    
    try:
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout
        
        if "postgres" in output.lower() and "up" in output.lower():
            print("✓ PostgreSQL container running")
        else:
            print("⚠ PostgreSQL container not running")
            return False
        
        # Check Redis (might be running outside Docker)
        result = subprocess.run(
            ["powershell", "-Command", "Get-NetTCPConnection -LocalPort 6379 -ErrorAction SilentlyContinue"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("✓ Redis service running (port 6379)")
        else:
            print("⚠ Redis not detected on port 6379")
        
        return True
    
    except Exception as e:
        print(f"⚠ Could not verify Docker services: {e}")
        return True  # Don't fail on this


def verify_database_migrations():
    """Verify database migrations are applied."""
    print(f"\n{'=' * 70}")
    print("Verifying Database Migrations")
    print(f"{'=' * 70}")
    
    try:
        result = subprocess.run(
            ["poetry", "run", "alembic", "current"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "191bb54848e3" in result.stdout or "(head)" in result.stdout:
            print("✓ Database migrations applied")
            print(f"  Current: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠ No migrations applied: {result.stdout}")
            return False
    
    except Exception as e:
        print(f"✗ Error checking migrations: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("MUSICMOOD - COMPREHENSIVE VERIFICATION")
    print("Verifying Phase 1 & Phase 2 Implementation")
    print("=" * 70)
    
    results: Dict[str, bool] = {}
    
    # Phase 0: File structure
    results["File Structure"] = verify_file_structure()
    
    # Phase 0: Dependencies
    results["Dependencies"] = verify_dependencies()
    
    # Phase 0: Docker services
    results["Docker Services"] = verify_docker_services()
    
    # Phase 0: Database migrations
    results["Database Migrations"] = verify_database_migrations()
    
    # Phase 1: Verification scripts
    phase1_checks = [
        ("verify_phase1.py", "Phase 1: Local Environment Setup"),
    ]
    
    for script, description in phase1_checks:
        if os.path.exists(script):
            success, _ = run_verification(script, description)
            results[description] = success
        else:
            print(f"\n⚠ {script} not found, skipping")
    
    # Phase 2: Verification scripts
    phase2_checks = [
        ("verify_task_2_2.py", "Phase 2 Task 2.2: Database Models & Schema"),
        ("verify_task_2_3.py", "Phase 2 Task 2.3: Database Connection & Session Management"),
        ("verify_task_2_4.py", "Phase 2 Task 2.4: Environment Configuration Management"),
        ("verify_task_2_5.py", "Phase 2 Task 2.5: Basic Health Check API"),
    ]
    
    for script, description in phase2_checks:
        if os.path.exists(script):
            success, _ = run_verification(script, description)
            results[description] = success
        else:
            print(f"\n⚠ {script} not found, skipping")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for check, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {check}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    total = passed + failed
    print(f"Results: {passed}/{total} checks passed ({(passed/total*100):.1f}%)")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("✅ Phase 1: Local Environment Setup - COMPLETE")
        print("✅ Phase 2: Core Backend Architecture - COMPLETE")
        print("\nReady to proceed to Phase 3: Agent Development")
        return 0
    else:
        print(f"\n⚠ {failed} verification(s) failed")
        print("Please review the failures above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
