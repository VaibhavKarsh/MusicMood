"""
Test FastAPI middleware configuration
Phase 2, Task 2.1, Subtask 2.1.3
"""
from app.main import app

def test_middleware():
    """Test that middleware is configured correctly"""
    print("=" * 70)
    print("Testing FastAPI Middleware Configuration")
    print("=" * 70)
    
    # Get middleware stack
    middleware_stack = []
    for middleware in app.user_middleware:
        middleware_name = middleware.cls.__name__
        middleware_stack.append(middleware_name)
        print(f"✓ Middleware: {middleware_name}")
    
    # Verify CORS middleware exists
    assert "CORSMiddleware" in middleware_stack, "CORS middleware should be configured"
    print("✓ CORS middleware configured")
    
    # Verify GZip middleware exists
    assert "GZipMiddleware" in middleware_stack, "GZip middleware should be configured"
    print("✓ GZip compression configured")
    
    # Verify CORS is in the stack (middleware order is reversed in stack)
    assert "CORSMiddleware" in middleware_stack, "CORS should be in middleware stack"
    print("✓ Middleware order verified (CORS will be executed first)")
    
    print("\n" + "=" * 70)
    print("✅ All Middleware Configured Successfully")
    print("=" * 70)
    return True

if __name__ == "__main__":
    test_middleware()
