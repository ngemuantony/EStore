from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import auth
import crud
from schemas import (
    OrderRequest,
    OrderResponse,
    OrderStatusUpdate,
    PaymentMethodCreate,
    PaymentMethodResponse,
    RefundRequest
)
from typing import List

# Constants
USER_SERVICE_URL = "http://localhost:8002"

# FastAPI app initialization
app = FastAPI()

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{USER_SERVICE_URL}/token")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Payment Method endpoints
@app.post("/payment-methods", response_model=PaymentMethodResponse)
async def create_payment_method(
    payment_method: PaymentMethodCreate,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    return crud.create_payment_method(
        user_id=user["id"],
        type=payment_method.type,
        details=payment_method.details
    )

@app.get("/payment-methods", response_model=List[PaymentMethodResponse])
async def get_payment_methods(token: str = Depends(oauth2_scheme)):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    return crud.get_user_payment_methods(user["id"])

@app.delete("/payment-methods/{payment_method_id}")
async def delete_payment_method(
    payment_method_id: str,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    payment_method = crud.get_payment_method(payment_method_id)
    if not payment_method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    
    if payment_method.user_id != user["id"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this payment method"
        )
    
    crud.delete_payment_method(payment_method_id)
    return {"message": "Payment method deleted successfully"}

# Order endpoints
@app.post("/orders", response_model=OrderResponse)
async def create_order(
    order: OrderRequest,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # Validate payment method if provided
    if order.payment_method_id:
        payment_method = crud.get_payment_method(order.payment_method_id)
        if not payment_method:
            raise HTTPException(
                status_code=404,
                detail="Payment method not found"
            )
        if payment_method.user_id != user["id"]:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to use this payment method"
            )
    
    return await crud.create_order(order, user["id"], order.payment_method_id)

@app.get("/orders", response_model=List[OrderResponse])
async def get_orders(token: str = Depends(oauth2_scheme)):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    return await crud.get_user_orders(user["id"])

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    order = await crud.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    if order.user_id != user["id"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view this order"
        )
    
    return order

@app.patch("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # Only allow admin to update order status
    is_admin = await auth.verify_admin(token)
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update order status"
        )
    
    return await crud.update_order_status(
        order_id=order_id,
        status=status_update.status,
        note=status_update.note
    )

@app.post("/orders/{order_id}/process-payment", response_model=OrderResponse)
async def process_payment(
    order_id: str,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    order = await crud.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    if order.user_id != user["id"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to process payment for this order"
        )
    
    return await crud.process_payment(order_id)

@app.post("/orders/{order_id}/refund", response_model=OrderResponse)
async def refund_order(
    order_id: str,
    refund_request: RefundRequest,
    token: str = Depends(oauth2_scheme)
):
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # Only allow admin to process refunds
    is_admin = await auth.verify_admin(token)
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can process refunds"
        )
    
    return await crud.process_refund(
        order_id=order_id,
        amount=refund_request.amount,
        reason=refund_request.reason
    )
