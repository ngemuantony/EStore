from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class OrderRequest(BaseModel):
    product_id: str
    quantity: int
    price: float
    payment_method_id: Optional[str] = None

class PaymentMethodBase(BaseModel):
    type: str = Field(..., description="Payment method type (e.g., 'card', 'paypal')")
    details: Dict = Field(..., description="Payment method details")

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    id: str
    user_id: int
    created_at: datetime
    last_used: Optional[datetime]
    is_default: bool
    is_active: bool

class OrderResponse(BaseModel):
    id: str
    product_id: str
    user_id: int
    quantity: int
    price: float
    fee: float
    total: float
    status: str
    payment_method_id: Optional[str]
    payment_status: str
    payment_error: Optional[str]
    notes: List[str]
    refund_amount: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., description="New status for the order")
    note: Optional[str] = None

class RefundRequest(BaseModel):
    amount: Optional[float] = None
    reason: str = Field(default="", description="Reason for the refund")
