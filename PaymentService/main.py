from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import wait_for_db

from database import get_db, Base, engine, SessionLocal
from schemas import (
    PaymentMethodCreate, PaymentMethodResponse,
    OrderCreate, OrderResponse,
    OrderStatusUpdate, RefundRequest
)
import crud

# Wait for database to be ready before creating tables
engine = wait_for_db(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/paymentdb"))
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment Service",
    description="""
    A microservice for managing payment methods and processing orders in the EStore application.
    
    Features:
    - Payment Method Management (CRUD operations)
    - Order Processing
    - PostgreSQL Database Integration
    - JWT Authentication (coming soon)
    """,
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Payment Method endpoints
@app.post("/payment-methods", response_model=PaymentMethodResponse,
    summary="Create a new payment method",
    description="Creates a new payment method for the authenticated user.")
async def create_payment_method(
    payment_method: PaymentMethodCreate,
    user_id: int = 1,  # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """Create a new payment method"""
    return crud.create_payment_method(
        db=db,
        user_id=user_id,
        payment_type=payment_method.payment_type,
        details=payment_method.details
    )

@app.get("/payment-methods", response_model=List[PaymentMethodResponse],
    summary="List user's payment methods",
    description="Retrieves all active payment methods for the authenticated user.")
async def get_payment_methods(
    user_id: int = 1,  # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """Get all payment methods for a user"""
    return crud.get_user_payment_methods(db=db, user_id=user_id)

@app.get("/payment-methods/{payment_method_id}", response_model=PaymentMethodResponse,
    summary="Get a specific payment method",
    description="Retrieves details of a specific payment method by its ID.")
async def get_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific payment method"""
    payment_method = crud.get_payment_method(db=db, payment_method_id=payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    return payment_method

@app.delete("/payment-methods/{payment_method_id}", response_model=PaymentMethodResponse,
    summary="Delete a payment method",
    description="Soft deletes a payment method by setting is_active to false.")
async def delete_payment_method(
    payment_method_id: int,
    user_id: int = 1,  # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """Delete a payment method"""
    return crud.delete_payment_method(db=db, payment_method_id=payment_method_id, user_id=user_id)

# Order endpoints
@app.post("/orders", response_model=OrderResponse,
    summary="Create a new order",
    description="Creates a new order with the specified product and payment method.")
async def create_order(
    order: OrderCreate,
    user_id: int = 1,  # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """Create a new order"""
    return crud.create_order(
        db=db,
        user_id=user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        payment_method_id=order.payment_method_id
    )

@app.get("/orders", response_model=List[OrderResponse],
    summary="List user's orders",
    description="Retrieves all orders for the authenticated user.")
async def get_orders(
    user_id: int = 1,  # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """Get all orders for a user"""
    return crud.get_user_orders(db=db, user_id=user_id)

@app.get("/orders/{order_id}", response_model=OrderResponse,
    summary="Get a specific order",
    description="Retrieves details of a specific order by its ID.")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific order"""
    order = crud.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}/status", response_model=OrderResponse,
    summary="Update order status",
    description="Updates the status of an order (e.g., pending, paid, cancelled).")
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update order status"""
    return crud.update_order_status(
        db=db,
        order_id=order_id,
        status=status_update.status,
        note=status_update.note
    )
