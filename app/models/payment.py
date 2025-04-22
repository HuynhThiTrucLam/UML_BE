from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, Date, String, Float, ForeignKey, Integer
from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID, primary_key=True, index=True)
    amount = Column(Float)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    evidence = Column(String)
    course_registration_id = Column(UUID, ForeignKey("course_registrations.id"))
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date)

    # relationships
    payment_method = relationship("PaymentMethod", back_populates="payments")
    course_registration = relationship("CourseRegistration", back_populates="payments")
