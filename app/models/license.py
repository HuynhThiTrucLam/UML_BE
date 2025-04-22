from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String, unique=True)
    license_type_id = Column(Integer, ForeignKey("license_types.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime)
    status = Column(String)  # e.g., "active", "expired", etc.

    # Relationships
    license_type = relationship("LicenseType")
    student = relationship("Student")
