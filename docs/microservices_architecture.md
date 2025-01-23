# E-Store Microservices Architecture

## Overview

The E-Store application is built using a microservices architecture, consisting of four main services:
1. User Service (Port 8002)
2. Inventory Service (Port 8001)
3. Payment Service (Port 8000)
4. Verification Service (Port 8003)

## Service Communication Flow

### Authentication Flow

```mermaid
sequenceDiagram
    Client->>UserService: Register/Login Request
    UserService->>VerificationService: Send Verification Email
    VerificationService->>Client: Email with Verification Link
    Client->>UserService: Verify Email
    UserService->>Client: JWT Token
```

1. **User Service (Port 8002)**
   - Handles user authentication and authorization
   - Issues JWT tokens for authenticated users
   - Communicates with Verification Service for email verification
   - Token is required by other services for authentication

2. **Verification Service (Port 8003)**
   - Manages email verification process
   - Sends verification emails to users
   - Validates verification tokens
   - Communicates results back to User Service

### Shopping Flow

```mermaid
sequenceDiagram
    Client->>InventoryService: Browse Products
    InventoryService->>UserService: Validate Token
    Client->>PaymentService: Create Order
    PaymentService->>InventoryService: Check Product Availability
    PaymentService->>UserService: Validate User & Payment
    PaymentService->>InventoryService: Update Inventory
    PaymentService->>Client: Order Confirmation
```

3. **Inventory Service (Port 8001)**
   - Manages product catalog and inventory
   - Validates JWT tokens with User Service
   - Communicates with Payment Service for stock updates
   - Uses Redis for fast data access and caching

4. **Payment Service (Port 8000)**
   - Handles all payment-related operations
   - Communicates with the User Service for authentication and the Inventory Service for stock verification

   ### Payment Method Creation

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

   ### Communication Flow
   - The Payment Service verifies the user's JWT token.
   - It stores payment details in Redis as a JSON string.

   ### Error Handling
   - The service returns appropriate error messages for invalid requests, including missing fields or invalid data types.

## Inter-Service Communication

### Authentication & Authorization
- All services validate JWT tokens with the User Service
- Token format: `Bearer eyJhbGciOiJIUzI1NiIs...`
- Services check user permissions before processing requests

### API Communication
- Services communicate via HTTP/REST
- Base URLs:
  ```
  User Service: http://localhost:8002
  Inventory Service: http://localhost:8001
  Payment Service: http://localhost:8000
  Verification Service: http://localhost:8003
  ```

### Data Consistency
1. **Distributed Transactions**
   - Payment Service coordinates order processing
   - Uses a two-phase approach:
     1. Verify inventory and payment
     2. Update inventory and complete payment

2. **Error Handling**
   - Services implement retry mechanisms
   - Failed transactions are rolled back
   - Error states are logged and monitored

## Database Architecture

### User Service
- PostgreSQL Database
- Stores:
  - User accounts
  - Authentication data
  - User profiles

### Inventory Service
- Redis Database
- Stores:
  - Product catalog
  - Inventory levels
  - Categories and tags

### Payment Service
- Redis Database
- Stores:
  - Orders
  - Payment methods
  - Transaction history

### Verification Service
- PostgreSQL Database
- Stores:
  - Verification tokens
  - Email templates
  - Verification status

## Security

1. **Authentication**
   - JWT-based authentication
   - Tokens expire after a set period
   - Refresh token mechanism

2. **API Security**
   - CORS protection
   - Rate limiting
   - Input validation

3. **Data Protection**
   - Encrypted communication
   - Secure password hashing
   - Payment data encryption

## Environment Variables

Each service requires specific environment variables for configuration:

```bash
# User Service (.env)
DATABASE_URL=postgresql://user:password@localhost/userdb
JWT_SECRET=your-secret-key
SERVICE_PORT=8002

# Inventory Service (.env)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=1
SERVICE_PORT=8001

# Payment Service (.env)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
SERVICE_PORT=8000

# Verification Service (.env)
DATABASE_URL=postgresql://user:password@localhost/verificationdb
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SERVICE_PORT=8003
```

## Error Handling

Services implement consistent error responses:

```json
{
    "error": "Error type",
    "message": "Detailed error message",
    "status_code": 400
}
```

Common status codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

## Monitoring and Logging

Each service implements:
- Request logging
- Error tracking
- Performance metrics
- Health check endpoints

## Scaling Considerations

The architecture supports:
1. Horizontal scaling of services
2. Load balancing
3. Cache optimization
4. Database replication

## Development Workflow

1. Start all services:
   ```bash
   # Terminal 1
   cd UserService
   uvicorn main:app --reload --port 8002

   # Terminal 2
   cd InventoryService
   uvicorn main:app --reload --port 8001

   # Terminal 3
   cd PaymentService
   uvicorn main:app --reload --port 8000

   # Terminal 4
   cd VerificationService
   uvicorn main:app --reload --port 8003
   ```

2. Ensure all environment variables are set
3. Run database migrations if needed
4. Test inter-service communication

## Testing

1. Unit Tests:
   - Individual service functionality
   - Model validation
   - Business logic

2. Integration Tests:
   - Service communication
   - Database operations
   - Authentication flow

3. End-to-End Tests:
   - Complete user journeys
   - Error scenarios
   - Performance testing
