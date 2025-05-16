from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import List, Dict, Any, Optional

from models import StudentRegistration

def get_total_registrations(
    db: Session, 
    year: Optional[int] = None, 
    programme: Optional[str] = None
) -> int:
    """Get the total number of student registrations with optional filters"""
    query = db.query(StudentRegistration)
    
    # Special handling for null year value
    if year is None:
        # No filter, include all records
        pass
    elif year == "null":
        # Filter for null academic_year
        query = query.filter(StudentRegistration.academic_year.is_(None))
    else:
        # Filter for specific year
        query = query.filter(StudentRegistration.academic_year == year)
    
    if programme:
        query = query.filter(StudentRegistration.programme == programme)
        
    return query.count()

def get_registrations_by_programme(db: Session, year: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Get the number of registrations by programme, optionally filtered by year"""
    query = db.query(
        StudentRegistration.programme,
        func.count(StudentRegistration.id).label("count")
    ).group_by(StudentRegistration.programme)
    
    # Special handling for null year value
    if year is None:
        # No filter, include all records
        pass
    elif year == "null":
        # Filter for null academic_year
        query = query.filter(StudentRegistration.academic_year.is_(None))
    else:
        # Filter for specific year
        query = query.filter(StudentRegistration.academic_year == year)
    
    result = query.order_by(desc("count")).limit(limit).all()
    
    return [{"programme": prog, "count": count} for prog, count in result]

def get_registrations_by_year(db: Session, programme: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get the number of registrations by academic year, optionally filtered by programme"""
    query = db.query(
        StudentRegistration.academic_year,
        func.count(StudentRegistration.id).label("count")
    ).group_by(StudentRegistration.academic_year)
    
    if programme:
        query = query.filter(StudentRegistration.programme == programme)
    
    result = query.order_by(StudentRegistration.academic_year).all()
    
    return [{"year": year, "count": count} for year, count in result]

def get_top_schools(
    db: Session, 
    year: Optional[int] = None, 
    programme: Optional[str] = None, 
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Get the top schools by number of registrations, with optional filters"""
    query = db.query(
        StudentRegistration.secondary_school,
        func.count(StudentRegistration.id).label("count")
    ).group_by(StudentRegistration.secondary_school)
    
    # Special handling for null year value
    if year is None:
        # No filter, include all records
        pass
    elif year == "null":
        # Filter for null academic_year
        query = query.filter(StudentRegistration.academic_year.is_(None))
    else:
        # Filter for specific year
        query = query.filter(StudentRegistration.academic_year == year)
    
    if programme:
        query = query.filter(StudentRegistration.programme == programme)
    
    result = query.order_by(desc("count")).limit(limit).all()
    
    return [{"school": school, "count": count} for school, count in result]

def get_registrations(
    db: Session,
    year: Optional[int] = None,
    programme: Optional[str] = None,
    school: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[StudentRegistration]:
    """Get student registrations with optional filters"""
    query = db.query(StudentRegistration)
    
    # Special handling for null year value
    if year is None:
        # No filter, include all records
        pass
    elif year == "null":
        # Filter for null academic_year
        query = query.filter(StudentRegistration.academic_year.is_(None))
    else:
        # Filter for specific year
        query = query.filter(StudentRegistration.academic_year == year)
    
    if programme:
        query = query.filter(StudentRegistration.programme == programme)
    
    if school:
        query = query.filter(StudentRegistration.secondary_school == school)
    
    return query.offset(skip).limit(limit).all()

def get_registrations_by_gender(
    db: Session,
    year: Optional[int] = None,
    programme: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get the number of registrations by gender, with optional filters"""
    query = db.query(
        StudentRegistration.gender,
        func.count(StudentRegistration.id).label("count")
    ).group_by(StudentRegistration.gender)
    
    # Special handling for null year value
    if year is None:
        # No filter, include all records
        pass
    elif year == "null":
        # Filter for null academic_year
        query = query.filter(StudentRegistration.academic_year.is_(None))
    else:
        # Filter for specific year
        query = query.filter(StudentRegistration.academic_year == year)
    
    if programme:
        query = query.filter(StudentRegistration.programme == programme)
    
    result = query.order_by(StudentRegistration.gender).all()
    
    return [{"gender": gender, "count": count} for gender, count in result]

def get_student_records(
    db: Session,
    search: Optional[str] = None,
    year: Optional[int] = None,
    programme: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[StudentRegistration], int]:
    """Get student records with search capability and return total count"""
    query = db.query(StudentRegistration)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentRegistration.first_name.ilike(search_term),
                StudentRegistration.last_name.ilike(search_term),
                StudentRegistration.email.ilike(search_term),
                StudentRegistration.student_id.ilike(search_term),
                StudentRegistration.programme.ilike(search_term)
            )
        )
    
    # Special handling for null year value
    if year is None:
        # No filter, include all records
        pass
    elif year == "null":
        # Filter for null academic_year
        query = query.filter(StudentRegistration.academic_year.is_(None))
    else:
        # Filter for specific year
        query = query.filter(StudentRegistration.academic_year == year)
    
    if programme:
        query = query.filter(StudentRegistration.programme == programme)
    
    # Get total count first
    total = query.count()
    
    # Then apply pagination and return records
    records = query.order_by(StudentRegistration.id).offset(skip).limit(limit).all()
    
    return records, total
