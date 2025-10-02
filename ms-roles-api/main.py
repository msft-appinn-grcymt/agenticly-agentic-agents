from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="MS Roles API",
    description="API to get employee roles by first name",
    version="1.0.0"
)

# Centralized employee data structure
EMPLOYEES = {
    "mary": {
        "first_name": "mary",
        "last_name": "bina",
        "full_name": "Mary Bina",
        "role": "CSA Manager"
    },
    "vasilis": {
        "first_name": "vasilis",
        "last_name": "zisiadis",
        "full_name": "Vasilis Zisiadis",
        "role": "CSA Cloud&AI"
    },
    "dimitris": {
        "first_name": "dimitris",
        "last_name": "kotanis",
        "full_name": "Dimitris Kotanis",
        "role": "CSA Infra"
    },
    "joanna": {
        "first_name": "joanna",
        "last_name": "tsakona",
        "full_name": "Joanna Tsakona",
        "role": "CSAM"
    },
    "thanasis": {
        "first_name": "thanasis",
        "last_name": "ragos",
        "full_name": "Thanasis Ragos",
        "role": "CSA Security"
    },
    "konstantina": {
        "first_name": "konstantina",
        "last_name": "fotiadou",
        "full_name": "Konstantina Fotiadou",
        "role": "CSA Data&AI"
    }
}

# Backward compatibility - derived from EMPLOYEES
EMPLOYEE_ROLES = {k: v["role"] for k, v in EMPLOYEES.items()}

class NameRequest(BaseModel):
    first_name: str

class RoleResponse(BaseModel):
    first_name: str
    role: str
    full_name: str

@app.get("/")
async def root():
    return {"message": "MS Roles API - Get employee roles by first name"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/get-role", response_model=RoleResponse)
async def get_role(request: NameRequest):
    """
    Get employee role by first name
    """
    first_name = request.first_name.lower().strip()
    
    if first_name not in EMPLOYEES:
        raise HTTPException(
            status_code=404, 
            detail=f"No employee found with first name: {request.first_name}"
        )
    
    employee = EMPLOYEES[first_name]
    
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
    first_name_lower = first_name.lower().strip()
    
    if first_name_lower not in EMPLOYEES:
        raise HTTPException(
            status_code=404,
            detail=f"No employee found with first name: {first_name}"
        )
    
    employee = EMPLOYEES[first_name_lower]
    
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
    employees = []
    
    for employee_data in EMPLOYEES.values():
        employees.append({
            "first_name": employee_data["first_name"].title(),
            "full_name": employee_data["full_name"],
            "role": employee_data["role"]
        })
    
    return {"employees": employees}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
