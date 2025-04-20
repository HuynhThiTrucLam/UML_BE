from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional
from datetime import date

# Base class with common attributes
class CourseBase(BaseModel):
    course_name: str = Field(..., example="B1 Driving Course")
    license_type_id: UUID4 = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    start_date: date = Field(..., example="2025-05-01")
    end_date: date = Field(..., example="2025-06-30")
    max_students: int = Field(..., example=30)
    price: int = Field(..., example=5000000)
    status: str = Field("active", example="active")

    @field_validator('status')
    def status_must_be_valid(cls, v):
        if v not in ["active", "inactive"]:
            raise ValueError('Status must be either "active" or "inactive"')
        return v

    @field_validator('end_date')
    def end_date_must_be_after_start_date(cls, v, info):
        values = info.data
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

# Schema for creating a new course
class CourseCreate(CourseBase):
    pass

# Schema for updating a course
class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    license_type_id: Optional[UUID4] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    max_students: Optional[int] = None
    current_students: Optional[int] = None
    price: Optional[int] = None
    status: Optional[str] = None

    @field_validator('status')
    def status_must_be_valid(cls, v):
        if v is None:
            return v
        if v not in ["active", "inactive"]:
            raise ValueError('Status must be either "active" or "inactive"')
        return v

# Schema for course response
class Course(CourseBase):
    id: UUID4
    current_students: int
    created_at: date
    updated_at: date

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

# Schema for a list of courses
class CourseList(BaseModel):
    items: list[Course]
    total: int

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }