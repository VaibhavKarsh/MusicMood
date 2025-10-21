"""
Test FastAPI server with TestClient
Phase 2, Task 2.1, Subtask 2.1.3 - Final Verification
"""
from fastapi.testclient import TestClient
from app.main import app
import sys

def test_api_server():
    """Test FastAPI server responds to requests"""
    print("=" * 70)
    print("Testing FastAPI Server with TestClient")
    print("=" * 70)
    
    # Create test client
    client = TestClient(app)
    
    try:
        # Test root endpoint
        response = client.get("/")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✓ Server responded with status: {response.status_code}")
        
        data = response.json()
        assert data["name"] == "MusicMood", "App name should be MusicMood"
        assert data["version"] == "0.1.0", "Version should be 0.1.0"
        assert data["status"] == "running", "Status should be running"
        print(f"✓ API returned correct data: {data['name']} v{data['version']}")
        print(f"✓ Status: {data['status']}")
        print(f"✓ Environment: {data['environment']}")
        
        # Test docs endpoint (should exist in debug mode)
        response_docs = client.get("/docs")
        assert response_docs.status_code == 200, "Docs should be accessible in debug mode"
        print(f"✓ API documentation accessible at /docs")
        
        print("\n" + "=" * 70)
        print("✅ FastAPI Server Working Correctly")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_server()
    sys.exit(0 if success else 1)
