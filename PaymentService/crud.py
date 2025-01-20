from typing import Dict, List
import uuid
from fastapi import HTTPException
from schemas import Order, OrderRequest
from services import InventoryService
from models import PaymentMethod, Order, payment_methods, orders

# In-memory storage
orders: Dict[str, dict] = {}

async def create_order(order_request: OrderRequest, user_id: int, payment_method_id: Optional[str] = None) -> Order:
    try:
        # Get product from inventory service
        product = await InventoryService.get_product(order_request.id)
        
        # Check if enough quantity is available
        if product['quantity'] < order_request.quantity:
            raise HTTPException(status_code=400, detail="Not enough quantity available")
            
        # Calculate order details    
        price = float(product['price']) * order_request.quantity
        fee = price * 0.2  # 20% fee
        total = price + fee
        
        # Update inventory quantity
        new_quantity = product['quantity'] - order_request.quantity
        await InventoryService.update_quantity(order_request.id, new_quantity)
        
        # Create order
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            product_id=order_request.id,
            price=price,
            fee=fee,
            total=total,
            quantity=order_request.quantity,
            status='pending',
            user_id=user_id,
            payment_method_id=payment_method_id
        )
        
        # Add initial note
        order.add_note("Order created")
        
        # Store in memory
        orders[order_id] = order.dict()
        
        return order
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with inventory service: {str(e)}")

async def get_order(order_id: str) -> Dict:
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

async def get_user_orders(user_id: int) -> List[Dict]:
    return [order for order in orders.values() if order["user_id"] == user_id]

# Payment Method operations
def create_payment_method(user_id: int, type: str, details: Dict) -> PaymentMethod:
    payment_method_id = str(uuid.uuid4())
    payment_method = PaymentMethod(
        id=payment_method_id,
        user_id=user_id,
        type=type,
        details=details
    )
    payment_methods[payment_method_id] = payment_method
    return payment_method

def get_user_payment_methods(user_id: int) -> List[PaymentMethod]:
    return [pm for pm in payment_methods.values() if pm.user_id == user_id]

def get_payment_method(payment_method_id: str) -> Optional[PaymentMethod]:
    return payment_methods.get(payment_method_id)

def delete_payment_method(payment_method_id: str):
    if payment_method_id in payment_methods:
        del payment_methods[payment_method_id]
        return True
    return False

def update_order_status(order_id: str, status: str, note: Optional[str] = None) -> Order:
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.update_status(status, note)
    return order

def process_payment(order_id: str) -> Order:
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Here you would integrate with actual payment gateway
    # For demo, we'll simulate payment processing
    try:
        # Simulate payment processing
        order.payment_status = 'processing'
        order.add_note("Payment processing started")
        
        # Simulate successful payment
        order.payment_status = 'completed'
        order.status = 'paid'
        order.add_note("Payment completed successfully")
        
    except Exception as e:
        order.payment_status = 'failed'
        order.payment_error = str(e)
        order.add_note(f"Payment failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Payment failed: {str(e)}")
    
    return order

def process_refund(order_id: str, amount: Optional[float] = None, reason: str = "") -> Order:
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != 'paid':
        raise HTTPException(status_code=400, detail="Order must be paid to process refund")
    
    try:
        # Here you would integrate with actual payment gateway for refund
        # For demo, we'll simulate refund processing
        order.process_refund(amount)
        order.add_note(f"Refund processed. Reason: {reason}")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Refund failed: {str(e)}")
    
    return order
