import re
from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from app.core.database import Base


class AbsentForm(Base):
    __tablename__ = "absent_forms"

    id = Column(UUID, primary_key=True, index=True)
    object_id = Column(UUID, nullable=True)
    type = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    evidence = Column(String, nullable=True)
