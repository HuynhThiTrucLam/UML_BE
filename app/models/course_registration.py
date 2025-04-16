from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class CourseRegistration(Base):
    __tablename__ = "course_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
