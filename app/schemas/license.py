from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional, List
from datetime import datetime

from app.schemas.license_type import LicenseType


class LicenseBase(BaseModel):
    license_number: str = Field(..., example="DL12345678")
    license_type_id: int = Field(..., example=1)
    student_id: int = Field(..., example=1)
    expiration_date: datetime = Field(..., example="2026-04-22T00:00:00")
    status: str = Field(..., example="active")

    @field_validator("status")
    def status_must_be_valid(cls, v):
        valid_statuses = ["active", "expired", "suspended", "revoked"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    license_number: Optional[str] = None
    license_type_id: Optional[int] = None
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
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class LicenseList(BaseModel):
    items: List[License]
    total: int