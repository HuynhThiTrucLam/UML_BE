from uuid import UUID
from sqlalchemy import Column, UUID, String, ForeignKey
from app.api import user
from app.core.database import Base
from sqlalchemy.orm import relationship

class Certification(Base):
    __tablename__ = "certifications"
    
    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    certification_url = Column(String)

    #relationships with user
    user = relationship("User", back_populates="certifications")

