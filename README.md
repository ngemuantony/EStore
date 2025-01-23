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
