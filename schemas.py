from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentRegistrationBase(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    email: str
    phone: str
    secondary_school: str
    programme: str
    academic_year: int
    registration_date: date

class StudentRegistrationCreate(StudentRegistrationBase):
    pass

class StudentRegistration(StudentRegistrationBase):
    id: int

    class Config:
        orm_mode = True
