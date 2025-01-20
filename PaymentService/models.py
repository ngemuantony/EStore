from typing import Dict, Optional
from datetime import datetime
import uuid

class PaymentMethod:
    def __init__(self, id: str, user_id: int, type: str, details: Dict):
        self.id = id
        self.user_id = user_id
        self.type = type  # 'card', 'paypal', etc.
        self.details = details
        self.created_at = datetime.utcnow()

class Order:
    def __init__(
        self,
        product_id: str,
        user_id: int,
        quantity: int,
        price: float,
        fee: float,
        payment_method_id: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.price = price
        self.fee = fee
        self.total = price + fee
        self.status = 'pending'  # pending, paid, cancelled, refunded
        self.payment_method_id = payment_method_id
        self.created_at = datetime.utcnow()
        self.updated_at = None
        self.notes: List[str] = []
        self.refund_amount: Optional[float] = None
        self.payment_status: str = 'pending'  # pending, processing, completed, failed
        self.payment_error: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'quantity': self.quantity,
            'price': self.price,
            'fee': self.fee,
            'total': self.total,
            'status': self.status,
            'payment_method_id': self.payment_method_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'refund_amount': self.refund_amount,
            'payment_status': self.payment_status,
            'payment_error': self.payment_error
        }

    def add_note(self, note: str):
        self.notes.append(f"{datetime.utcnow().isoformat()}: {note}")
        self.updated_at = datetime.utcnow()

    def update_status(self, status: str, note: Optional[str] = None):
        self.status = status
        self.updated_at = datetime.utcnow()
        if note:
            self.add_note(note)

    def process_refund(self, amount: Optional[float] = None):
        if amount is None:
            amount = self.total
        if amount > self.total:
            raise ValueError("Refund amount cannot exceed order total")
        self.refund_amount = amount
        self.status = 'refunded'
        self.updated_at = datetime.utcnow()
        self.add_note(f"Refunded amount: ${amount:.2f}")

# In-memory storage
payment_methods: Dict[str, PaymentMethod] = {}
orders: Dict[str, Order] = {}
