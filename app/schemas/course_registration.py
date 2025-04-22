import datetime
from re import U
from pydantic import BaseModel, UUID4, Field, field_validator
from typing import List, Optional, Any, Dict
from datetime import date

# Fix the imports - import crud module instead of API routes
from app.crud import course as course_crud
from app.crud import health_check_schedule as health_check_schedule_crud
from app.crud import license_type as license_type_crud
from sqlalchemy.orm import Session
from app.api.deps import get_db

# Import Pydantic schemas instead of SQLAlchemy models
from app.schemas.health_check_document import (
    HealthCheckDocument as HealthCheckDocSchema,
)
from app.schemas.course import Course as CourseSchema
from app.schemas.personal_infor_document import (
    PersonalInformationDocument as PersonalDocSchema,
)
from app.schemas.student import Student as StudentSchema


class CourseRegistrationCreate(BaseModel):
    identity_number: str
    full_name: str
    gender: str
    phone_number: str
    date_of_birth: date
    address: str
    email: Optional[str] = None
    license_type_id: UUID4
    identity_image_front: str
    identity_image_back: str
    avatar: str
    course_id: UUID4
    health_check_schedule_id: UUID4
    role: str

    @field_validator("course_id")
    def validate_course_id(cls, v):
        db = next(get_db())
        course = course_crud.get_course(db, course_id=v)
        if not course:
            raise ValueError(f"Course with ID {v} does not exist")
        return v

    @field_validator("health_check_schedule_id")
    def validate_health_check_schedule_id(cls, v):
        db = next(get_db())
        health_check = health_check_schedule_crud.get_health_check_schedule(
            db, health_check_schedule_id=v
        )
        if not health_check:
            raise ValueError(f"Health check schedule with ID {v} does not exist")
        return v

    @field_validator("license_type_id")
    def validate_license_type_id(cls, v):
        # Use dependency injection to get db and then use the crud function
        db = next(get_db())
        license_type = license_type_crud.get_license_type_by_id(db, license_type_id=v)
        if not license_type:
            raise ValueError(f"License type with ID {v} does not exist")
        return v


class CourseRegistrationUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


# Response
class CourseRegistration(BaseModel):
    id: UUID4

    # Use Pydantic schema models instead of SQLAlchemy models
    health_check_doc: Optional[HealthCheckDocSchema] = None
    course: Optional[CourseSchema] = None
    personal_doc: Optional[PersonalDocSchema] = None
    student: Optional[StudentSchema] = None

    status: str
    created_at: datetime
    updated_at: datetime

    note: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
    }


class CoursePersonalData(BaseModel):
    name: str
    identityNumber: str
    address: str
    phone: str
    gender: str
    birthDate: str
    licenseType: str
    email: str
    healthCheckDocURL: str


class PersonalImgData(BaseModel):
    avatar: str
    cardImgFront: str
    cardImgBack: str


class CourseType(BaseModel):
    id: str
    name: str
    licenseTypeId: str
    examDate: str
    startDate: str
    endDate: str
    registeredCount: int
    maxStudents: int


class HealthCheckType(BaseModel):
    id: str
    name: str
    date: str
    address: str
    courseId: str


class ChooseData(BaseModel):
    course: CourseType
    healthCheck: HealthCheckType


class CourseStudent(BaseModel):
    personalData: CoursePersonalData
    personalImgData: PersonalImgData
    chooseData: ChooseData

    class Config:
        orm_mode = True


class TypeOfLicense(BaseModel):
    id: str
    name: str


class ScheduleType(BaseModel):
    id: str
    courseId: str
    typeOfLicense: TypeOfLicense
    type: str
    startTime: str
    endTime: str
    location: str
    teacher: Optional[str] = None

class CourseRegistrationResponse(BaseModel):
    id: UUID4
    method: str
    registrationDate: str
    status: str
    studentInfor: CourseStudent
    scheduleInfor: list[ScheduleType]
    scoreOverall: Optional[str] = None
    receiveDate: Optional[str] = None
    location: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
    }
