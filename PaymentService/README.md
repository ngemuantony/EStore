# EStore Payment Service

## Project Overview

This project is part of my journey to deepen my understanding of DevOps practices and System Design principles. After extensive research through various resources including technical articles, e-books, tutorials, and system design podcasts, I decided to create this practical implementation to solidify my knowledge.

The Payment Service is a crucial microservice within the EStore ecosystem, designed to handle payment processing with a focus on scalability, reliability, and security.

## System Design & Architecture

### Microservices Architecture
The Payment Service is part of a larger microservices architecture, where each service is:
- Independently deployable
- Loosely coupled
- Highly cohesive
- Owns its own data store

### Technical Stack
- **Framework**: FastAPI - chosen for its high performance, automatic API documentation, and modern Python features
- **Database**: PostgreSQL - selected for:
  - ACID compliance
  - Complex query support (especially JSONB for flexible payment details)
  - Data integrity and reliability
  - Robust transaction support
- **API Design**: RESTful principles with clear resource naming and HTTP method usage
- **Authentication**: JWT-based authentication (planned)
- **Documentation**: OpenAPI (Swagger) specification

### Design Patterns & Best Practices
- **Repository Pattern**: Separation of data access logic (crud.py)
- **DTO Pattern**: Clear separation of API models (schemas.py) from database models (models.py)
- **Dependency Injection**: For database sessions and future authentication
- **SOLID Principles**: Emphasis on Single Responsibility and Interface Segregation

## Features

- Payment Method Management (CRUD operations)
- Order Processing
- PostgreSQL Database Integration
- Duplicate Payment Method Prevention
- JWT Authentication (planned)

## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual Environment (recommended)

## Environment Setup

Create a `.env` file in the root directory with:

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

## API Documentation

### Payment Methods

- `POST /payment-methods`: Create a new payment method
  - Implements duplicate detection for card numbers
  - Validates payment method details
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

## Future Enhancements

1. **Security Improvements**
   - Implement rate limiting
   - Add request validation middleware
   - Enhanced error handling

2. **Monitoring & Observability**
   - Prometheus metrics integration
   - Grafana dashboards
   - Distributed tracing

3. **Infrastructure**
   - Docker containerization
   - Kubernetes deployment
   - CI/CD pipeline with GitHub Actions

4. **Payment Gateway Integration**
   - Stripe integration
   - PayPal integration
   - Support for multiple payment providers

## Learning Resources

Some valuable resources that influenced this project's design:

1. **System Design**
   - "Designing Data-Intensive Applications" by Martin Kleppmann
   - System Design Primer (GitHub)
   - Various tech blog posts from companies like Uber, Netflix, and Stripe

2. **DevOps Practices**
   - The DevOps Handbook
   - Container and Kubernetes documentation
   - CI/CD best practices

3. **Microservices Architecture**
   - "Building Microservices" by Sam Newman
   - Microsoft's microservices architecture documentation
   - Netflix's tech blog

## Error Handling

The service implements standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Contributing

Feel free to submit issues and enhancement requests!
