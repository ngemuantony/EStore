# Testing E-Store API with Postman

This document provides instructions for testing all the microservices in the E-Store application using Postman.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Authentication](#authentication)
- [User Service](#user-service)
- [Inventory Service](#inventory-service)
- [Payment Service](#payment-service)
- [Common Issues](#common-issues)

## Prerequisites

1. Make sure all services are running:
   ```bash
   # User Service (Port 8002)
   cd UserService
   uvicorn main:app --reload --port 8002

   # Inventory Service (Port 8001)
   cd InventoryService
   uvicorn main:app --reload --port 8001

   # Payment Service (Port 8000)
   cd PaymentService
   uvicorn main:app --reload --port 8000

   # Verification Service (Port 8003)
   cd VerificationService
   uvicorn main:app --reload --port 8003
   ```

2. Install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)

## Authentication

### 1. Create User Account
```http
POST http://localhost:8002/users/
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "testuser",
    "password": "strongpassword123"
}
```

### 2. Verify Email
Check your email for the verification link and make a POST request:
```http
POST http://localhost:8002/users/verify/{verification_code}
```

### 3. Get Authentication Token
```http
POST http://localhost:8002/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com
password=strongpassword123
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV...",
    "token_type": "bearer"
}
```

Save this token for all subsequent requests!

## User Service (Port 8002)

All requests except registration and login require the Authorization header:
```
Authorization: Bearer your_access_token
```

### Get User Profile
```http
GET http://localhost:8002/users/me/
```

### Update User Profile
```http
PUT http://localhost:8002/users/me/
Content-Type: application/json

{
    "username": "newusername",
    "email": "newemail@example.com"
}
```

## Inventory Service (Port 8001)

### List Products
```http
GET http://localhost:8001/products
```

Query Parameters:
- `name`: Search by product name
- `category_id`: Filter by category
- `min_price`: Minimum price
- `max_price`: Maximum price
- `tags`: Filter by tags (comma-separated)
- `in_stock`: true/false

### Get Single Product
```http
GET http://localhost:8001/products/{product_id}
```

### Get Categories
```http
GET http://localhost:8001/categories
```

### Get Tags
```http
GET http://localhost:8001/tags
```

## Payment Service

### Create Payment Method

To create a payment method, send a POST request to `/payment-methods` with the following JSON structure:

```json
{
    "payment_type": "Card",
    "details": {
        "card_number": "15346781053311236",
        "expiry_month": 12,
        "expiry_year": 2029,
        "cvc": "123"
    }
}
```

### Example Request

- **URL**: `http://localhost:8000/payment-methods`
- **Method**: `POST`
- **Headers**: 
    - `Authorization: Bearer <your_jwt_token>`
- **Body**: (as shown above)

### Common Issues
- Ensure that the `payment_type` and `details` fields are correctly formatted.

### List Payment Methods
```http
GET http://localhost:8000/payment-methods
```

### Create Order
```http
POST http://localhost:8000/orders
Content-Type: application/json

{
    "product_id": "product_id_here",
    "quantity": 1,
    "price": 99.99,
    "payment_method_id": "payment_method_id_here"
}
```

### Process Payment
```http
POST http://localhost:8000/orders/{order_id}/pay
```

### Get Order Details
```http
GET http://localhost:8000/orders/{order_id}
```

### Request Refund
```http
POST http://localhost:8000/orders/{order_id}/refund
Content-Type: application/json

{
    "amount": 99.99,
    "reason": "Customer request"
}
```

## Common Issues

### 1. Authentication Errors
- **401 Unauthorized**: Token is missing or invalid
  - Solution: Make sure to include the Authorization header with a valid token
  - Token format: `Bearer your_access_token`

### 2. Validation Errors
- **400 Bad Request**: Check the request body format
- Make sure all required fields are included
- Check data types (e.g., price should be a number)

### 3. Resource Not Found
- **404 Not Found**: Check if the ID exists
- Verify the URL path is correct

### 4. Service Unavailable
- **503 Service Unavailable**: Make sure all required services are running
- Check if Redis is running for Inventory and Payment services
- Check if PostgreSQL is running for User and Verification services

## Testing Flow Example

1. Create user account
2. Verify email
3. Get authentication token
4. Browse products
5. Create payment method
6. Create order
7. Process payment
8. Check order status

## Environment Variables

Each service requires specific environment variables. Make sure to copy `.env.example` to `.env` in each service directory and update the values accordingly.
