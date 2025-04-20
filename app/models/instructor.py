from sqlalchemy import Column, String, Boolean, UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Instructor(Base):
    __tablename__ = "instructors"
    
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, index=True, nullable=False)  # ID of the user who is an instructor
    
    certification = Column(String, index=True, nullable=False)  # Instructor certification details
    
    # One-to-Many: an instructor might have multiple schedules
    schedules = relationship("Schedule", back_populates="instructor")