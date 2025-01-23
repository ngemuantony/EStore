# EStore - Microservices-based E-Commerce Platform

## Project Context
This project represents my journey in learning and implementing modern system design principles, DevOps practices, and microservices architecture. After extensive research through technical articles, e-books, tutorials, and system design podcasts, I created this practical implementation to solidify my understanding of large-scale system architecture.

## System Architecture Overview

### High-Level Design
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│  Load Balancer  │────▶│   Service Mesh  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  UserService    │     │InventoryService │     │ PaymentService  │
│  Port: 8002     │     │  Port: 8001     │     │  Port: 8000     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  User Database  │     │    Inventory    │     │    Payment      │
│   (PostgreSQL)  │     │    Database     │     │    Database     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Microservices Architecture
The application is built using a microservices architecture with the following core services:

1. **UserService** (Port 8002)
   - User authentication and authorization
   - Profile management
   - Role-based access control
   - Database: PostgreSQL
   - Key Features:
     * JWT-based authentication
     * Password hashing with bcrypt
     * Email verification
     * Session management

2. **InventoryService** (Port 8001)
   - Product management
   - Inventory tracking
   - Category management
   - Search functionality
   - Database: PostgreSQL
   - Key Features:
     * Real-time stock updates
     * Product categorization
     * Advanced search with filters
     * Price management
     * Image handling

3. **PaymentService** (Port 8000)
   - Payment processing
   - Order management
   - Payment method handling
   - Database: PostgreSQL
   - Key Features:
     * Multiple payment methods
     * Order tracking
     * Refund processing
     * Payment verification
     * Duplicate prevention

4. **VerificationService** (Port 8003)
   - Email verification
   - Notification handling
   - Communication management
   - Database: PostgreSQL
   - Key Features:
     * Email verification
     * Notification templates
     * Rate limiting
     * Queue management

### Technical Stack

#### Backend
- **Framework**: FastAPI
  * High performance
  * Automatic API documentation
  * Modern Python features
  * Async support
  
- **Databases**:
  * PostgreSQL (Primary data store)
    - ACID compliance
    - Complex queries
    - Data integrity
    - Transaction support
  * Redis (Caching)
    - Session management
    - Rate limiting
    - Real-time features

- **Authentication**:
  * JWT tokens
  * OAuth2 (planned)
  * Role-based access

#### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes (planned)
- **CI/CD**: GitHub Actions (planned)
- **Monitoring**: 
  * Prometheus
  * Grafana
  * ELK Stack

### Design Patterns & Principles

1. **Architectural Patterns**
   - Microservices Architecture
   - Event-Driven Architecture
   - Repository Pattern
   - CQRS (planned)

