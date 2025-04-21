from sqlalchemy import Column, Integer, String, UUID, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import date, datetime

class Course(Base):
    __tablename__ = "courses"

    __table_args__ = (
        CheckConstraint("max_students >= 0", name="check_max_students_positive"),
        CheckConstraint("current_students >= 0", name="check_current_students_positive"),
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("status IN ('active', 'inactive')", name="check_course_status_valid"),
    )

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    course_name = Column(String, index=True, nullable=False)

    license_type_id = Column(UUID, ForeignKey("license_types.id", ondelete="CASCADE"), nullable=False, index=True)

    start_date = Column(Date, nullable=False)  # dùng Date thay vì String để chuẩn hoá
    end_date = Column(Date, nullable=False)

    max_students = Column(Integer, nullable=False)
    current_students = Column(Integer, default=0, nullable=False)

    price = Column(Integer, nullable=False)

    status = Column(String, default="active", nullable=False)

    created_at = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, default=date.today, nullable=False)

    # Relationships
    license_type = relationship("LicenseType", back_populates="courses")
    registrations = relationship("CourseRegistration", back_populates="course")
    health_check_schedules = relationship("HealthCheckSchedule", back_populates="course")
    schedules = relationship("Schedule", back_populates="course")
    