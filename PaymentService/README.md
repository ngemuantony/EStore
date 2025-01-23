# Payment Service

A microservice for handling payment methods and orders in the EStore application.

## Features

- Payment Method Management (CRUD operations)
- Order Processing
- PostgreSQL Database Integration
- JWT Authentication

## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual Environment (recommended)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/estore_payments
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create the database:
```sql
CREATE DATABASE estore_payments;
```

4. Start the server:
```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

### Payment Methods

- `POST /payment-methods`: Create a new payment method
- `GET /payment-methods`: List all payment methods for a user
- `GET /payment-methods/{id}`: Get a specific payment method
- `DELETE /payment-methods/{id}`: Delete a payment method

### Orders

- `POST /orders`: Create a new order
- `GET /orders`: List all orders for a user
- `GET /orders/{id}`: Get a specific order
- `PUT /orders/{id}/status`: Update order status

## Database Schema

### Payment Methods
```sql
CREATE TABLE payment_methods (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    payment_type VARCHAR NOT NULL,
    details JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Orders
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount INTEGER NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'pending',
    payment_method_id INTEGER REFERENCES payment_methods(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Error Handling

The service implements standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
