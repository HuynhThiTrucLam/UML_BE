from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date

from app.api import course
from app.models import instructor
from app.schemas.course import Course


class LicenseTypeInfo(BaseModel):
    id: Optional[UUID4]
    type_name: Optional[str]

    model_config = {"from_attributes": True}


class ScheduleBase(BaseModel):
    course_id: Optional[UUID4]
    start_time: datetime
    end_time: datetime
    location: str
    type: str
    instructor_id: Optional[str]
    max_students: int
    course: Optional[Dict] = None


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: UUID4
    license_type: Optional[LicenseTypeInfo] = None

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


class ScheduleUpdate(BaseModel):
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str]
    type: Optional[str]
    instructor_id: Optional[str]
    max_students: Optional[int]


class ScheduleList(BaseModel):
    items: List[Schedule]
    total: int

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}
