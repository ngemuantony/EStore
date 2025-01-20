from fastapi import HTTPException
from datetime import datetime
from models import Product, Category, Tag, ProductAnalytics, format_product
from schemas import ProductRequest, UpdateQuantityRequest, CategoryCreate, TagCreate, ProductSearchParams
from typing import List, Optional

# Category operations
async def create_category(category: CategoryCreate) -> dict:
    category_obj = Category(
        name=category.name,
        description=category.description,
        parent_id=category.parent_id
    )
    category_obj.save()
    return {"id": category_obj.pk}

async def get_all_categories():
    return [format_category(pk) for pk in Category.all_pks()]

def format_category(pk: str):
    category = Category.get(pk)
    if not category:
        return None
    return {
        'id': category.pk,
        'name': category.name,
        'description': category.description,
        'parent_id': category.parent_id
    }

# Tag operations
async def create_tag(tag: TagCreate) -> dict:
    tag_obj = Tag(name=tag.name)
    tag_obj.save()
    return {"id": tag_obj.pk}

async def get_all_tags():
    return [format_tag(pk) for pk in Tag.all_pks()]

def format_tag(pk: str):
    tag = Tag.get(pk)
    if not tag:
        return None
    return {
        'id': tag.pk,
        'name': tag.name
    }

# Product operations
async def create_new_product(product: ProductRequest, user_id: int) -> dict:
    # Validate category if provided
    if product.category_id and not Category.get(product.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Validate tags
    valid_tags = []
    for tag_id in product.tags:
        if Tag.get(tag_id):
            valid_tags.append(tag_id)
    
    product_obj = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        created_by=user_id,
        category_id=product.category_id,
        description=product.description,
        tags=valid_tags,
        image_url=product.image_url,
        min_stock_level=product.min_stock_level,
        discount_percentage=product.discount_percentage
    )
    product_obj.save()
    
    # Initialize analytics
    analytics = ProductAnalytics(
        product_id=product_obj.pk,
        views=0,
        stock_updates=1,
        last_stock_update=datetime.utcnow()
    )
    analytics.save()
    
    return {"id": product_obj.pk}

async def get_all_products():
    return [format_product(pk) for pk in Product.all_pks()]

async def get_product_by_id(pk: str):
    product = Product.get(pk)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update view count
    try:
        analytics = ProductAnalytics.get(pk)
        analytics.views += 1
        analytics.last_viewed = datetime.utcnow()
        analytics.save()
    except:
        pass
    
    return format_product(pk)

async def delete_product_by_id(pk: str):
    if not Product.get(pk):
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete associated analytics
    try:
        ProductAnalytics.delete(pk)
    except:
        pass
    
    return Product.delete(pk)

async def update_product_quantity(pk: str, update: UpdateQuantityRequest):
    product = Product.get(pk)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.quantity = update.quantity
    product.updated_at = datetime.utcnow()
    product.save()
    
    # Update analytics
    try:
        analytics = ProductAnalytics.get(pk)
        analytics.stock_updates += 1
        analytics.last_stock_update = datetime.utcnow()
        analytics.save()
    except:
        pass
    
    # Check if below minimum stock level
    if product.min_stock_level and product.quantity <= product.min_stock_level:
        # TODO: Implement notification system for low stock
        print(f"Low stock alert for product {product.name}: {product.quantity} items remaining")
    
    return format_product(pk)

async def search_products(params: ProductSearchParams) -> List[dict]:
    all_products = [format_product(pk) for pk in Product.all_pks()]
    filtered_products = []
    
    for product in all_products:
        if product is None:
            continue
            
        # Apply filters
        if params.name and params.name.lower() not in product['name'].lower():
            continue
            
        if params.category_id and product['category_id'] != params.category_id:
            continue
            
        if params.min_price is not None and product['price'] < params.min_price:
            continue
            
        if params.max_price is not None and product['price'] > params.max_price:
            continue
            
        if params.tags:
            if not all(tag in product['tags'] for tag in params.tags):
                continue
                
        if params.in_stock is not None:
            if params.in_stock and product['quantity'] <= 0:
                continue
            elif not params.in_stock and product['quantity'] > 0:
                continue
        
        filtered_products.append(product)
    
    return filtered_products
