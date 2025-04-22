from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api.deps import get_db, get_current_active_user, require_roles
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodList
from app.crud import payment_method as crud

router = APIRouter()


@router.get(
    "/payment-methods/",
    response_model=PaymentMethodList,
)
def list_payment_methods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db),
):
    payment_methods = crud.get_payment_methods(db, skip=skip, limit=limit)
    return payment_methods

#create payment method
@router.post("/", response_model=PaymentMethodCreate, status_code=status.HTTP_201_CREATED)
def create_payment_method(
    payment_method: PaymentMethodCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),  # Only admin can create
):
    existing_license_type = crud.get_payment_method_by_name(db, name_in=payment_method.method)
    if existing_license_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment method already exists"
        )

    return crud.create_payment_method(db=db, payment_method=payment_method)

#update payment method
@router.put(
    "/{payment_method_id}",
    response_model=PaymentMethodUpdate,
)
def update_payment_method(
    payment_method: PaymentMethodUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),  # Only admin can update
):
    existing_payment_method = crud.get_payment_method_by_id(db, payment_method_id=payment_method.id)
    if not existing_payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )

    return crud.update_payment_method(db=db, payment_method=payment_method)

#delete payment method
# @router.delete(
#     "/{payment_method_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_payment_method(
#     payment_method_id: uuid.UUID,
#     db: Session = Depends(get_db),
#     _: dict = Depends(require_roles("admin")),  # Only admin can delete
# ):
#     existing_payment_method = crud.get_payment_method_by_id(db, payment_method_id=payment_method_id)
#     if not existing_payment_method:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Payment method not found"
#         )

#     deletion_successful = crud.delete_payment_method(db=db, payment_method_id=payment_method_id)
#     if not deletion_successful:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to delete payment method"
#         )
    
#     # Return 204 No Content with no response body for successful deletion
#     return None