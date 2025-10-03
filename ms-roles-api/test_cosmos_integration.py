"""
Tests for Cosmos DB integration and surname endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_role_by_surname_post():
    """Test POST endpoint for getting role by surname"""
    response = client.post("/get-role-by-surname", json={"last_name": "Kotanis"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Dimitris"
    assert data["role"] == "CSA Infra"
    assert data["full_name"] == "Dimitris Kotanis"


def test_get_role_by_surname_post_invalid():
    """Test POST endpoint with invalid surname"""
    response = client.post("/get-role-by-surname", json={"last_name": "Unknown"})
    assert response.status_code == 404


def test_get_role_by_surname_path():
    """Test GET endpoint for getting role by surname"""
    response = client.get("/get-role-by-surname/Bina")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Mary"
    assert data["role"] == "CSA Manager"
    assert data["full_name"] == "Mary Bina"


def test_get_role_by_surname_path_invalid():
    """Test GET endpoint with invalid surname"""
    response = client.get("/get-role-by-surname/Unknown")
    assert response.status_code == 404


def test_surname_case_insensitive():
    """Test that surname queries are case-insensitive"""
    response1 = client.get("/get-role-by-surname/kotanis")
    response2 = client.get("/get-role-by-surname/KOTANIS")
    response3 = client.get("/get-role-by-surname/Kotanis")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    
    assert response1.json()["role"] == response2.json()["role"] == response3.json()["role"]


def test_all_employees_have_surnames():
    """Test that all employees can be found by surname"""
    response = client.get("/employees")
    assert response.status_code == 200
    employees = response.json()["employees"]
    
    # Test each employee has a queryable surname
    for employee in employees:
        full_name = employee["full_name"]
        last_name = full_name.split()[-1]  # Get last name from full name
        
        surname_response = client.get(f"/get-role-by-surname/{last_name}")
        assert surname_response.status_code == 200
        assert surname_response.json()["full_name"] == full_name


def test_all_surnames():
    """Test all known surnames"""
    surnames = ["Bina", "Zisiadis", "Kotanis", "Tsakona", "Ragos", "Fotiadou"]
    
    for surname in surnames:
        response = client.get(f"/get-role-by-surname/{surname}")
        assert response.status_code == 200, f"Failed to find employee with surname: {surname}"
        data = response.json()
        assert surname.lower() in data["full_name"].lower()


def test_repository_consistency():
    """Test that all endpoints return consistent data from the repository"""
    # Get Vasilis by first name
    first_name_response = client.get("/get-role/Vasilis")
    assert first_name_response.status_code == 200
    first_name_data = first_name_response.json()
    
    # Get Vasilis by last name
    last_name_response = client.get("/get-role-by-surname/Zisiadis")
    assert last_name_response.status_code == 200
    last_name_data = last_name_response.json()
    
    # Both should return the same employee data
    assert first_name_data["full_name"] == last_name_data["full_name"]
    assert first_name_data["role"] == last_name_data["role"]


def test_employee_list_count():
    """Test that all 6 employees are present"""
    response = client.get("/employees")
    assert response.status_code == 200
    employees = response.json()["employees"]
    assert len(employees) == 6
    
    # Verify specific employees
    names = [e["first_name"].lower() for e in employees]
    assert "mary" in names
    assert "vasilis" in names
    assert "dimitris" in names
    assert "joanna" in names
    assert "thanasis" in names
    assert "konstantina" in names
