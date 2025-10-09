#!/usr/bin/env python
"""
Script to initialize Cosmos DB with employee data.
This script creates the database and container if they don't exist,
and seeds the initial employee data.

Usage:
    python init_cosmos_db.py
    
Environment variables required:
    COSMOS_ENDPOINT: Cosmos DB endpoint URL
    COSMOS_KEY: Cosmos DB primary key
    COSMOS_DATABASE_NAME: Database name (default: employees-db)
    COSMOS_CONTAINER_NAME: Container name (default: employees)
"""
import sys
import logging
from employee_repository import get_employee_repository, FALLBACK_EMPLOYEES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def seed_employee_data():
    """Seed the Cosmos DB with initial employee data."""
    try:
        repository = get_employee_repository()
        
        if not repository._use_cosmos:
            logger.error("Cosmos DB is not enabled or not available.")
            logger.error("Please set USE_COSMOS_DB=true and ensure COSMOS_ENDPOINT and COSMOS_KEY are configured.")
            return False
        
        logger.info("Starting employee data seeding...")
        
        # Seed all employees from fallback data
        for first_name, employee_data in FALLBACK_EMPLOYEES.items():
            try:
                # Check if employee already exists
                existing = repository.get_employee_by_first_name(first_name)
                
                if existing:
                    logger.info(f"Employee {first_name} already exists, skipping...")
                else:
                    # Create employee
                    repository.create_employee(employee_data)
                    logger.info(f"Created employee: {employee_data['full_name']}")
            
            except Exception as e:
                logger.error(f"Failed to create employee {first_name}: {e}")
        
        logger.info("Employee data seeding completed!")
        
        # Verify the data
        all_employees = repository.get_all_employees()
        logger.info(f"Total employees in database: {len(all_employees)}")
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to seed employee data: {e}")
        return False


def main():
    """Main entry point for the initialization script."""
    logger.info("=" * 60)
    logger.info("Cosmos DB Employee Database Initialization")
    logger.info("=" * 60)
    
    success = seed_employee_data()
    
    if success:
        logger.info("✓ Initialization completed successfully!")
        sys.exit(0)
    else:
        logger.error("✗ Initialization failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
