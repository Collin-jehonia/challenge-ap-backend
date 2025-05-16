from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from contextlib import asynccontextmanager
import os

from database import get_db, init_db, SessionLocal
from models import StudentRegistration
import schemas
from repositories import registration_repository
from load_data import load_mock_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    
    # Load mock data if database is empty
    db = SessionLocal()
    try:
        existing_count = db.query(StudentRegistration).count()
        if existing_count == 0:
            print("Database is empty. Loading mock data...")
            load_mock_data(db)
        else:
            print(f"Database already contains {existing_count} records. Skipping data load.")
    finally:
        db.close()
        
    yield

app = FastAPI(
    title="IUM Student Registration API",
    description="API for the International University of Management student registration dashboard",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"}
    )

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Student Registration Dashboard API"}

# Get total registrations
@app.get("/api/total-registrations", 
         response_model=Dict[str, int],
         summary="Get total registrations",
         description="Returns the total number of student registrations, optionally filtered by year or programme")
def get_total_registrations(
    year: int = None,
    programme: str = None,
    db: Session = Depends(get_db)
):
    total = registration_repository.get_total_registrations(db, year, programme)
    return {"total": total}

# Get registrations by programme
@app.get("/api/registrations-by-programme", 
         response_model=List[Dict[str, Any]],
         summary="Get registrations by programme",
         description="Returns the count of registrations grouped by programme, optionally filtered by year")
def get_registrations_by_programme(
    year: int = None, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    data = registration_repository.get_registrations_by_programme(db, year, limit)
    return data

# Get registrations by academic year
@app.get("/api/registrations-by-year", 
         response_model=List[Dict[str, Any]],
         summary="Get registrations by year",
         description="Returns the count of registrations grouped by academic year, optionally filtered by programme")
def get_registrations_by_year(
    programme: str = None,
    db: Session = Depends(get_db)
):
    data = registration_repository.get_registrations_by_year(db, programme)
    return data

# Get top schools by number of students
@app.get("/api/top-schools", 
         response_model=List[Dict[str, Any]],
         summary="Get top schools",
         description="Returns the top schools by number of registrations, optionally filtered by year or programme")
def get_top_schools(
    year: int = None,
    programme: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    data = registration_repository.get_top_schools(db, year, programme, limit)
    return data

# Get all registrations (with optional filters)
@app.get("/api/registrations", 
         response_model=List[schemas.StudentRegistration],
         summary="Get student registrations",
         description="Returns a list of student registrations with various filter options")
def get_registrations(
    year: int = None,
    programme: str = None,
    school: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    registrations = registration_repository.get_registrations(
        db, year, programme, school, skip, limit
    )
    return registrations

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
