from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime, date

from app.schemas.health_check_schedule import HealthCheckSchedule


class HealthCheckDocumentBase(BaseModel):
    """
    HealthCheckDocument is a Pydantic model that represents the health check document.
    It includes fields for the status, timestamp, and any errors encountered during the health check.
    """

    student_id: UUID4 = Field(
        ..., description="The ID of the student associated with the health check."
    )
    health_check_id: UUID4 = Field(..., description="The ID of the health check.")

    document: str = Field(..., description="The link of the health check document.")
    status: str = Field(..., description="The status of the health check document.")


class HealthCheckDocumentCreate(BaseModel):
    """
    HealthCheckDocumentCreate is a Pydantic model that represents the creation of a health check document.
    It inherits from HealthCheckDocumentBase and includes additional fields for the creation process.
    """

    student_id: UUID4 = Field(
        ..., description="The ID of the student associated with the health check."
    )
    health_check_id: UUID4 = Field(..., description="The ID of the health check.")
    status: str = Field(..., description="The status of the health check document.")
    document: str = Field(..., description="The link of the health check document.")


class HealthCheckDocumentUpdate(BaseModel):
    """
    HealthCheckDocumentUpdate is a Pydantic model that represents the update of a health check document.
    It inherits from HealthCheckDocumentBase and includes additional fields for the update process.
    """

    health_check_id: UUID4 = Field(..., description="The ID of the health check.")
    document: str = Field(..., description="The link of the health check document.")
    status: str = Field(..., description="The status of the health check document.")


class HealthCheckDocument(HealthCheckDocumentBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    health_check: Optional[HealthCheckSchedule] = None
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
        },
    }


class HealthCheckDocumentList(BaseModel):
    items: List[HealthCheckDocument]
    total: int

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}
