from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from app.core.database import Base
import uuid


class LicenseType(Base):
    __tablename__ = "license_types"
    __table_args__ = (
        CheckConstraint('training_duration > 0', name='check_training_duration_positive'),
        CheckConstraint('fee >= 0', name='check_fee_non_negative'),
    )
    
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    type_name = Column(String, unique=True, nullable=False, index=True)
    age_requirement = Column(String, nullable=False)
    health_requirements = Column(String, nullable=False)
    training_duration = Column(Integer, nullable=False)  # sửa chính tả
    fee = Column(Integer, nullable=False)

    # One-to-Many relationship with HealthCheckSchedule
    health_check_schedules = relationship("HealthCheckSchedule", back_populates="license_type")
    # One-to-Many relationship with Course
    courses = relationship("Course", back_populates="license_type")
