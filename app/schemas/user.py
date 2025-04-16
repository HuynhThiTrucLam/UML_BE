from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a user
class UserCreate(UserBase):
    password: str
    role: str

# Schema for updating a user
class UserUpdate(UserBase):
    is_active: Optional[bool] = True

# Schema for DB model
class UserInDBBase(UserBase):
    id: UUID4
    is_active: bool
    role: str

    class Config:
        orm_mode = True

# Response schema
class User(UserInDBBase):
    pass
