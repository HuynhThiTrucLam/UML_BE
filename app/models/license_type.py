from sqlalchemy import Column, Integer, String
from app.core.database import Base

class LicenseType(Base):
    __tablename__ = "license_types"
    
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True)
    description = Column(String)
