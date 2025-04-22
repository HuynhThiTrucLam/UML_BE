import sched
import uuid
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, UUID
from app.core.database import Base
from sqlalchemy.orm import relationship


# -- Bảng Exams: Đại diện cho một bài thi
# CREATE TABLE exams (
#     exam_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
#     course_id UUID NOT NULL,
#     type VARCHAR(20) CHECK (type IN ('theory', 'practice')),

#     CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses(id)
# );

class Exam(Base):
    __tablename__ = "exams"

    id = Column( UUID,
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )
    course_id= Column(UUID, ForeignKey("courses.id"), nullable=False)
    type = Column(String(20), nullable=False)

    #relationship
    exam_results = relationship("ExamResult", back_populates="exam")
    course = relationship("Course", back_populates="exams")
    schedules = relationship("Schedule", back_populates="exam")