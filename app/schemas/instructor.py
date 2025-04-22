import uuid
from pydantic import BaseModel
from app.schemas.user import UserBase


class Instructor(BaseModel):
    id: uuid.UUID


class InstructorResponse(Instructor):
    user: UserBase
