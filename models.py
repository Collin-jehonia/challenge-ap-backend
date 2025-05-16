from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class StudentRegistration(Base):
    __tablename__ = "student_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    email = Column(String)
    secondary_school = Column(String, index=True)
    programme = Column(String, index=True)
    academic_year = Column(Integer, index=True)
    registration_date = Column(Date)
