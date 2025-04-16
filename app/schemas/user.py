from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional
from datetime import datetime


# Shared fields across all schemas
class UserBase(BaseModel):
    user_name: str = Field(..., example="admin")

    email: EmailStr = Field(..., example="admin@example.com")
    role: str = Field(..., example="admin")
    phone_number: str = Field(..., example="0366400874")

class UserLogin(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")
    
# Schema used when creating a user (request body)
class UserCreate(UserBase):
    password: str = Field(..., example="admin123")  # Raw password (will be hashed in backend)

# Schema used for updating a user``
class UserUpdate(BaseModel):
    user_name: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    phone_number: Optional[str]
    is_active: Optional[bool]
    password: Optional[str]  # Plain password, to re-hash


# Schema used internally and in responses
class UserInDBBase(UserBase):
    id: UUID4
    hashed_password: str
    created_at: str

    class Config:
        orm_mode = True


# Final schema used for API responses
class User(UserInDBBase):
    pass
