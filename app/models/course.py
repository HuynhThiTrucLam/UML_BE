from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)
    description = Column(String)
