from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String, unique=True)
    license_type_id = Column(Integer, ForeignKey("license_types.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    # Relationships
    license_type = relationship("LicenseType")
    # You can define a relationship with Student if needed
