from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: str

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: str

class ProductRequest(BaseModel):
    name: str
    price: float
    quantity: int
    category_id: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    image_url: Optional[str] = None
    min_stock_level: Optional[int] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    
    class Config:
        arbitrary_types_allowed = True

class UpdateQuantityRequest(BaseModel):
    quantity: int

class ProductSearchParams(BaseModel):
    name: Optional[str] = None
    category_id: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    tags: Optional[List[str]] = None
    in_stock: Optional[bool] = None

class ProductAnalyticsResponse(BaseModel):
    views: int
    last_viewed: Optional[datetime]
    stock_updates: int
    last_stock_update: Optional[datetime]

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    quantity: int
    created_by: int
    category: Optional[str]
    description: Optional[str]
    tags: List[str]
    image_url: Optional[str]
    min_stock_level: Optional[int]
    discount_percentage: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    analytics: ProductAnalyticsResponse

    class Config:
        arbitrary_types_allowed = True
