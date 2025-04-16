from sqlalchemy import Column, String, ForeignKey, UUID, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class HealthCheckDocument(Base):
    __tablename__ = "health_check_documents"

    __table_args__ = (
        CheckConstraint("status IN ('registered', 'checked')", name="check_valid_document_status"),
    )

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    student_id = Column(UUID, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    health_check_id = Column(UUID, ForeignKey("health_check_schedules.id", ondelete="CASCADE"), nullable=False, index=True)

    document = Column(String, nullable=False)  # Path hoặc tên file upload
    status = Column(String, nullable=False, default="registered")  # registered / checked

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="health_check_documents")
    health_check = relationship("HealthCheckSchedule", back_populates="health_check_documents")
