from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional, List
from datetime import datetime, date

class HealthCheckScheduleBase(BaseModel):
    course_id: UUID4 = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    address: str = Field(..., example="123 Main St, City, Country")
    scheduled_datetime: datetime = Field(..., example="2025-05-01T10:00:00Z")
    description: str = Field(None, example="Annual health check")
    status: str = Field(..., example="scheduled")
    created_at: date
    updated_at: date

class HealthCheckScheduleCreate(BaseModel):
    course_id: UUID4 = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    address: str = Field(..., example="123 Main St, City, Country")
    scheduled_datetime: datetime = Field(..., example="2025-05-01T10:00:00Z")
    description: Optional[str] = Field(None, example="Annual health check")
    status: str = Field("scheduled", example="scheduled")
    
    @field_validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['scheduled', 'in_progress', 'completed', 'canceled']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

class HealthCheckScheduleUpdate(BaseModel):

    course_id: Optional[UUID4] = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    address: Optional[str] = Field(None, example="123 Main St, City, Country")
    scheduled_datetime: Optional[datetime] = Field(None, example="2025-05-01T10:00:00Z")
    description: Optional[str] = Field(None, example="Annual health check")
    status: Optional[str] = Field(None, example="in_progress")
    
    @field_validator('status')
    def validate_status(cls, v):
        if v is None:
            return v
        allowed_statuses = ['scheduled', 'in_progress', 'completed', 'canceled']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

# Schema for course response
class HealthCheckSchedule(HealthCheckScheduleBase):
    id: UUID4

    class Config:
        from_attributes = True
    
# Schema for health check schedule list response
class HealthCheckScheduleList(BaseModel):
    items: List[HealthCheckSchedule]
    total: int
    
    class Config:
        from_attributes = True

