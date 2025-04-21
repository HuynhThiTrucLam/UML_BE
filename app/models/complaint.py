from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from app.core.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    description = Column(String)
