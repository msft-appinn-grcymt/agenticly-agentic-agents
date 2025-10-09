from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from employee_repository import get_employee_repository

app = FastAPI(
    title="MS Roles API",
    description="API to get employee roles by first name or last name",
    version="1.0.0"
)

# Initialize repository
repository = get_employee_repository()

class NameRequest(BaseModel):
    first_name: str

class LastNameRequest(BaseModel):
    last_name: str

class RoleResponse(BaseModel):
    first_name: str
    role: str
    full_name: str

@app.get("/")
async def root():
    return {"message": "MS Roles API - Get employee roles by first name or last name"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/get-role", response_model=RoleResponse)
async def get_role(request: NameRequest):
    """
    Get employee role by first name
    """
    employee = repository.get_employee_by_first_name(request.first_name)
    
    if not employee:
        raise HTTPException(
            status_code=404, 
            detail=f"No employee found with first name: {request.first_name}"
        )
    
    return RoleResponse(
        first_name=request.first_name,
        role=employee["role"],
        full_name=employee["full_name"]
    )

@app.get("/get-role/{first_name}", response_model=RoleResponse)
async def get_role_by_path(first_name: str):
    """
    Get employee role by first name (path parameter)
    """
    employee = repository.get_employee_by_first_name(first_name)
    
    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"No employee found with first name: {first_name}"
        )
    
    return RoleResponse(
        first_name=first_name,
        role=employee["role"],
        full_name=employee["full_name"]
    )

@app.get("/employees")
async def list_all_employees():
    """
    List all employees and their roles
    """
    all_employees = repository.get_all_employees()
    
    employees = []
    for employee_data in all_employees:
        employees.append({
            "first_name": employee_data["first_name"].title(),
            "full_name": employee_data["full_name"],
            "role": employee_data["role"]
        })
    
    return {"employees": employees}

@app.post("/get-role-by-surname", response_model=RoleResponse)
async def get_role_by_surname(request: LastNameRequest):
    """
    Get employee role by last name
    """
    employee = repository.get_employee_by_last_name(request.last_name)
    
    if not employee:
        raise HTTPException(
            status_code=404, 
            detail=f"No employee found with last name: {request.last_name}"
        )
    
    return RoleResponse(
        first_name=employee["first_name"].title(),
        role=employee["role"],
        full_name=employee["full_name"]
    )

@app.get("/get-role-by-surname/{last_name}", response_model=RoleResponse)
async def get_role_by_surname_path(last_name: str):
    """
    Get employee role by last name (path parameter)
    """
    employee = repository.get_employee_by_last_name(last_name)
    
    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"No employee found with last name: {last_name}"
        )
    
    return RoleResponse(
        first_name=employee["first_name"].title(),
        role=employee["role"],
        full_name=employee["full_name"]
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
