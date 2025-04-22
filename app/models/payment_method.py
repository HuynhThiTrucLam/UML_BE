from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, unique=True)

    # Relationships
    payments = relationship("Payment", back_populates="payment_method")
