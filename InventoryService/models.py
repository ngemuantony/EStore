from redis_om import HashModel, Field
from database import redis
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Category(HashModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    
    class Meta:
        database = redis

class Tag(HashModel):
    name: str = Field(index=True)
    
    class Meta:
        database = redis

class ProductAnalytics(HashModel):
    product_id: str
    views: int = Field(default=0)
    last_viewed: Optional[datetime] = None
    stock_updates: int = Field(default=0)
    last_stock_update: Optional[datetime] = None
    
    class Meta:
        database = redis

class Product(HashModel):
    name: str = Field(index=True)
    price: float = Field(index=True)
    quantity: int = Field(index=True)
    created_by: int
    category_id: Optional[str] = Field(index=True)
    description: Optional[str] = None
    tag_ids: str = Field(index=True, default="")  # Store as comma-separated string
    image_url: Optional[str] = None
    min_stock_level: Optional[int] = None
    discount_percentage: Optional[float] = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Meta:
        database = redis

def format_product(pk: str):
    product = Product.get(pk)
    if not product:
        return None
        
    # Get category if exists
    category = None
    if product.category_id:
        category = Category.get(product.category_id)
        
    # Get tags
    tags = []
    for tag_id in product.tag_ids.split(","):
        if tag_id:
            tag = Tag.get(tag_id)
            if tag:
                tags.append(tag.name)
                
    # Get analytics
    analytics = None
    try:
        analytics = ProductAnalytics.get(product.pk)
    except:
        analytics = ProductAnalytics(
            product_id=product.pk,
            views=0
        )
        analytics.save()
    
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'created_by': product.created_by,
        'category': category.name if category else None,
        'description': product.description,
        'tags': tags,
        'image_url': product.image_url,
        'min_stock_level': product.min_stock_level,
        'discount_percentage': product.discount_percentage,
        'created_at': product.created_at.isoformat() if product.created_at else None,
        'updated_at': product.updated_at.isoformat() if product.updated_at else None,
        'analytics': {
            'views': analytics.views if analytics else 0,
            'last_viewed': analytics.last_viewed.isoformat() if analytics and analytics.last_viewed else None,
            'stock_updates': analytics.stock_updates if analytics else 0,
            'last_stock_update': analytics.last_stock_update.isoformat() if analytics and analytics.last_stock_update else None
        }
    }
