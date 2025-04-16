from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class StaffCertification(Base):
    __tablename__ = "staff_certifications"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    certification_name = Column(String)
