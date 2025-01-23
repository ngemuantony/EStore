import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import auth
import crud
from schemas import (
    ProductRequest, 
    UpdateQuantityRequest, 
    CategoryCreate,
    TagCreate,
    ProductSearchParams
)
from typing import List, Optional
from redis_om import get_redis_connection, HashModel
import requests
import sys
from utils.database import wait_for_db

# Load environment variables
load_dotenv()

# Constants
USER_SERVICE_URL = "http://localhost:8002"

# FastAPI app initialization
app = FastAPI(title="Inventory Service")

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

# Redis connection using redis-om
redis = get_redis_connection(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    created_by: int  # Add user_id to track who created the product

    class Meta:
        database = redis

# Category endpoints
@app.post("/categories")
async def create_category(
    category: CategoryCreate,
    token: str = Depends(oauth2_scheme)
):
    # Verify user is admin
    is_admin = await auth.verify_admin(token)
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only verified users can create categories"
        )
    return await crud.create_category(category)

@app.get("/categories")
async def get_categories(token: str = Depends(oauth2_scheme)):
    # Verify user is authenticated
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    return await crud.get_all_categories()

# Tag endpoints
@app.post("/tags")
async def create_tag(
    tag: TagCreate,
    token: str = Depends(oauth2_scheme)
):
    # Verify user is admin
    is_admin = await auth.verify_admin(token)
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only verified users can create tags"
        )
    return await crud.create_tag(tag)

@app.get("/tags")
async def get_tags(token: str = Depends(oauth2_scheme)):
    # Verify user is authenticated
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    return await crud.get_all_tags()

# Product endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/products")
async def get_products(
    token: str = Depends(oauth2_scheme),
    name: Optional[str] = None,
    category_id: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    tags: Optional[List[str]] = Query(None),
    in_stock: Optional[bool] = None
):
    # Verify user is authenticated
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # If no search parameters, return all products
    if not any([name, category_id, min_price, max_price, tags, in_stock]):
        return await crud.get_all_products()
    
    # Otherwise, perform search
    search_params = ProductSearchParams(
        name=name,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        tags=tags,
        in_stock=in_stock
    )
    return await crud.search_products(search_params)

@app.post("/products")
async def create_product(
    product: ProductRequest,
    token: str = Depends(oauth2_scheme)
):
    # Verify user is admin
    is_admin = await auth.verify_admin(token)
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only verified users can create products"
        )

    user = await auth.verify_user_token(token)
    return await crud.create_new_product(product, user["id"])

@app.get("/products/{pk}")
async def get_product(pk: str, token: str = Depends(oauth2_scheme)):
    # Verify user is authenticated
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    return await crud.get_product_by_id(pk)

@app.delete("/products/{pk}")
async def delete_product(
    pk: str,
    token: str = Depends(oauth2_scheme)
):
    # Verify user is admin
    is_admin = await auth.verify_admin(token)
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only verified users can delete products"
        )

    # Check if product exists and user has permission
    product = await crud.get_product_by_id(pk)
    user = await auth.verify_user_token(token)
    auth.check_product_owner(product, user["id"])

    return await crud.delete_product_by_id(pk)

@app.patch("/products/{pk}/quantity")
async def update_quantity(
    pk: str,
    update: UpdateQuantityRequest,
    token: str = Depends(oauth2_scheme)
):
    # Verify user is authenticated
    user = await auth.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    return await crud.update_product_quantity(pk, update)