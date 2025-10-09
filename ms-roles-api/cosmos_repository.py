"""
Cosmos DB Repository for Employee Data
Implements data access layer with fallback to in-memory data
"""
from typing import Optional, List, Dict

# Try to import Cosmos DB SDK, but allow fallback if not available
try:
    from azure.cosmos.exceptions import CosmosResourceNotFoundError
    COSMOS_AVAILABLE = True
except ImportError:
    COSMOS_AVAILABLE = False
    # Define a dummy exception for compatibility
    class CosmosResourceNotFoundError(Exception):
        pass

from cosmos_config import cosmos_config, USE_COSMOS_DB


# Fallback in-memory data for local development
FALLBACK_EMPLOYEES = {
    "mary": {
        "id": "mary",
        "first_name": "mary",
        "last_name": "bina",
        "full_name": "Mary Bina",
        "role": "CSA Manager"
    },
    "vasilis": {
        "id": "vasilis",
        "first_name": "vasilis",
        "last_name": "zisiadis",
        "full_name": "Vasilis Zisiadis",
        "role": "CSA Cloud&AI"
    },
    "dimitris": {
        "id": "dimitris",
        "first_name": "dimitris",
        "last_name": "kotanis",
        "full_name": "Dimitris Kotanis",
        "role": "CSA Infra"
    },
    "joanna": {
        "id": "joanna",
        "first_name": "joanna",
        "last_name": "tsakona",
        "full_name": "Joanna Tsakona",
        "role": "CSAM"
    },
    "thanasis": {
        "id": "thanasis",
        "first_name": "thanasis",
        "last_name": "ragos",
        "full_name": "Thanasis Ragos",
        "role": "CSA Security"
    },
    "konstantina": {
        "id": "konstantina",
        "first_name": "konstantina",
        "last_name": "fotiadou",
        "full_name": "Konstantina Fotiadou",
        "role": "CSA Data&AI"
    }
}


class EmployeeRepository:
    """Repository pattern for employee data access"""
    
    def __init__(self):
        self.container = cosmos_config.get_container()
        self.use_cosmos = USE_COSMOS_DB and self.container is not None
        
        # Cache for performance
        self._cache: Optional[Dict[str, dict]] = None
    
    def _get_all_from_cosmos(self) -> Dict[str, dict]:
        """Fetch all employees from Cosmos DB"""
        if not self.use_cosmos:
            return FALLBACK_EMPLOYEES
        
        try:
            query = "SELECT * FROM c"
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            # Convert to dictionary keyed by first_name (lowercase)
            employees = {}
            for item in items:
                first_name_key = item.get("first_name", "").lower()
                if first_name_key:
                    employees[first_name_key] = item
            
            return employees if employees else FALLBACK_EMPLOYEES
            
        except Exception as e:
            print(f"Error fetching from Cosmos DB: {e}")
            return FALLBACK_EMPLOYEES
    
    def _get_cache(self) -> Dict[str, dict]:
        """Get cached employee data with lazy loading"""
        if self._cache is None:
            self._cache = self._get_all_from_cosmos()
        return self._cache
    
    def invalidate_cache(self):
        """Invalidate cache to force refresh on next access"""
        self._cache = None
    
    def get_employee_by_first_name(self, first_name: str) -> Optional[dict]:
        """
        Get employee by first name (case-insensitive)
        
        Args:
            first_name: Employee's first name
            
        Returns:
            Employee dictionary or None if not found
        """
        first_name_lower = first_name.lower().strip()
        
        if self.use_cosmos:
            try:
                # Try direct query for better performance
                query = "SELECT * FROM c WHERE LOWER(c.first_name) = @first_name"
                parameters = [{"name": "@first_name", "value": first_name_lower}]
                
                items = list(self.container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True
                ))
                
                return items[0] if items else None
                
            except Exception as e:
                print(f"Error querying Cosmos DB: {e}")
                # Fallback to cache
                return self._get_cache().get(first_name_lower)
        
        return self._get_cache().get(first_name_lower)
    
    def get_employee_by_last_name(self, last_name: str) -> Optional[dict]:
        """
        Get employee by last name (case-insensitive)
        
        Args:
            last_name: Employee's last name
            
        Returns:
            Employee dictionary or None if not found
        """
        last_name_lower = last_name.lower().strip()
        
        if self.use_cosmos:
            try:
                # Query by last name
                query = "SELECT * FROM c WHERE LOWER(c.last_name) = @last_name"
                parameters = [{"name": "@last_name", "value": last_name_lower}]
                
                items = list(self.container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True
                ))
                
                return items[0] if items else None
                
            except Exception as e:
                print(f"Error querying Cosmos DB: {e}")
                # Fallback to cache
                cache = self._get_cache()
                for employee in cache.values():
                    if employee.get("last_name", "").lower() == last_name_lower:
                        return employee
                return None
        
        # Search in cache
        cache = self._get_cache()
        for employee in cache.values():
            if employee.get("last_name", "").lower() == last_name_lower:
                return employee
        
        return None
    
    def get_all_employees(self) -> List[dict]:
        """
        Get all employees
        
        Returns:
            List of employee dictionaries
        """
        cache = self._get_cache()
        return list(cache.values())
    
    def create_employee(self, employee: dict) -> dict:
        """
        Create a new employee
        
        Args:
            employee: Employee data dictionary
            
        Returns:
            Created employee dictionary
        """
        if not self.use_cosmos:
            # Update fallback data
            first_name_key = employee.get("first_name", "").lower()
            FALLBACK_EMPLOYEES[first_name_key] = employee
            self.invalidate_cache()
            return employee
        
        try:
            # Ensure id is set to first_name for partition key
            if "id" not in employee:
                employee["id"] = employee.get("first_name", "").lower()
            
            created = self.container.create_item(body=employee)
            self.invalidate_cache()
            return created
            
        except Exception as e:
            print(f"Error creating employee in Cosmos DB: {e}")
            raise


# Global repository instance
employee_repository = EmployeeRepository()
