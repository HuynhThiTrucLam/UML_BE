from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.core.database import Base
import uuid
from datetime import datetime


class HealthCheckSchedule(Base):
    __tablename__ = "health_check_schedules"
    __table_args__ = (
        CheckConstraint(
            "scheduled_datetime > CURRENT_TIMESTAMP", name="check_schedule_in_future"
        ),
        CheckConstraint(
            "status IN ('scheduled', 'in_progress', 'completed', 'canceled')",
            name="check_status_valid",
        ),
    )

    id = Column(
        PostgresUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )

    course_id = Column(
        PostgresUUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    address = Column(String, index=True, nullable=False)

    scheduled_datetime = Column(DateTime, nullable=False)
    description = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    status = Column(
        String, nullable=False, default="scheduled"
    )  # scheduled, in_progress, completed, canceled

    # One-to-Many relationship with Course
    course = relationship("Course", back_populates="health_check_schedules")
    # One-to-Many relationship with HealthCheckDocument
    health_check_documents = relationship(
        "HealthCheckDocument", back_populates="health_check"
    )
