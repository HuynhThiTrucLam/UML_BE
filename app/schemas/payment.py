import datetime
from pydantic import BaseModel, UUID4, Field, field_validator, RootModel
from typing import Optional, List
from datetime import date

class PaymentBase(BaseModel):
    payment_method_id: UUID4
    evidence: str
    course_registration_id: UUID4

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    amount: Optional[float] = None
    paymeent_method: Optional[UUID4] = None
    evidence: Optional[str] = None
    course_registration_id: Optional[UUID4] = None

class Payment(PaymentBase):
    id: UUID4
    amount: float
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)
        }

class PaymentList(RootModel):
    root: List[Payment]

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)
        }