from pydantic import BaseModel, UUID4, Field
from typing import Optional, List

class PaymentMethodBase(BaseModel):
    name: str

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            UUID4: lambda v: str(v),
        }
    }

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(PaymentMethodBase):
    id: Optional[UUID4] = Field(default=None, alias="payment_method_id")

class PaymentMethod(PaymentMethodBase):
    id: Optional[UUID4] = Field(default=None, alias="payment_method_id")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    deleted_at: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
        "json_encoders": {
            UUID4: lambda v: str(v),
        }
    }

class PaymentMethodList(BaseModel):
    payment_methods: List[PaymentMethod]
    total: int

    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
        "json_encoders": {
            UUID4: lambda v: str(v),
        }
    }
