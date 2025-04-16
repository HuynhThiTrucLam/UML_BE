from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Staff(Base):
    __tablename__ = "staffs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    department = Column(String)
    certification = Column(String)

    # Relationship back to user
    user = relationship("User", back_populates="staff")
