from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class PracticeClass(Base):
    __tablename__ = "practice_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    scheduled_time = Column(DateTime)
