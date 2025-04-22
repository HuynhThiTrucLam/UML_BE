from sqlalchemy import Column, String, Integer, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
import uuid
from app.api import exam
from app.core.database import Base


class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = (
        CheckConstraint(
            "type IN ('theory', 'practice','exam')", name="check_type_of_schedule"
        ),
    )

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    course_id = Column(UUID, ForeignKey("courses.id"), index=True, nullable=True)
    exam_id = Column(
        UUID, ForeignKey("exams.id"), index=True, nullable=True
    )  # Nullable for non-exam schedules
    start_time = Column(String, index=True, nullable=False)  # ISO format time string
    end_time = Column(String, index=True, nullable=False)  # ISO format time string
    location = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)  # e.g., "theory", "practice"
    instructor_id = Column(
        UUID, ForeignKey("instructors.id"), index=True, nullable=True
    )
    max_students = Column(Integer, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="schedules")
    instructor = relationship("Instructor", back_populates="schedules")
    exam = relationship("Exam", back_populates="schedules")