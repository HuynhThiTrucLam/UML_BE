from sqlalchemy import Column, Integer, String, ForeignKey,UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class PersonalInforDocument(Base):
    __tablename__ = "personal_infor_documents"
    
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    
    full_name = Column(String)
    date_of_birth = Column(String)  # ISO format date string
    gender = Column(String)
    address = Column(String)

    identity_number = Column(String)
    identity_img_front = Column(String)
    identity_img_back = Column(String)
    avatar = Column(String)

    user = relationship("User", back_populates="personal_documents")
