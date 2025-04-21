from sqlalchemy import Column, String, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    user_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Quan hệ đến User (1-1)
    user = relationship("User", back_populates="student")

    # Quan hệ đến nhiều HealthCheckDocuments
    health_check_documents = relationship(
        "HealthCheckDocument", back_populates="student"
    )
    course_registrations = relationship("CourseRegistration", back_populates="student")
    payments = relationship("Payment", back_populates="student")
