from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
