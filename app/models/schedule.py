from sqlalchemy import Column, String, Integer, UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    course_id = Column(UUID, index=True, nullable=False)
    schedule_datetime = Column(String, index=True, nullable=False)  # ISO format date string
    start_time = Column(String, index=True, nullable=False)  # ISO format time string
    end_time = Column(String, index=True, nullable=False)  # ISO format time string
    location = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)  # e.g., "theory", "practice"
    instructor_id = Column(UUID, index=True, nullable=False)  # ID of the instructor teaching the course
    vehicle_id = Column(UUID, index=True, nullable=False)  # ID of the vehicle used for the course
    max_students = Column(Integer, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="schedules")
    instructor = relationship("Teacher", back_populates="schedules")
    vehicle = relationship("Vehicle", back_populates="schedules")