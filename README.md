# EStore - Microservices-based E-Commerce Platform

## Overview
EStore is a modern, scalable e-commerce platform built using a microservices architecture. The system is designed to handle various aspects of e-commerce operations including user management, inventory control, payment processing, and email verification.

## Architecture
The application is divided into four main microservices:

1. **UserService**: Handles user authentication, registration, and profile management
2. **InventoryService**: Manages product inventory, categories, and search functionality
3. **PaymentService**: Processes orders, payments, and manages payment methods
4. **VerificationService**: Handles email verification and notifications

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

### Installation
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

## Documentation

For detailed documentation, please refer to the following files in the `docs` directory:

- [Database Schema and Design](docs/database.md)
- [Features and Capabilities](docs/features.md)
- [Technologies and Tools](docs/technologies.md)
- [API Endpoints](docs/endpoints.md)

## Key Features

### User Management
- User registration and authentication
- JWT-based authorization
- Email verification
- Role-based access control

### Inventory Management
- Product CRUD operations
- Category and tag management
- Advanced search and filtering
- Stock tracking and alerts
- Product analytics

### Payment Processing
- Multiple payment method support
- Order management
- Payment status tracking
- Refund processing
- Order analytics

### Security Features
- JWT authentication
- Password hashing
- Email verification
- Role-based access control
- Request validation

## API Documentation

The API documentation is available at the following endpoints when running the services:

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
- JWT for authentication
- SQLAlchemy ORM
