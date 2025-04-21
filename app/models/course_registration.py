from sqlalchemy import Column, String, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from app.core.database import Base
from app.models import schedule  # Ensure you import Base from the correct module


class CourseRegistration(Base):
    __tablename__ = "course_registrations"


    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved','payment','successful', 'rejected')",
            name="check_status_valid"
        ),
    )
    
    id = Column(UUID, primary_key=True, index=True)
    student_id = Column(UUID, ForeignKey("students.id"))
    course_id = Column(UUID, ForeignKey("courses.id"))

    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    note = Column(String)

    # Relationships
    student = relationship("Student", back_populates="course_registrations")
    course = relationship("Course", back_populates="registrations")
    payments = relationship("Payment", back_populates="course_registration")
