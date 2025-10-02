from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="MS Roles API",
    description="API to get employee roles by first name",
    version="1.0.0"
)

# Data mapping first names to roles
EMPLOYEE_ROLES = {
    "mary": "CSA Manager",
    "vasilis": "CSA Cloud&AI", 
    "dimitris": "CSA Infra",
    "joanna": "CSAM",
    "thanasis": "CSA Security"
}

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
    
    if first_name not in EMPLOYEE_ROLES:
        raise HTTPException(
            status_code=404, 
            detail=f"No employee found with first name: {request.first_name}"
        )
    
    role = EMPLOYEE_ROLES[first_name]
    
    # Map back to full names for response
    full_name_mapping = {
        "mary": "Mary Bina",
        "vasilis": "Vasilis Zisiadis",
        "dimitris": "Dimitris Kotanis", 
        "joanna": "Joanna Tsakona",
        "thanasis": "Thanasis Ragos"
    }
    
    return RoleResponse(
        first_name=request.first_name,
        role=role,
        full_name=full_name_mapping[first_name]
    )

@app.get("/get-role/{first_name}", response_model=RoleResponse)
async def get_role_by_path(first_name: str):
    """
    Get employee role by first name (path parameter)
    """
    first_name_lower = first_name.lower().strip()
    
    if first_name_lower not in EMPLOYEE_ROLES:
        raise HTTPException(
            status_code=404,
            detail=f"No employee found with first name: {first_name}"
        )
    
    role = EMPLOYEE_ROLES[first_name_lower]
    
    # Map back to full names for response
    full_name_mapping = {
        "mary": "Mary Bina", 
        "vasilis": "Vasilis Zisiadis",
        "dimitris": "Dimitris Kotanis",
        "joanna": "Joanna Tsakona", 
        "thanasis": "Thanasis Ragos"
    }
    
    return RoleResponse(
        first_name=first_name,
        role=role,
        full_name=full_name_mapping[first_name_lower]
    )

@app.get("/employees")
async def list_all_employees():
    """
    List all employees and their roles
    """
    employees = []
    full_name_mapping = {
        "mary": "Mary Bina",
        "vasilis": "Vasilis Zisiadis", 
        "dimitris": "Dimitris Kotanis",
        "joanna": "Joanna Tsakona",
        "thanasis": "Thanasis Ragos",
        "konstantina": "Konstantina Fotiadou"
            }
    
    for first_name, role in EMPLOYEE_ROLES.items():
        employees.append({
            "first_name": first_name.title(),
            "full_name": full_name_mapping[first_name],
            "role": role
        })
    
    return {"employees": employees}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
