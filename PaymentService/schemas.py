from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class OrderRequest(BaseModel):
    id: str  # This will be used as product_id
    quantity: int
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

class OrderNote(BaseModel):
    timestamp: datetime
    content: str

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
    created_at: datetime
    updated_at: Optional[datetime]
    notes: List[str]
    refund_amount: Optional[float]
    payment_status: str
    payment_error: Optional[str]

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., description="New status for the order")
    note: Optional[str] = None

class RefundRequest(BaseModel):
    amount: Optional[float] = None
    reason: str
