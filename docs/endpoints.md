# API Endpoints Documentation

## Overview
This document details all the API endpoints available in the EStore microservices ecosystem. Each service runs on its own port and provides a specific set of functionalities.

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## UserService (Port 8002)

### Authentication Endpoints
```http
POST /register
Description: Register a new user
Request:
{
    "email": "string",
    "password": "string"
}
Response: 201 Created
{
    "id": "integer",
    "email": "string",
    "is_active": "boolean",
    "is_verified": "boolean"
}

POST /token
Description: Get access token
Request:
{
    "username": "string",
    "password": "string"
}
Response: 200 OK
{
    "access_token": "string",
    "token_type": "bearer"
}

POST /verify/{token}
Description: Verify email address
Response: 200 OK
{
    "message": "Email verified successfully"
}
```

### User Management
```http
GET /users/me
Description: Get current user profile
Response: 200 OK
{
    "id": "integer",
    "email": "string",
    "is_active": "boolean",
    "is_verified": "boolean"
}

PUT /users/me
Description: Update current user
Request:
{
    "email": "string",
    "password": "string"
}
Response: 200 OK
{
    "id": "integer",
    "email": "string",
    "is_active": "boolean",
    "is_verified": "boolean"
}
```

## InventoryService (Port 8001)

### Product Management
```http
GET /products
Description: List all products
Query Parameters:
- category_id: integer
- min_price: integer (in cents)
- max_price: integer (in cents)
- in_stock: boolean
Response: 200 OK
[
    {
        "id": "integer",
        "name": "string",
        "price": "integer",
        "quantity": "integer",
        "category_id": "integer",
        "description": "string",
        "image_url": "string",
        "is_active": "boolean"
    }
]

POST /products
Description: Create a new product
Request:
{
    "name": "string",
    "price": "integer",
    "quantity": "integer",
    "category_id": "integer",
    "description": "string",
    "image_url": "string"
}
Response: 201 Created
{
    "id": "integer",
    "name": "string",
    "price": "integer",
    "quantity": "integer",
    "category_id": "integer",
    "description": "string",
    "image_url": "string",
    "is_active": "boolean"
}

GET /products/{product_id}
Description: Get product details
Response: 200 OK
{
    "id": "integer",
    "name": "string",
    "price": "integer",
    "quantity": "integer",
    "category_id": "integer",
    "description": "string",
    "image_url": "string",
    "is_active": "boolean"
}
```

### Category Management
```http
GET /categories
Description: List all categories
Response: 200 OK
[
    {
        "id": "integer",
        "name": "string",
        "description": "string",
        "parent_id": "integer"
    }
]

POST /categories
Description: Create a new category
Request:
{
    "name": "string",
    "description": "string",
    "parent_id": "integer"
}
Response: 201 Created
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "parent_id": "integer"
}
```

## PaymentService (Port 8000)

### Payment Methods
```http
POST /payment-methods
Description: Create a new payment method
Request:
{
    "payment_type": "string",
    "details": {
        "card_number": "string",
        "expiry_month": "integer",
        "expiry_year": "integer",
        "cvv": "string"
    }
}
Response: 201 Created
{
    "id": "integer",
    "user_id": "string",
    "payment_type": "string",
    "details": "object",
    "is_active": "boolean"
}

GET /payment-methods
Description: List user's payment methods
Response: 200 OK
[
    {
        "id": "integer",
        "user_id": "string",
        "payment_type": "string",
        "details": "object",
        "is_active": "boolean"
    }
]

DELETE /payment-methods/{payment_method_id}
Description: Delete a payment method
Response: 200 OK
{
    "id": "integer",
    "user_id": "string",
    "payment_type": "string",
    "details": "object",
    "is_active": "boolean"
}
```

### Order Management
```http
POST /orders
Description: Create a new order
Request:
{
    "product_id": "string",
    "quantity": "integer",
    "payment_method_id": "integer"
}
Response: 201 Created
{
    "id": "integer",
    "user_id": "string",
    "product_id": "string",
    "quantity": "integer",
    "total_amount": "integer",
    "status": "string",
    "payment_method_id": "integer"
}

GET /orders
Description: List user's orders
Response: 200 OK
[
    {
        "id": "integer",
        "user_id": "string",
        "product_id": "string",
        "quantity": "integer",
        "total_amount": "integer",
        "status": "string",
        "payment_method_id": "integer"
    }
]

GET /orders/{order_id}
Description: Get order details
Response: 200 OK
{
    "id": "integer",
    "user_id": "string",
    "product_id": "string",
    "quantity": "integer",
    "total_amount": "integer",
    "status": "string",
    "payment_method_id": "integer"
}

PUT /orders/{order_id}/status
Description: Update order status
Request:
{
    "status": "string",
    "note": "string"
}
Response: 200 OK
{
    "id": "integer",
    "user_id": "string",
    "product_id": "string",
    "quantity": "integer",
    "total_amount": "integer",
    "status": "string",
    "payment_method_id": "integer"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "detail": "Error message explaining what went wrong"
}
```

### 401 Unauthorized
```json
{
    "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
    "detail": "Not enough privileges"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
    "detail": [
        {
            "loc": ["body", "field_name"],
            "msg": "field validation error",
            "type": "value_error"
        }
    ]
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

## Rate Limiting

All endpoints are subject to rate limiting:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1640995200
