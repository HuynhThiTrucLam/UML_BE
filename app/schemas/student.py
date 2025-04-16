from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    enrollment_number: str
    course_of_study: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentInDB(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Student(StudentInDB):
    pass
