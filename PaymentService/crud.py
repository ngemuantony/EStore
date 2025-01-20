from fastapi import HTTPException
import uuid
from datetime import datetime
from typing import List, Optional, Dict
from models import Order, PaymentMethod
from schemas import OrderRequest

async def create_order(order_request: OrderRequest, user_id: int, payment_method_id: Optional[str] = None) -> Order:
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

# Payment Method operations
async def create_payment_method(user_id: int, type: str, details: Dict) -> PaymentMethod:
    payment_method = PaymentMethod(
        user_id=user_id,
        type=type
    )
    payment_method.set_details(details)
    payment_method.save()
    return payment_method

async def get_user_payment_methods(user_id: int) -> List[PaymentMethod]:
    return PaymentMethod.find(PaymentMethod.user_id == user_id).all()

async def get_payment_method(payment_method_id: str) -> Optional[PaymentMethod]:
    try:
        return PaymentMethod.get(payment_method_id)
    except Exception:
        return None

async def delete_payment_method(payment_method_id: str) -> bool:
    payment_method = await get_payment_method(payment_method_id)
    if payment_method:
        payment_method.delete()
        return True
    return False
