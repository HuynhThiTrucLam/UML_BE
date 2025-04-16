from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class HealthCheckSchedule(Base):
    __tablename__ = "health_check_schedules"
    __table_args__ = (
        CheckConstraint("scheduled_datetime > CURRENT_TIMESTAMP", name="check_schedule_in_future"),
    )

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    license_type_id = Column(UUID, ForeignKey("license_types.id"), nullable=False, index=True)

    address = Column(String, index=True, nullable=False)
    
    scheduled_datetime = Column(DateTime, nullable=False)  
    description = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # One-to-Many relationship with LicenseType
    license_type = relationship("LicenseType", back_populates="health_check_schedules")
    # One-to-Many relationship with HealthCheckDocument
    health_check_documents = relationship("HealthCheckDocument", back_populates="health_check")