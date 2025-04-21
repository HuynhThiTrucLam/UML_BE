from sqlalchemy import Column, UUID, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Staff(Base):
    __tablename__ = "staffs"
    
    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    department = Column(String)

    # Relationship back to user
    user = relationship("User", back_populates="staff")
