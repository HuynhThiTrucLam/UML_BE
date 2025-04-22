import datetime
from sqlalchemy.orm import Session
from app.schemas.payment import PaymentCreate, PaymentUpdate, Payment
from app.models.payment import Payment as PaymentModel
import uuid
from datetime import date


#List all payments
def get_payments(db: Session, skip: int = 0, limit: int = 100):
    payments = db.query(PaymentModel).offset(skip).limit(limit).all()
    return payments


#Create a new payment
def create_payment(db: Session, payment: PaymentCreate):
    db_payment = PaymentModel(
        id=uuid.uuid4(),
        amount=0.0,
        payment_method_id=payment.payment_method_id,
        evidence=payment.evidence,
        course_registration_id=payment.course_registration_id,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


#get a payment by identity_number in the course_registration join