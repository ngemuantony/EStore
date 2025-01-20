# API Endpoints Documentation

## UserService (Port 8002)

### Authentication Endpoints
```http
POST /register
{
    "email": "string",
    "password": "string"
}

POST /token
{
    "username": "string",
    "password": "string"
}

POST /refresh-token
{
    "refresh_token": "string"
}
```

### User Management
```http
GET /users/me
Authorization: Bearer {token}

PUT /users/me
Authorization: Bearer {token}
{
    "email": "string",
    "password": "string"
}

POST /users/verify/{token}

POST /users/resend-verification
Authorization: Bearer {token}
```

### Admin Endpoints
```http
GET /users
Authorization: Bearer {token}

GET /users/{user_id}
Authorization: Bearer {token}

DELETE /users/{user_id}
Authorization: Bearer {token}
```

## InventoryService (Port 8001)

### Product Management
```http
GET /products
Authorization: Bearer {token}
Query Parameters:
- name: string
- category_id: string
- min_price: float
- max_price: float
- tags: List[string]
- in_stock: boolean

POST /products
Authorization: Bearer {token}
{
    "name": "string",
    "price": float,
    "quantity": int,
    "category_id": "string",
    "description": "string",
    "tags": ["string"],
    "image_url": "string",
    "min_stock_level": int,
    "discount_percentage": float
}

GET /products/{product_id}
Authorization: Bearer {token}

DELETE /products/{product_id}
Authorization: Bearer {token}

PATCH /products/{product_id}/quantity
Authorization: Bearer {token}
{
    "quantity": int
}
```

### Category Management
```http
POST /categories
Authorization: Bearer {token}
{
    "name": "string",
    "description": "string",
    "parent_id": "string"
}

GET /categories
Authorization: Bearer {token}
```

### Tag Management
```http
POST /tags
Authorization: Bearer {token}
{
    "name": "string"
}

GET /tags
Authorization: Bearer {token}
```

## PaymentService (Port 8000)

### Payment Methods
```http
POST /payment-methods
Authorization: Bearer {token}
{
    "type": "string",
    "details": {
        "key": "value"
    }
}

GET /payment-methods
Authorization: Bearer {token}

DELETE /payment-methods/{payment_method_id}
Authorization: Bearer {token}
```

### Order Management
```http
POST /orders
Authorization: Bearer {token}
{
    "id": "string",
    "quantity": int,
    "payment_method_id": "string"
}

GET /orders
Authorization: Bearer {token}

GET /orders/{order_id}
Authorization: Bearer {token}

PATCH /orders/{order_id}/status
Authorization: Bearer {token}
{
    "status": "string",
    "note": "string"
}

POST /orders/{order_id}/process-payment
Authorization: Bearer {token}

POST /orders/{order_id}/refund
Authorization: Bearer {token}
{
    "amount": float,
    "reason": "string"
}
```

## VerificationService (Port 8003)

### Email Verification
```http
POST /verify
{
    "token": "string"
}

POST /resend
{
    "email": "string"
}
```

### Notification Endpoints
```http
POST /notify/order-confirmation
{
    "order_id": "string",
    "user_email": "string"
}

POST /notify/payment-confirmation
{
    "order_id": "string",
    "user_email": "string"
}

POST /notify/low-stock
{
    "product_id": "string",
    "quantity": int,
    "admin_email": "string"
}
```

## Common Response Formats

### Success Response
```json
{
    "status": "success",
    "data": {
        // Response data
    }
}
```

### Error Response
```json
{
    "status": "error",
    "detail": "Error message"
}
```

### Validation Error
```json
{
    "status": "error",
    "detail": {
        "loc": ["field_name"],
        "msg": "Error message",
        "type": "validation_error"
    }
}
```

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Rate Limiting

- Anonymous requests: 100 requests per hour
- Authenticated requests: 1000 requests per hour
- Admin requests: 5000 requests per hour

## Pagination

For endpoints that return lists, use the following query parameters:
```http
GET /endpoint?skip=0&limit=10
```

## Filtering and Sorting

For endpoints that support filtering:
```http
GET /endpoint?field=value&sort=field&order=asc
```

## Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 429: Too Many Requests
- 500: Internal Server Error
