"""
Employee repository for data access with Cosmos DB support and in-memory fallback.
Implements repository pattern with caching for optimal performance.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from config import settings

# Optional import for Azure Cosmos DB
try:
    from azure.cosmos import CosmosClient, exceptions, PartitionKey
    COSMOS_AVAILABLE = True
except ImportError:
    COSMOS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Azure Cosmos DB SDK not available. Using in-memory fallback only.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback hardcoded data (used when Cosmos DB is disabled)
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
    """
    Repository for employee data with Cosmos DB support.
    Implements caching and graceful fallback to in-memory data.
    """
    
    def __init__(self):
        """Initialize repository with optional Cosmos DB connection."""
        self._container = None
        self._cache: Dict[str, any] = {}
        self._cache_timestamp: Optional[datetime] = None
        self._use_cosmos = settings.USE_COSMOS_DB and COSMOS_AVAILABLE
        
        if settings.USE_COSMOS_DB and not COSMOS_AVAILABLE:
            logger.warning("Cosmos DB requested but SDK not available. Using in-memory fallback.")
        
        if self._use_cosmos:
            try:
                self._initialize_cosmos_db()
                logger.info("Successfully connected to Cosmos DB")
            except Exception as e:
                logger.error(f"Failed to initialize Cosmos DB: {e}")
                logger.warning("Falling back to in-memory data")
                self._use_cosmos = False
        else:
            logger.info("Using in-memory employee data (Cosmos DB disabled)")
    
    def _initialize_cosmos_db(self):
        """Initialize Cosmos DB client and container."""
        settings.validate()
        
        # Create Cosmos DB client with connection pooling
        client = CosmosClient(
            settings.COSMOS_ENDPOINT,
            settings.COSMOS_KEY,
            connection_verify=True,
            connection_timeout=5,
            request_timeout=10
        )
        
        # Get or create database
        try:
            database = client.create_database_if_not_exists(
                id=settings.COSMOS_DATABASE_NAME
            )
            logger.info(f"Database '{settings.COSMOS_DATABASE_NAME}' ready")
        except exceptions.CosmosResourceExistsError:
            database = client.get_database_client(settings.COSMOS_DATABASE_NAME)
        
        # Get or create container with partition key on first_name for efficient queries
        try:
            self._container = database.create_container_if_not_exists(
                id=settings.COSMOS_CONTAINER_NAME,
                partition_key=PartitionKey(path="/first_name"),
                offer_throughput=400  # Minimum RU/s for cost optimization
            )
            logger.info(f"Container '{settings.COSMOS_CONTAINER_NAME}' ready")
        except exceptions.CosmosResourceExistsError:
            self._container = database.get_container_client(
                settings.COSMOS_CONTAINER_NAME
            )
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid based on TTL."""
        if not self._cache_timestamp:
            return False
        
        age = datetime.now() - self._cache_timestamp
        return age < timedelta(seconds=settings.CACHE_TTL_SECONDS)
    
    def _refresh_cache(self):
        """Refresh the employee cache from database."""
        if self._use_cosmos and self._container:
            try:
                # Query all employees
                query = "SELECT * FROM c"
                items = list(self._container.query_items(
                    query=query,
                    enable_cross_partition_query=True
                ))
                
                # Build cache indexed by lowercase first_name
                self._cache = {
                    item["first_name"].lower(): item
                    for item in items
                }
                self._cache_timestamp = datetime.now()
                logger.info(f"Cache refreshed with {len(self._cache)} employees")
            except Exception as e:
                logger.error(f"Failed to refresh cache from Cosmos DB: {e}")
                # Fall back to hardcoded data on error
                self._cache = FALLBACK_EMPLOYEES.copy()
                self._cache_timestamp = datetime.now()
        else:
            # Use fallback data when Cosmos DB is not available
            self._cache = FALLBACK_EMPLOYEES.copy()
            self._cache_timestamp = datetime.now()
    
    def get_employee_by_first_name(self, first_name: str) -> Optional[Dict]:
        """
        Get employee by first name (case-insensitive).
        
        Args:
            first_name: Employee's first name
            
        Returns:
            Employee dictionary or None if not found
        """
        first_name_lower = first_name.lower().strip()
        
        # Check cache validity and refresh if needed
        if not self._is_cache_valid():
            self._refresh_cache()
        
        return self._cache.get(first_name_lower)
    
    def get_employee_by_last_name(self, last_name: str) -> Optional[Dict]:
        """
        Get employee by last name (case-insensitive).
        
        Args:
            last_name: Employee's last name
            
        Returns:
            Employee dictionary or None if not found
        """
        last_name_lower = last_name.lower().strip()
        
        # Check cache validity and refresh if needed
        if not self._is_cache_valid():
            self._refresh_cache()
        
        # Search for employee with matching last name
        for employee in self._cache.values():
            if employee.get("last_name", "").lower() == last_name_lower:
                return employee
        
        return None
    
    def get_all_employees(self) -> List[Dict]:
        """
        Get all employees.
        
        Returns:
            List of all employee dictionaries
        """
        # Check cache validity and refresh if needed
        if not self._is_cache_valid():
            self._refresh_cache()
        
        return list(self._cache.values())
    
    def create_employee(self, employee_data: Dict) -> Dict:
        """
        Create a new employee record.
        
        Args:
            employee_data: Employee data dictionary
            
        Returns:
            Created employee dictionary
        """
        if self._use_cosmos and self._container:
            try:
                # Ensure id field is set to first_name for consistency
                if "id" not in employee_data:
                    employee_data["id"] = employee_data["first_name"].lower()
                
                created_item = self._container.create_item(body=employee_data)
                
                # Invalidate cache to force refresh on next read
                self._cache_timestamp = None
                
                logger.info(f"Created employee: {employee_data['first_name']}")
                return created_item
            except Exception as e:
                logger.error(f"Failed to create employee: {e}")
                raise
        else:
            # For in-memory mode, just add to cache
            employee_id = employee_data.get("first_name", "").lower()
            if "id" not in employee_data:
                employee_data["id"] = employee_id
            
            self._cache[employee_id] = employee_data
            self._cache_timestamp = datetime.now()
            
            return employee_data


# Global repository instance (singleton pattern)
_repository_instance: Optional[EmployeeRepository] = None


def get_employee_repository() -> EmployeeRepository:
    """
    Get the global employee repository instance (singleton).
    
    Returns:
        EmployeeRepository instance
    """
    global _repository_instance
    
    if _repository_instance is None:
        _repository_instance = EmployeeRepository()
    
    return _repository_instance
