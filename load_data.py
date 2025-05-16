
import json
import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import StudentRegistration

def load_mock_data(db: Session):
    # Load mock data from JSON file
    try:
        with open("mock_student_data.json", "r") as f:
            data = json.load(f)
        
        # Insert data into the database
        for record in data:
            # Parse registration date from string to datetime
            try:
                if record.get('registration_date'):
                    month, day, year = map(int, record['registration_date'].split('/'))
                    registration_date = datetime.date(year, month, day)
                else:
                    registration_date = None
            except Exception as e:
                print(f"Error parsing date for record {record['id']}: {e}")
                registration_date = None
            
            # Create new student registration record
            registration = StudentRegistration(
                student_id=record.get('student_id'),
                first_name=record.get('first_name'),
                last_name=record.get('last_name'),
                gender=record.get('gender'),
                email=record.get('email'),
                secondary_school=record.get('secondary_school'),
                programme=record.get('study_programme'),
                academic_year=record.get('academic_year'),
                registration_date=registration_date
            )
            db.add(registration)
        
        db.commit()
        print(f"Loaded {len(data)} mock registrations into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error loading mock data: {e}")

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Create a new session
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_count = db.query(StudentRegistration).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} records. Skipping data load.")
        else:
            load_mock_data(db)
    finally:
        db.close()
