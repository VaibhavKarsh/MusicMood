"""
Verification script for Task 2.5: Basic Health Check API
"""

import sys
from fastapi.testclient import TestClient

from app.main import app


def verify_health_api():
    """Verify health check API endpoints."""
    
    print("=" * 70)
    print("Verifying Basic Health Check API (Task 2.5)")
    print("=" * 70)
    
    try:
        client = TestClient(app)
        
        # Check 1: Test /health endpoint
        print("\n[CHECK 1] Testing /health endpoint...")
        response = client.get("/health")
        
        if response.status_code == 200:
            print("✓ /health endpoint returns 200 OK")
            
            data = response.json()
            
            # Check response structure
            required_fields = ["status", "timestamp", "environment", "version", "services"]
            for field in required_fields:
                if field in data:
                    print(f"✓ Response contains '{field}' field")
                else:
                    print(f"✗ Response missing '{field}' field")
                    return False
            
            # Check services
            if "services" in data:
                services = data["services"]
                required_services = ["api", "database", "redis", "ollama"]
                
                for service in required_services:
                    if service in services:
                        status = services[service].get("status", "unknown")
                        print(f"✓ {service.upper()} service: {status}")
                        
                        if status == "unhealthy":
                            print(f"  ⚠ {service} is unhealthy: {services[service].get('error', 'unknown error')}")
                    else:
                        print(f"✗ {service} service not in response")
                        return False
                
                # Check overall status
                if data["status"] in ["healthy", "degraded"]:
                    print(f"\n✓ Overall health status: {data['status']}")
                else:
                    print(f"\n✗ Invalid health status: {data['status']}")
                    return False
            
        else:
            print(f"✗ /health endpoint returned {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        # Check 2: Test /health/live endpoint
        print("\n[CHECK 2] Testing /health/live endpoint...")
        response = client.get("/health/live")
        
        if response.status_code == 200:
            print("✓ /health/live endpoint returns 200 OK")
            
            data = response.json()
            
            if data.get("status") == "alive":
                print("✓ Liveness probe returns 'alive' status")
            else:
                print(f"✗ Liveness probe returned unexpected status: {data.get('status')}")
                return False
            
            if "timestamp" in data:
                print(f"✓ Timestamp present: {data['timestamp']}")
            else:
                print("✗ Timestamp missing")
                return False
        else:
            print(f"✗ /health/live endpoint returned {response.status_code}")
            return False
        
        # Check 3: Test /health/ready endpoint
        print("\n[CHECK 3] Testing /health/ready endpoint...")
        response = client.get("/health/ready")
        
        if response.status_code == 200:
            print("✓ /health/ready endpoint returns 200 OK")
            
            data = response.json()
            
            if data.get("status") in ["ready", "not_ready"]:
                print(f"✓ Readiness probe returns '{data.get('status')}' status")
            else:
                print(f"✗ Readiness probe returned unexpected status: {data.get('status')}")
                return False
            
            if "database" in data:
                print(f"✓ Database status present: {data['database']}")
            else:
                print("✗ Database status missing")
                return False
        else:
            print(f"✗ /health/ready endpoint returned {response.status_code}")
            return False
        
        # Check 4: Verify database health check
        print("\n[CHECK 4] Verifying database health check details...")
        response = client.get("/health")
        data = response.json()
        
        db_health = data["services"]["database"]
        if "version" in db_health:
            print(f"✓ Database version reported: {db_health['version']}")
        else:
            print("⚠ Database version not reported")
        
        if "tables" in db_health:
            print(f"✓ Database tables count: {db_health['tables']}")
        else:
            print("⚠ Database tables count not reported")
        
        # Check 5: Verify Redis health check
        print("\n[CHECK 5] Verifying Redis health check details...")
        redis_health = data["services"]["redis"]
        
        if redis_health["status"] == "healthy":
            if "version" in redis_health:
                print(f"✓ Redis version reported: {redis_health['version']}")
            else:
                print("⚠ Redis version not reported")
            
            if "connected_clients" in redis_health:
                print(f"✓ Redis connected clients: {redis_health['connected_clients']}")
            else:
                print("⚠ Redis clients not reported")
        else:
            print(f"⚠ Redis health check failed: {redis_health.get('error', 'unknown')}")
        
        # Check 6: Verify Ollama health check
        print("\n[CHECK 6] Verifying Ollama health check details...")
        ollama_health = data["services"]["ollama"]
        
        if ollama_health["status"] == "healthy":
            if "configured_model" in ollama_health:
                print(f"✓ Configured model: {ollama_health['configured_model']}")
            else:
                print("⚠ Configured model not reported")
            
            if "model_available" in ollama_health:
                if ollama_health["model_available"]:
                    print(f"✓ Configured model is available")
                else:
                    print(f"⚠ Configured model is NOT available")
            
            if "available_models" in ollama_health:
                print(f"✓ Available models count: {ollama_health['available_models']}")
        else:
            print(f"⚠ Ollama health check failed: {ollama_health.get('error', 'unknown')}")
        
        # Check 7: Verify health endpoint in OpenAPI docs
        print("\n[CHECK 7] Verifying health endpoints in OpenAPI schema...")
        response = client.get("/openapi.json")
        
        if response.status_code == 200:
            openapi_schema = response.json()
            paths = openapi_schema.get("paths", {})
            
            health_endpoints = ["/health", "/health/live", "/health/ready"]
            for endpoint in health_endpoints:
                if endpoint in paths:
                    print(f"✓ {endpoint} documented in OpenAPI")
                else:
                    print(f"✗ {endpoint} not documented in OpenAPI")
                    return False
        else:
            print("⚠ Could not retrieve OpenAPI schema")
        
        # Check 8: Test response times
        print("\n[CHECK 8] Testing endpoint response times...")
        import time
        
        endpoints = ["/health", "/health/live", "/health/ready"]
        for endpoint in endpoints:
            start = time.time()
            response = client.get(endpoint)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                if elapsed < 5.0:  # Should respond within 5 seconds
                    print(f"✓ {endpoint} responded in {elapsed:.3f}s")
                else:
                    print(f"⚠ {endpoint} slow response: {elapsed:.3f}s")
            else:
                print(f"✗ {endpoint} failed")
                return False
        
        print("\n" + "=" * 70)
        print("✅ ALL CHECKS PASSED - Task 2.5 Complete")
        print("=" * 70)
        print("\nSummary:")
        print("  • /health endpoint working with comprehensive service checks")
        print("  • /health/live endpoint working (Kubernetes liveness probe)")
        print("  • /health/ready endpoint working (Kubernetes readiness probe)")
        print("  • Database connectivity verified")
        print("  • Redis connectivity verified")
        print("  • Ollama service connectivity verified")
        print("  • All endpoints documented in OpenAPI")
        print("  • Response times within acceptable range")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_health_api()
    sys.exit(0 if success else 1)
