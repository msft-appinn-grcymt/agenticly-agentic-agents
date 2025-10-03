#!/usr/bin/env python
"""
Database Seeding Script
Seeds employee data into Cosmos DB
"""
import os
import sys
from cosmos_repository import employee_repository, FALLBACK_EMPLOYEES

def seed_employees():
    """Seed employee data into Cosmos DB"""
    
    # Check if Cosmos DB is enabled
    use_cosmos = os.getenv("USE_COSMOS_DB", "false").lower() == "true"
    
    if not use_cosmos:
        print("❌ USE_COSMOS_DB is not set to 'true'")
        print("   Set USE_COSMOS_DB=true in your .env file to seed Cosmos DB")
        print("   Current mode: Using in-memory fallback data")
        return False
    
    container = employee_repository.container
    if container is None:
        print("❌ Failed to connect to Cosmos DB")
        print("   Please check your COSMOS_ENDPOINT and COSMOS_KEY environment variables")
        return False
    
    print("🚀 Starting database seed...")
    print(f"   Database: {os.getenv('COSMOS_DATABASE_NAME', 'employees-db')}")
    print(f"   Container: {os.getenv('COSMOS_CONTAINER_NAME', 'employees')}")
    print()
    
    success_count = 0
    error_count = 0
    
    for employee_data in FALLBACK_EMPLOYEES.values():
        try:
            # Create employee in Cosmos DB
            employee_repository.create_employee(employee_data)
            print(f"✅ Created: {employee_data['full_name']} - {employee_data['role']}")
            success_count += 1
        except Exception as e:
            # If item already exists, try to update it
            try:
                # For simplicity, we'll just skip existing items
                print(f"⚠️  Skipped: {employee_data['full_name']} (may already exist)")
            except Exception as update_error:
                print(f"❌ Error: {employee_data['full_name']} - {update_error}")
                error_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Successfully seeded: {success_count} employees")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    print("=" * 60)
    
    return error_count == 0


def verify_data():
    """Verify seeded data"""
    print("\n🔍 Verifying seeded data...")
    
    try:
        all_employees = employee_repository.get_all_employees()
        print(f"   Total employees in database: {len(all_employees)}")
        
        if len(all_employees) == 0:
            print("   ⚠️  No employees found. Database may be empty.")
            return False
        
        print("\n📋 Employee List:")
        for emp in all_employees:
            print(f"   • {emp['full_name']}: {emp['role']}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error verifying data: {e}")
        return False


def main():
    """Main function"""
    print()
    print("=" * 60)
    print("  Employee Database Seeding Script")
    print("=" * 60)
    print()
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded from .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment")
    except Exception as e:
        print(f"⚠️  Could not load .env file: {e}")
    
    print()
    
    # Seed the database
    success = seed_employees()
    
    if success:
        # Verify the data
        verify_data()
        print("\n🎉 Database seeding completed successfully!")
        return 0
    else:
        print("\n⚠️  Database seeding completed with warnings")
        print("   If using fallback mode, no action is required.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
