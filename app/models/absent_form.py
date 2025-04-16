from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class AbsentForm(Base):
    __tablename__ = "absent_forms"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    reason = Column(String)
