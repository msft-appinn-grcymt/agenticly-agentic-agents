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
    assert len(data["employees"]) == 6

def test_case_insensitive():
    # Test with different cases
    response1 = client.get("/get-role/mary")
    response2 = client.get("/get-role/MARY") 
    response3 = client.get("/get-role/Mary")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    
    assert response1.json()["role"] == response2.json()["role"] == response3.json()["role"]
