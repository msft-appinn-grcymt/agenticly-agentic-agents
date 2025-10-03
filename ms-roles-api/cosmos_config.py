"""
Cosmos DB Configuration Module
Handles connection settings and initialization for Azure Cosmos DB
"""
import os
from typing import Optional

# Try to import Cosmos DB SDK, but allow fallback if not available
try:
    from azure.cosmos import CosmosClient, PartitionKey
    COSMOS_SDK_AVAILABLE = True
except ImportError:
    COSMOS_SDK_AVAILABLE = False
    # Define dummy classes for compatibility
    class CosmosClient:
        pass
    class PartitionKey:
        def __init__(self, path):
            pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Cosmos DB Configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "")
COSMOS_KEY = os.getenv("COSMOS_KEY", "")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "employees-db")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "employees")

# Fallback mode for local development without Cosmos DB
USE_COSMOS_DB = os.getenv("USE_COSMOS_DB", "false").lower() == "true"


class CosmosDBConfig:
    """Singleton configuration class for Cosmos DB"""
    
    _instance: Optional['CosmosDBConfig'] = None
    _client: Optional[CosmosClient] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CosmosDBConfig, cls).__new__(cls)
        return cls._instance
    
    def get_client(self) -> Optional[CosmosClient]:
        """
        Get or create Cosmos DB client with connection pooling
        Returns None if Cosmos DB is not configured
        """
        if not USE_COSMOS_DB or not COSMOS_SDK_AVAILABLE:
            return None
            
        if self._client is None:
            if not COSMOS_ENDPOINT or not COSMOS_KEY:
                raise ValueError(
                    "Cosmos DB is enabled but COSMOS_ENDPOINT or COSMOS_KEY is not set. "
                    "Please configure these environment variables or set USE_COSMOS_DB=false"
                )
            
            self._client = CosmosClient(
                url=COSMOS_ENDPOINT,
                credential=COSMOS_KEY,
                connection_timeout=300,  # 5 minutes
                request_timeout=30  # 30 seconds per request
            )
        
        return self._client
    
    def get_database(self):
        """Get or create database"""
        client = self.get_client()
        if client is None:
            return None
        
        database = client.create_database_if_not_exists(id=COSMOS_DATABASE_NAME)
        return database
    
    def get_container(self):
        """Get or create container with optimized indexing"""
        database = self.get_database()
        if database is None:
            return None
        
        # Define partition key and indexing policy
        partition_key = PartitionKey(path="/id")
        
        # Optimized indexing policy for employee queries
        indexing_policy = {
            "indexingMode": "consistent",
            "automatic": True,
            "includedPaths": [
                {"path": "/first_name/?"},
                {"path": "/last_name/?"},
                {"path": "/role/?"}
            ],
            "excludedPaths": [
                {"path": "/\"_etag\"/?"}
            ]
        }
        
        container = database.create_container_if_not_exists(
            id=COSMOS_CONTAINER_NAME,
            partition_key=partition_key,
            indexing_policy=indexing_policy
        )
        
        return container


# Global instance
cosmos_config = CosmosDBConfig()
