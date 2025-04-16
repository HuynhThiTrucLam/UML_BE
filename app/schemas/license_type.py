from pydantic import BaseModel, UUID4, Field
from typing import Optional, List

# Base class with common attributes
class LicenseTypeBase(BaseModel):
    type_name: str = Field(..., example="B1 Car License")
    age_requirement: str = Field(..., example="18 years and above")
    health_requirements: str = Field(..., example="Good vision, no serious health conditions")
    training_duration: int = Field(..., example=30, description="Training duration in days")
    fee: int = Field(..., example=5000000, description="Fee in VND")

# Schema for creating a new license type
class LicenseTypeCreate(LicenseTypeBase):
    pass

# Schema for updating a license type
class LicenseTypeUpdate(BaseModel):
    type_name: Optional[str] = None
    age_requirement: Optional[str] = None
    health_requirements: Optional[str] = None
    training_duration: Optional[int] = None
    fee: Optional[int] = None

# Schema for license type response
class LicenseType(LicenseTypeBase):
    id: UUID4

    class Config:
        orm_mode = True

# Schema for a list of license types
class LicenseTypeList(BaseModel):
    items: List[LicenseType]
    total: int