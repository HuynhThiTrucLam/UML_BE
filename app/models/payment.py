from uuid import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, String, Float, ForeignKey, Integer
from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID, primary_key=True, index=True)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    student_id = Column(UUID, ForeignKey("students.id"))
    amount = Column(Float)
    course_registration_id = Column(UUID, ForeignKey("course_registrations.id"))

    # relationships
    payment_method = relationship("PaymentMethod", back_populates="payments")
    student = relationship("Student", back_populates="payments")
    course_registration = relationship("CourseRegistration", back_populates="payments")
