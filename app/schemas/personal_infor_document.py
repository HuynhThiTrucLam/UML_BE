from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional, List
from datetime import datetime, date

class PersonalInformationDocumentBase(BaseModel):
    user_id: UUID4
    full_name: str
    date_of_birth: date
    gender: str
    address: str
    email: Optional[str] = None
    phone_number: Optional[str] = None

    identity_number: str
    identity_img_front: str
    identity_img_back: str
    avatar: str
    
    @field_validator('date_of_birth', mode='before')
    @classmethod
    def validate_date_of_birth(cls, value):
        """Validate date_of_birth format."""
        if isinstance(value, str):
            try:
                # Fix possible typos in year (like 20004 instead of 2004)
                parts = value.split('-')
                if len(parts) == 3 and len(parts[0]) > 4:
                    parts[0] = parts[0][-4:]  # Keep only last 4 digits of year
                    value = '-'.join(parts)
                
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Date must be in format YYYY-MM-DD")
        return value

class PersonalInformationDocumentCreate(PersonalInformationDocumentBase):
    pass

class PersonalInformationDocumentUpdate(PersonalInformationDocumentBase):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    identity_number: Optional[str] = None
    identity_img_front: Optional[str] = None
    identity_img_back: Optional[str] = None
    avatar: Optional[str] = None


class PersonalInformationDocument(PersonalInformationDocumentBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }
    }


