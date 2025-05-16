"""
Setup script for initializing the PostgreSQL database and loading sample data.
Usage: python setup.py
"""

import os
import sys
import subprocess
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from database import Base, SessionLocal, init_db, DATABASE_URL
from models import StudentRegistration
from load_data import load_sample_data

def check_postgres_db_exists():
    """Check if the PostgreSQL database exists and create it if it doesn't"""
    # Extract database name from the URL
    db_name = DATABASE_URL.split('/')[-1]
    
    try:
        # Try to create the database (will fail if it already exists, which is fine)
        process = subprocess.run(
            ['createdb', db_name],
            capture_output=True,
            text=True
        )
        
        # If the database was created successfully
        if process.returncode == 0:
            print(f"PostgreSQL database '{db_name}' created successfully.")
            return True
        
        # If the database already exists, that's fine
        if "already exists" in process.stderr:
            print(f"PostgreSQL database '{db_name}' already exists.")
            return True
        
        # Other error
        print(f"Error creating PostgreSQL database: {process.stderr}")
        return False
        
    except Exception as e:
        print(f"Error checking PostgreSQL database: {str(e)}")
        print("Make sure PostgreSQL is installed and running.")
        return False

def setup_database():
    """Set up the PostgreSQL database, create tables, and load sample data"""
    print("Setting up the PostgreSQL database...")
    
    print("Using PostgreSQL database.")
    if not check_postgres_db_exists():
        print("\nTroubleshooting PostgreSQL connection:")
        print("1. Make sure PostgreSQL is installed and running")
        print("2. Check if PostgreSQL user has appropriate permissions")
        print("3. You can manually create the database with: createdb ium_challenge")
        return False
    
    try:
        # Initialize the database (creates tables if they don't exist)
        init_db()
        print("Database tables created successfully.")
        
        # Create a database session
        db = SessionLocal()
        
        try:
            # Check if data already exists
            existing_count = db.query(StudentRegistration).count()
            if existing_count > 0:
                print(f"Database already contains {existing_count} records. Skipping data load.")
            else:
                # Load sample data
                print("Loading sample data...")
                load_sample_data(db)
                print("Sample data loaded successfully.")
        finally:
            db.close()
        
        print("\nSetup completed successfully!")
        print("To start the API server, run: uvicorn main:app --reload")
        
        return True
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have the required packages installed: pip install -r requirements.txt")
        print("2. Check your database connection settings in .env file")
        print("3. Ensure the PostgreSQL server is running and user has appropriate permissions")
        
        return False

if __name__ == "__main__":
    # Execute setup
    success = setup_database()
    sys.exit(0 if success else 1) 