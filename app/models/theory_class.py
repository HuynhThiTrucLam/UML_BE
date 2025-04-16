from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class TheoryClass(Base):
    __tablename__ = "theory_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    scheduled_time = Column(DateTime)
