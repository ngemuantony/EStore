from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

class PaymentMethodBase(BaseModel):
    """Base schema for payment methods"""
    payment_type: str = Field(..., description="Type of payment method (e.g., Card, PayPal)")
    details: Dict = Field(..., description="Payment method details (e.g., card number, expiry)")

class PaymentMethodCreate(PaymentMethodBase):
    """Schema for creating a new payment method"""
    pass

class PaymentMethodResponse(PaymentMethodBase):
    """Schema for payment method responses"""
    id: int = Field(..., description="Unique identifier for the payment method")
    user_id: str = Field(..., description="ID of the user who owns this payment method")
    is_active: bool = Field(..., description="Whether this payment method is active")
    created_at: datetime = Field(..., description="When this payment method was created")
    updated_at: Optional[datetime] = Field(None, description="When this payment method was last updated")

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    """Base schema for orders"""
    product_id: str = Field(..., description="ID of the product being ordered")
    quantity: int = Field(..., gt=0, description="Quantity of the product")
    payment_method_id: Optional[int] = Field(None, description="ID of the payment method to use")

class OrderCreate(OrderBase):
    """Schema for creating a new order"""
    pass

class OrderResponse(OrderBase):
    """Schema for order responses"""
    id: int = Field(..., description="Unique identifier for the order")
    user_id: str = Field(..., description="ID of the user who placed the order")
    total_amount: int = Field(..., description="Total amount in cents")
    status: str = Field(..., description="Current status of the order")
    created_at: datetime = Field(..., description="When this order was created")
    updated_at: Optional[datetime] = Field(None, description="When this order was last updated")

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    """Schema for updating order status"""
    status: str = Field(..., description="New status for the order")
    note: Optional[str] = Field(None, description="Optional note about the status change")

class RefundRequest(BaseModel):
    """Schema for requesting a refund"""
    amount: Optional[int] = Field(None, description="Amount to refund in cents, defaults to full amount")
    reason: str = Field(..., description="Reason for the refund")