2. **Design Principles**
   - SOLID Principles
   - DRY (Don't Repeat Yourself)
   - KISS (Keep It Simple, Stupid)
   - Separation of Concerns

3. **Database Patterns**
   - Database per Service
   - Event Sourcing
   - Saga Pattern for Distributed Transactions

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- SMTP Server (for email verification)

### Environment Setup
Each service requires its own environment variables. Check the respective `.env` files in each service directory.

Example `.env` for UserService:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/estore_users
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

### Installation Steps
1. Clone the repository
```bash
git clone https://github.com/yourusername/estore.git
cd estore
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies for each service
```bash
cd UserService && pip install -r requirements.txt
cd ../InventoryService && pip install -r requirements.txt
cd ../PaymentService && pip install -r requirements.txt
cd ../VerificationService && pip install -r requirements.txt
```

4. Start the services
```bash
# In separate terminals
uvicorn UserService.main:app --reload --port 8002
uvicorn InventoryService.main:app --reload --port 8001
uvicorn PaymentService.main:app --reload --port 8000
uvicorn VerificationService.main:app --reload --port 8003
```

## System Capabilities

### Core Features
1. **User Management**
   - Registration and authentication
   - Profile management
   - Role-based access control
   - Password recovery

2. **Inventory Management**
   - Product CRUD operations
   - Category management
   - Stock tracking
   - Search and filtering

3. **Payment Processing**
   - Multiple payment methods
   - Order management
   - Refund processing
   - Payment verification

4. **Communication**
   - Email verification
   - Order notifications
   - System alerts
   - User communications

### Security Features
- JWT authentication
- Password hashing
- Rate limiting
- Input validation
- CORS protection
- SQL injection prevention

### Scalability Features
- Horizontal scaling capability
- Load balancing
- Caching strategies
- Database optimization
- Async operations

## Future Roadmap

### Phase 1: Core Infrastructure
- [x] Basic microservices setup
- [x] Database integration
- [x] API documentation
- [ ] Service discovery

### Phase 2: Advanced Features
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Performance optimization

### Phase 3: Production Readiness
- [ ] Security hardening
- [ ] Scalability testing
- [ ] Disaster recovery
- [ ] Documentation completion

## Learning Resources

### System Design
- "Designing Data-Intensive Applications" by Martin Kleppmann
- System Design Primer (GitHub)
- Tech blogs: Uber, Netflix, Stripe

### DevOps Practices
- The DevOps Handbook
- Kubernetes Documentation
- CI/CD Best Practices

### Microservices
- "Building Microservices" by Sam Newman
- Microsoft's Architecture Guides
- Netflix Tech Blog

## API Documentation

Each service provides its own Swagger documentation:
- UserService: `http://localhost:8002/docs`
- InventoryService: `http://localhost:8001/docs`
- PaymentService: `http://localhost:8000/docs`
- VerificationService: `http://localhost:8003/docs`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- FastAPI framework
- PostgreSQL
- Redis
- JWT
- SQLAlchemy

# E-Store Microservices

A modern e-commerce platform built with microservices architecture using FastAPI and Docker.

## Services

### User Service
- Handles user authentication and management
- Port: 8000
- Database: PostgreSQL (userdb)

### Payment Service
- Manages payment processing and transactions
- Port: 8001
- Database: PostgreSQL (paymentdb)

### Inventory Service
- Manages product inventory and stock levels
- Port: 8002
- Database: Redis
- Features:
  - Real-time inventory tracking
  - Product categorization
  - Stock level management

### Verification Service
- Handles verification and validation processes
- Port: 8003
- Database: PostgreSQL (verificationdb)

## Database Architecture

The platform uses a polyglot persistence approach:

- **PostgreSQL**: Used by User, Payment, and Verification services for persistent data storage
  - Connection managed through SQLAlchemy
  - Automatic retry mechanism for reliability
  - Environment variables for configuration:
    - `DATABASE_URL`: Connection string for PostgreSQL
    - `MAX_DB_RETRIES`: Maximum connection attempts (default: 5)
    - `DB_RETRY_INTERVAL`: Seconds between retries (default: 5)

- **Redis**: Used by Inventory Service for fast, real-time operations
  - Connection managed through redis-om
  - Environment variables for configuration:
    - `REDIS_HOST`: Redis server hostname
    - `REDIS_PORT`: Redis server port
    - `REDIS_PASSWORD`: Authentication password

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd EStore
```

2. Create `.env` files for each service in their respective directories:
```
UserService/.env
PaymentService/.env
InventoryService/.env
VerificationService/.env
```

3. Configure environment variables in each `.env` file:

For services using PostgreSQL:
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/[service-specific-db]
MAX_DB_RETRIES=10
DB_RETRY_INTERVAL=5
```

For Inventory Service:
```env
REDIS_HOST=your-redis-host
REDIS_PORT=your-redis-port
REDIS_PASSWORD=your-redis-password
```

4. Build and run the services:
```bash
docker-compose up --build
```

## API Documentation

Once the services are running, you can access their Swagger documentation:

- User Service: http://localhost:8000/docs
- Payment Service: http://localhost:8001/docs
- Inventory Service: http://localhost:8002/docs
- Verification Service: http://localhost:8003/docs

## Development

### Database Connections
The platform uses a robust database connection handler (`utils/database.py`) that:
- Supports both Redis and PostgreSQL
- Implements retry logic for reliability
- Uses environment variables for configuration
- Provides detailed logging
- Conditionally imports dependencies based on the database type

### Adding New Services
1. Create a new directory for your service
2. Copy the base Dockerfile structure
3. Add service configuration to docker-compose.yml
4. Create a .env file for service-specific configuration
5. Implement the service using FastAPI

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.
