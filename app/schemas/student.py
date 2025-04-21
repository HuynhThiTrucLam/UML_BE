from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class StudentBase(BaseModel):
    user_id: UUID4


class StudentCreate(StudentBase):
    pass


class StudentInDB(StudentBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime

    class Config:
        orm_mode = True


class Student(StudentInDB):
    pass
