import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "MS Roles API" in response.json()["message"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_role_post_valid():
    response = client.post("/get-role", json={"first_name": "Mary"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Mary"
    assert data["role"] == "CSA Manager"
    assert data["full_name"] == "Mary Bina"

def test_get_role_post_invalid():
    response = client.post("/get-role", json={"first_name": "Unknown"})
    assert response.status_code == 404

def test_get_role_path_valid():
    response = client.get("/get-role/Vasilis")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Vasilis"
    assert data["role"] == "CSA Cloud&AI"
    assert data["full_name"] == "Vasilis Zisiadis"

def test_get_role_path_invalid():
    response = client.get("/get-role/Unknown")
    assert response.status_code == 404

def test_list_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert len(data["employees"]) == 5

def test_case_insensitive():
    # Test with different cases
    response1 = client.get("/get-role/mary")
    response2 = client.get("/get-role/MARY") 
    response3 = client.get("/get-role/Mary")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    
    assert response1.json()["role"] == response2.json()["role"] == response3.json()["role"]

def test_swagger_ui_accessible():
    """Test that Swagger UI is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_swagger_redirect():
    """Test that /swagger redirects to /docs"""
    response = client.get("/swagger", follow_redirects=False)
    assert response.status_code == 307  # FastAPI uses 307 for RedirectResponse by default
    assert response.headers["location"] == "/docs"

def test_redoc_accessible():
    """Test that ReDoc is accessible"""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_openapi_json_accessible():
    """Test that OpenAPI JSON spec is accessible and valid"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
    # Check that it's a valid OpenAPI spec
    openapi_spec = response.json()
    assert "openapi" in openapi_spec
    assert openapi_spec["openapi"] == "3.1.0"
    assert "info" in openapi_spec
    assert openapi_spec["info"]["title"] == "MS Roles API"
    assert "paths" in openapi_spec
    assert "components" in openapi_spec

def test_openapi_spec_completeness():
    """Test that OpenAPI spec includes all expected endpoints and metadata"""
    response = client.get("/openapi.json")
    spec = response.json()
    
    # Check basic metadata
    assert spec["info"]["description"]
    assert spec["info"]["version"] == "1.0.0"
    assert "contact" in spec["info"]
    assert "license" in spec["info"]
    
    # Check all endpoints are documented
    paths = spec["paths"]
    assert "/" in paths
    assert "/health" in paths
    assert "/get-role" in paths
    assert "/get-role/{first_name}" in paths
    assert "/employees" in paths
    
    # Check tags are present
    tags_found = set()
    for path_data in paths.values():
        for method_data in path_data.values():
            if "tags" in method_data:
                tags_found.update(method_data["tags"])
    
    assert "system" in tags_found
    assert "roles" in tags_found
    assert "employees" in tags_found

def test_response_models_in_spec():
    """Test that response models are properly defined in the OpenAPI spec"""
    response = client.get("/openapi.json")
    spec = response.json()
    
    # Check that response models are defined
    schemas = spec["components"]["schemas"]
    assert "RoleResponse" in schemas
    assert "NameRequest" in schemas
    assert "EmployeesResponse" in schemas
    assert "ErrorResponse" in schemas
    assert "HealthResponse" in schemas
    assert "ApiResponse" in schemas
