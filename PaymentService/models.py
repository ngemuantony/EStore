from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
from redis_om import HashModel, Field
import json
from database import redis

class PaymentMethod(HashModel):
    user_id: int = Field(index=True)
    type: str = Field(index=True)  # e.g., 'card', 'paypal'
    details_json: str = Field(default="{}")  # Store payment details as JSON string
    created_at: datetime = Field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    is_default: bool = Field(default=False)
    is_active: bool = Field(default=True)

    class Meta:
        database = redis

    @property
    def details(self) -> Dict:
        """Get payment details as dictionary"""
        try:
            return json.loads(self.details_json)
        except json.JSONDecodeError:
            return {}

    def set_details(self, details: Dict):
        """Set payment details from dictionary"""
        self.details_json = json.dumps(details)
        self.save()

class Order(HashModel):
    product_id: str = Field(index=True)
    user_id: int = Field(index=True)
    quantity: int = Field(index=True)
    price: float = Field(index=True)
    fee: float = Field(index=True)
    total: float = Field(index=True)
    status: str = Field(index=True, default="pending")  # pending, paid, cancelled, refunded
    payment_method_id: Optional[str] = Field(index=True)
    payment_status: str = Field(index=True, default="pending")  # pending, processing, completed, failed
    payment_error: Optional[str] = None
    notes_json: str = Field(default="[]")  # Store notes as JSON string
    refund_amount: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Meta:
        database = redis

    @property
    def notes(self) -> List[str]:
        """Get notes as list"""
        try:
            return json.loads(self.notes_json)
        except json.JSONDecodeError:
            return []

    def add_note(self, note: str):
        """Add a note to the order with timestamp"""
        timestamp = datetime.now().isoformat()
        notes = self.notes
        notes.append(f"[{timestamp}] {note}")
        self.notes_json = json.dumps(notes)
        self.save()

    def update_status(self, status: str, note: Optional[str] = None):
        """Update order status with optional note"""
        self.status = status
        self.updated_at = datetime.now()
        if note:
            self.add_note(note)
        self.save()

    def process_refund(self, amount: Optional[float] = None):
        """Process a refund for the order"""
        if self.status != 'paid':
            raise ValueError("Can only refund paid orders")
            
        refund_amount = amount if amount is not None else self.total
        if refund_amount > self.total:
            raise ValueError("Refund amount cannot exceed order total")
            
        self.refund_amount = refund_amount
        self.status = 'refunded'
        self.updated_at = datetime.now()
        self.add_note(f"Refund processed: ${refund_amount:.2f}")
        self.save()
