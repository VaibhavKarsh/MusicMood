"""
Test FastAPI application initialization
Phase 2, Task 2.1, Subtask 2.1.2
"""
from app.main import app
from app.config.settings import settings

def test_app_initialization():
    """Test that FastAPI app initializes without errors"""
    print("=" * 70)
    print("Testing FastAPI Application Initialization")
    print("=" * 70)
    
    # Test app exists
    assert app is not None, "App should be initialized"
    print("✓ FastAPI app instance created")
    
    # Test app properties
    assert app.title == settings.APP_NAME, "App title should match settings"
    print(f"✓ App title: {app.title}")
    
    assert app.version == settings.APP_VERSION, "App version should match settings"
    print(f"✓ App version: {app.version}")
    
    assert app.debug == settings.DEBUG, "Debug mode should match settings"
    print(f"✓ Debug mode: {app.debug}")
    
    # Test routes exist
    routes = [route.path for route in app.routes]
    assert "/" in routes, "Root route should exist"
    print(f"✓ Root route exists")
    
    # Test docs routes
    if settings.DEBUG:
        assert "/docs" in routes or any("openapi" in r for r in routes), "Docs should be available in debug mode"
        print("✓ API documentation available")
    
    print("\n" + "=" * 70)
    print("✅ FastAPI Application Initialized Successfully")
    print("=" * 70)
    return True

if __name__ == "__main__":
    test_app_initialization()
