from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional, List, Union
from datetime import datetime

from app.schemas.license_type import LicenseType


class LicenseBase(BaseModel):
    license_number: str = Field(..., example="DL12345678")
    license_type_id: UUID4 = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    student_id: UUID4 = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    expiration_date: Optional[datetime] = Field(None, example="2026-04-22T00:00:00")
    status: Optional[str] = Field(None, example="active")

    @field_validator("status")
    def status_must_be_valid(cls, v):
        if v is None:
            return v
        valid_statuses = ["active", "expired", "suspended", "revoked"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    license_number: Optional[str] = None
    license_type_id: Optional[UUID4] = None
    expiration_date: Optional[datetime] = None
    status: Optional[str] = None

    @field_validator("status")
    def status_must_be_valid(cls, v):
        if v is None:
            return v
        valid_statuses = ["active", "expired", "suspended", "revoked"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v


class License(LicenseBase):
    id: UUID4
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            UUID4: lambda v: str(v),
        }
    }


class LicenseList(BaseModel):
    items: List[License]
    total: int
    
    model_config = {
        "from_attributes": True,
        "json_encoders": {
            UUID4: lambda v: str(v),
        }
    }