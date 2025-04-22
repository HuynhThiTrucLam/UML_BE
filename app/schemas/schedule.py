from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class LicenseTypeInfo(BaseModel):
    id: Optional[UUID4]
    type_name: Optional[str]

    model_config = {"from_attributes": True}


class CourseInfo(BaseModel):
    id: Optional[UUID4] = None  # Allow None values
    name: Optional[str] = ""
    
    model_config = {"from_attributes": True}


class InstructorInfo(BaseModel):
    id: Optional[UUID4]
    name: Optional[str]
    # Add other minimal fields you need from Instructor
    
    model_config = {"from_attributes": True}


class ScheduleBase(BaseModel):
    course_id: Optional[UUID4] = None
    exam_id: Optional[UUID4] = None
    start_time: datetime
    end_time: datetime
    location: str
    type: str
    instructor_id: Optional[UUID4] = None
    max_students: int


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(BaseModel):
    id: UUID4
    license_type: Optional[LicenseTypeInfo] = None
    course: Optional[CourseInfo] = None
    instructor: Optional[InstructorInfo] = None

    model_config = {"from_attributes": True}


class ScheduleUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    type: Optional[str] = None
    instructor_id: Optional[UUID4] = None
    max_students: Optional[int] = None

class ScheduleResponse(BaseModel):
    id: UUID4
    course_id: Optional[UUID4] = None
    course_name: Optional[str] = None
    license_type_id: Optional[UUID4] = None
    license_type_name: Optional[str] = None
    exam_id: Optional[UUID4] = None
    start_time: datetime
    end_time: datetime
    location: str
    type: str
    instructor_id: Optional[UUID4] = None
    max_students: int

    model_config = {"from_attributes": True}


class ScheduleList(BaseModel):
    items: List[ScheduleResponse]
    total: int

    model_config = {"from_attributes": True}
