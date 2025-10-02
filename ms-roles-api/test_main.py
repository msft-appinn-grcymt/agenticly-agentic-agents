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

def test_get_role_by_surname_post_valid():
    response = client.post("/get-role-by-surname", json={"last_name": "Kotanis"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Dimitris"
    assert data["role"] == "CSA Infra"
    assert data["full_name"] == "Dimitris Kotanis"

def test_get_role_by_surname_post_invalid():
    response = client.post("/get-role-by-surname", json={"last_name": "Unknown"})
    assert response.status_code == 404

def test_get_role_by_surname_path_valid():
    response = client.get("/get-role-by-surname/Tsakona")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Joanna"
    assert data["role"] == "CSAM"
    assert data["full_name"] == "Joanna Tsakona"

def test_get_role_by_surname_path_invalid():
    response = client.get("/get-role-by-surname/Unknown")
    assert response.status_code == 404

def test_surname_case_insensitive():
    # Test with different cases for surname
    response1 = client.get("/get-role-by-surname/kotanis")
    response2 = client.get("/get-role-by-surname/KOTANIS") 
    response3 = client.get("/get-role-by-surname/Kotanis")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    
    assert response1.json()["role"] == response2.json()["role"] == response3.json()["role"]
    assert response1.json()["full_name"] == "Dimitris Kotanis"

def test_all_surnames():
    # Test all available surnames
    surnames = ["Bina", "Zisiadis", "Kotanis", "Tsakona", "Ragos"]
    expected_roles = ["CSA Manager", "CSA Cloud&AI", "CSA Infra", "CSAM", "CSA Security"]
    
    for surname, expected_role in zip(surnames, expected_roles):
        response = client.get(f"/get-role-by-surname/{surname}")
        assert response.status_code == 200
        assert response.json()["role"] == expected_role
