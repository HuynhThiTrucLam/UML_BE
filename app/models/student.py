from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    enrollment_number = Column(String, unique=True, index=True)
    course_of_study = Column(String)

    # Relationship back to user
    user = relationship("User", back_populates="student")
