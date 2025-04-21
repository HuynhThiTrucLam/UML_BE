from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String)
    scheduled_time = Column(DateTime)
