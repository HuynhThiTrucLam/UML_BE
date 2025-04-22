from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Double
from app.core.database import Base
from sqlalchemy.orm import relationship

class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(UUID, primary_key=True, index=True)
    exam_id = Column(UUID, ForeignKey("exams.id"))
    student_id = Column(UUID, ForeignKey("students.id"))
    score = Column(Double, nullable=False)

    #relationships
    exam = relationship("Exam", back_populates="exam_results")
    student = relationship("Student", back_populates="exam_results")
