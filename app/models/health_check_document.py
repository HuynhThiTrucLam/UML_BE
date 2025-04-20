from sqlalchemy import Column, String, ForeignKey, UUID, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.core.database import Base
import uuid
from datetime import datetime

class HealthCheckDocument(Base):
    __tablename__ = "health_check_documents"

    __table_args__ = (
        CheckConstraint("status IN ('registered', 'checked')", name="check_valid_document_status"),
    )

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    health_check_id = Column(PostgresUUID(as_uuid=True), ForeignKey("health_check_schedules.id", ondelete="CASCADE"), nullable=False, index=True)

    document = Column(String, nullable=True)  # Path hoặc tên file upload
    status = Column(String, nullable=False, default="registered")  # registered / checked 

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="health_check_documents")
    health_check = relationship("HealthCheckSchedule", back_populates="health_check_documents", foreign_keys=[health_check_id])
