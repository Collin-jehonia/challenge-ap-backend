from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Database connection settings - PostgreSQL only
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost/ium_challenge"
)
print(f"Using DATABASE_URL: {DATABASE_URL}")

# Ensure the DATABASE_URL is for PostgreSQL
if not DATABASE_URL.startswith("postgresql"):
    raise ValueError("Only PostgreSQL database is supported. Please update your DATABASE_URL configuration.")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database, creating tables if they don't exist"""
    Base.metadata.create_all(bind=engine)
