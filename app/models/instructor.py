from sqlalchemy import Column, String, Boolean, UUID, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.api import user
from app.core.database import Base
from app.models import certification


class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(
        UUID, ForeignKey("users.id"), index=True, nullable=False
    )  # Fixed: Added ForeignKey constraint

    # One-to-Many: an instructor might have multiple schedules
    user = relationship("User", back_populates="instructor")
    schedules = relationship("Schedule", back_populates="instructor")
