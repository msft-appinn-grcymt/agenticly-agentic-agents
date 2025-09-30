from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn

app = FastAPI(
    title="MS Roles API",
    description="""
    A comprehensive API for managing and retrieving employee role information.
    
    This API provides endpoints to:
    * Get employee roles by first name
    * List all employees and their roles
    * Health monitoring
    
    The API follows RESTful principles and provides detailed responses with employee information.
    """,
    version="1.0.0",
    contact={
        "name": "MS Roles API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "roles",
            "description": "Operations related to employee roles retrieval",
        },
        {
            "name": "employees", 
            "description": "Operations for listing all employees",
        },
        {
            "name": "system",
            "description": "System operations like health checks",
        },
    ]
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
    """Request model for employee role lookup by first name."""
    first_name: str = Field(
        ...,
        description="The first name of the employee to look up",
        json_schema_extra={"example": "Mary"},
        min_length=1,
        max_length=50
    )

class RoleResponse(BaseModel):
    """Response model containing employee role information."""
    first_name: str = Field(
        ...,
        description="The first name of the employee",
        json_schema_extra={"example": "Mary"}
    )
    role: str = Field(
        ...,
        description="The job role/title of the employee",
        json_schema_extra={"example": "CSA Manager"}
    )
    full_name: str = Field(
        ...,
        description="The full name of the employee",
        json_schema_extra={"example": "Mary Bina"}
    )

class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(
        ...,
        description="Error message describing what went wrong",
        json_schema_extra={"example": "No employee found with first name: John"}
    )

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(
        ...,
        description="Current health status of the API",
        json_schema_extra={"example": "healthy"}
    )

class ApiResponse(BaseModel):
    """Root API response model."""
    message: str = Field(
        ...,
        description="Welcome message for the API",
        json_schema_extra={"example": "MS Roles API - Get employee roles by first name"}
    )

class Employee(BaseModel):
    """Individual employee model."""
    first_name: str = Field(
        ...,
        description="The first name of the employee",
        json_schema_extra={"example": "Mary"}
    )
    full_name: str = Field(
        ...,
        description="The full name of the employee", 
        json_schema_extra={"example": "Mary Bina"}
    )
    role: str = Field(
        ...,
        description="The job role/title of the employee",
        json_schema_extra={"example": "CSA Manager"}
    )

class EmployeesResponse(BaseModel):
    """Response model for listing all employees."""
    employees: List[Employee] = Field(
        ...,
        description="List of all employees and their roles"
    )

@app.get(
    "/",
    response_model=ApiResponse,
    tags=["system"],
    summary="API Root Endpoint",
    description="Returns basic information about the MS Roles API."
)
async def root():
    return ApiResponse(message="MS Roles API - Get employee roles by first name")

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
    summary="Health Check",
    description="Returns the current health status of the API service."
)
async def health_check():
    return HealthResponse(status="healthy")

@app.post(
    "/get-role",
    response_model=RoleResponse,
    responses={
        200: {
            "description": "Employee role found successfully",
            "model": RoleResponse,
        },
        404: {
            "description": "Employee not found",
            "model": ErrorResponse,
        },
        422: {
            "description": "Validation error in request data",
        }
    },
    tags=["roles"],
    summary="Get Employee Role (POST)",
    description="Retrieve an employee's role information by providing their first name in the request body."
)
async def get_role(request: NameRequest):
    """
    Get employee role by first name via POST request.
    
    - **first_name**: The first name of the employee (case-insensitive)
    
    Returns the employee's role, full name, and formatted first name.
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

@app.get(
    "/get-role/{first_name}",
    response_model=RoleResponse,
    responses={
        200: {
            "description": "Employee role found successfully",
            "model": RoleResponse,
        },
        404: {
            "description": "Employee not found",
            "model": ErrorResponse,
        },
        422: {
            "description": "Validation error in path parameter",
        }
    },
    tags=["roles"],
    summary="Get Employee Role (GET)",
    description="Retrieve an employee's role information by providing their first name as a path parameter."
)
async def get_role_by_path(
    first_name: str = Path(
        ...,
        description="The first name of the employee to look up (case-insensitive)",
        examples=["Mary"],
        min_length=1,
        max_length=50
    )
):
    """
    Get employee role by first name via GET request with path parameter.
    
    - **first_name**: The first name of the employee (case-insensitive)
    
    Returns the employee's role, full name, and formatted first name.
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

@app.get(
    "/employees",
    response_model=EmployeesResponse,
    tags=["employees"],
    summary="List All Employees",
    description="Retrieve a complete list of all employees with their roles and full names."
)
async def list_all_employees():
    """
    List all employees and their roles.
    
    Returns a comprehensive list of all employees in the system with their:
    - First name (formatted)
    - Full name
    - Job role/title
    """
    employees = []
    full_name_mapping = {
        "mary": "Mary Bina",
        "vasilis": "Vasilis Zisiadis", 
        "dimitris": "Dimitris Kotanis",
        "joanna": "Joanna Tsakona",
        "thanasis": "Thanasis Ragos"
    }
    
    for first_name, role in EMPLOYEE_ROLES.items():
        employees.append(Employee(
            first_name=first_name.title(),
            full_name=full_name_mapping[first_name],
            role=role
        ))
    
    return EmployeesResponse(employees=employees)

@app.get(
    "/swagger",
    tags=["system"],
    summary="Swagger Documentation",
    description="Redirect to the Swagger UI documentation interface.",
    response_class=RedirectResponse,
    status_code=302
)
async def swagger_redirect():
    """
    Redirect to Swagger UI documentation.
    
    This provides a dedicated '/swagger' path that redirects to the standard '/docs' endpoint
    for accessing the interactive API documentation.
    """
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
