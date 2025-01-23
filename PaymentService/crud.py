from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import cast, JSON, text
from fastapi import HTTPException
from typing import List, Dict, Optional
from models import PaymentMethod, Order
import json

# Payment Method operations
def create_payment_method(db: Session, user_id: int, payment_type: str, details: Dict) -> PaymentMethod:
    """Create a new payment method"""
    try:
        # Check for existing card
        if payment_type == "Card" and "card_number" in details:
            card_number = details["card_number"]
            # Query for existing payment method with the same card number using PostgreSQL JSONB operator
            existing = db.query(PaymentMethod).filter(
                PaymentMethod.user_id == str(user_id),
                PaymentMethod.payment_type == "Card",
                PaymentMethod.is_active == True,
                text("details->>'card_number' = :card_number")
            ).params(card_number=card_number).first()
            
            if existing:
                print(f"Found existing card with number: {card_number}")
                return existing

        # Create new payment method
        payment_method = PaymentMethod(
            user_id=str(user_id),
            payment_type=payment_type,
            details=details,
            is_active=True
        )
        db.add(payment_method)
        db.commit()
        db.refresh(payment_method)
        return payment_method
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create payment method: {str(e)}"
        )

def get_user_payment_methods(db: Session, user_id: int) -> List[PaymentMethod]:
    """Get all payment methods for a user"""
    try:
        return db.query(PaymentMethod).filter(
            PaymentMethod.user_id == str(user_id),
            PaymentMethod.is_active == True
        ).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get payment methods: {str(e)}"
        )

def get_payment_method(db: Session, payment_method_id: int) -> Optional[PaymentMethod]:
    """Get a specific payment method"""
    try:
        return db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_method_id,
            PaymentMethod.is_active == True
        ).first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get payment method: {str(e)}"
        )

def delete_payment_method(db: Session, payment_method_id: int, user_id: int):
    """Soft delete a payment method"""
    try:
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_method_id,
            PaymentMethod.user_id == str(user_id)
        ).first()
        
        if not payment_method:
            raise HTTPException(status_code=404, detail="Payment method not found")
            
        payment_method.is_active = False
        db.commit()
        return payment_method
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete payment method: {str(e)}"
        )

# Order operations
def create_order(db: Session, user_id: int, product_id: str, quantity: int, payment_method_id: Optional[int] = None) -> Order:
    """Create a new order"""
    try:
        # TODO: Get product price from product service
        price_per_unit = 1000  # Example: $10.00 in cents
        total_amount = price_per_unit * quantity
        
        order = Order(
            user_id=str(user_id),
            product_id=product_id,
            quantity=quantity,
            total_amount=total_amount,
            status="pending",
            payment_method_id=payment_method_id
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create order: {str(e)}"
        )

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    """Get all orders for a user"""
    try:
        return db.query(Order).filter(
            Order.user_id == str(user_id)
        ).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get orders: {str(e)}"
        )

def get_order(db: Session, order_id: int) -> Optional[Order]:
    """Get a specific order"""
    try:
        return db.query(Order).filter(Order.id == order_id).first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get order: {str(e)}"
        )

def update_order_status(db: Session, order_id: int, status: str, note: Optional[str] = None) -> Order:
    """Update order status"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
            
        order.status = status
        db.commit()
        db.refresh(order)
        return order
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update order status: {str(e)}"
        )

async def create_order(order_request, user_id: int, payment_method_id: Optional[str] = None) -> Order:
    try:
        # Calculate fee (example: 5% of price)
        fee = order_request.price * 0.05
        total = order_request.price + fee
        
        order = Order(
            product_id=order_request.product_id,
            user_id=user_id,
            quantity=order_request.quantity,
            price=order_request.price,
            fee=fee,
            total=total,
            payment_method_id=payment_method_id
        )
        
        # Add initial note
        order.add_note("Order created")
        order.save()
        
        return order
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

async def get_order(order_id: str) -> Optional[Order]:
    try:
        return Order.get(order_id)
    except Exception:
        return None

async def get_user_orders(user_id: int) -> List[Order]:
    return Order.find(Order.user_id == user_id).all()

async def update_order_status(order_id: str, status: str, note: Optional[str] = None) -> Order:
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.update_status(status, note)
    return order

async def process_payment(order_id: str) -> Order:
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Here you would integrate with actual payment gateway
    # For demo, we'll simulate payment processing
    try:
        # Simulate payment processing
        order.payment_status = 'processing'
        order.add_note("Payment processing started")
        order.save()
        
        # Simulate successful payment
        order.payment_status = 'completed'
        order.status = 'paid'
        order.add_note("Payment completed successfully")
        order.save()
        
    except Exception as e:
        order.payment_status = 'failed'
        order.payment_error = str(e)
        order.add_note(f"Payment failed: {str(e)}")
        order.save()
        raise HTTPException(status_code=400, detail=f"Payment failed: {str(e)}")
    
    return order

async def process_refund(order_id: str, amount: Optional[float] = None, reason: str = "") -> Order:
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != 'paid':
        raise HTTPException(status_code=400, detail="Order must be paid to process refund")
    
    try:
        # Here you would integrate with actual payment gateway for refund
        # For demo, we'll simulate refund processing
        order.process_refund(amount)
        order.add_note(f"Refund processed. Reason: {reason}")
        order.save()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Refund failed: {str(e)}")
    
    return order
