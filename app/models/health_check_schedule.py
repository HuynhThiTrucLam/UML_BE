from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class HealthCheckSchedule(Base):
    __tablename__ = "health_check_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    scheduled_date = Column(DateTime)
    description = Column(String)
