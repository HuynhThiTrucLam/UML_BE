from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String, unique=True)
    model = Column(String)
