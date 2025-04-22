from typing import List
from fastapi import APIRouter, Query
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from sqlalchemy.orm import Session
from app.crud import payment as crud
from app.crud.course_registration import get_course_registration_by_id
from app.schemas.payment import PaymentCreate, PaymentUpdate, Payment, PaymentList
from app.api.deps import get_db, require_roles

router = APIRouter()

#List all payments
@router.get("/", response_model=PaymentList)
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_payments(db=db, skip=skip, limit=limit)

# # Get list payments by identity_number
# @router.get("/{payment_id}", response_model=PaymentList)
# def get_payment(
#     identity_number: uuid.UUID,
#     db: Session = Depends(get_db),
# ):
#     payments = crud.get_payment_by_indentity_number(db=db, identity_number=identity_number)
#     return payments


#create a new payment
@router.post("/", response_model=Payment)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
):
    exist_course_registration = get_course_registration_by_id(
        db=db, course_registration_id=payment.course_registration_id
    )
    if not exist_course_registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course registration not found",
        )
    return crud.create_payment(db=db, payment=payment)
