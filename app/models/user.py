from sqlalchemy import Column, String, Boolean, UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_name = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    phone_number = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)  # e.g., "student", "staff", "admin", "teacher"
    created_at = Column(String, nullable=False)  # ISO format date string

    # One-to-One relationships
    student = relationship("Student", back_populates="user", uselist=False)
    staff = relationship("Staff", back_populates="user", uselist=False)
    
    # One-to-Many: a user might have multiple personal documents
    personal_documents = relationship("PersonalInforDocument", back_populates="user")
