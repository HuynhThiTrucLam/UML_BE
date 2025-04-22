from sqlalchemy.orm import Session
from app.models.payment_method import PaymentMethod
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodList
import uuid
from typing import List, Optional

def get_payment_method_by_id(db: Session, payment_method_id: uuid.UUID) -> Optional[PaymentMethod]:
    return db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()

def get_payment_method_by_name(db: Session, name_in: str) -> Optional[PaymentMethod]:
    return db.query(PaymentMethod).filter(PaymentMethod.method == name_in).first()

def get_payment_methods(db: Session, skip: int = 0, limit: int = 100) -> PaymentMethodList:
    payment_methods = db.query(PaymentMethod).offset(skip).limit(limit).all()
    total = db.query(PaymentMethod).count()
    return PaymentMethodList(payment_methods=payment_methods, total=total)

def create_payment_method(db: Session, payment_method: PaymentMethodCreate) -> PaymentMethod:
    db_payment_method = PaymentMethod(
        id=uuid.uuid4(),
        method=payment_method.method,
    )
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method

def update_payment_method(db: Session, payment_method: PaymentMethodUpdate) -> Optional[PaymentMethod]:
    db_payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment_method.id).first()
    if db_payment_method:
        db_payment_method.method = payment_method.method
        db.commit()
        db.refresh(db_payment_method)
        return db_payment_method
    return None

def delete_payment_method(db: Session, payment_method_id: uuid.UUID) -> bool:
    """
    Delete a payment method by ID
    
    Args:
        db: Database session
        payment_method_id: UUID of the payment method to delete
        
    Returns:
        bool: True if deletion was successful, False if payment method not found
    """
    try:
        result = db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).delete()
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        raise e