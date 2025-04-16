from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class VehicleMaintenance(Base):
    __tablename__ = "vehicle_maintenance"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    maintenance_date = Column(DateTime)
    description = Column(String)
