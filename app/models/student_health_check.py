from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class StudentHealthCheck(Base):
    __tablename__ = "student_health_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(String)
    remarks = Column(String)

    # Relationship to Student can be defined here
