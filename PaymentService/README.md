# Payment Service

A microservice for handling payment processing in the E-Store platform.

## Features
- Payment processing
- Transaction history
- Refund management
- Payment status tracking

## Database
- Uses PostgreSQL for persistent storage
- Database name: `paymentdb`
- Connection managed through SQLAlchemy with retry mechanism

## Configuration

### Environment Variables
Create a `.env` file in the PaymentService directory with:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/paymentdb
MAX_DB_RETRIES=10
DB_RETRY_INTERVAL=5
```

### Database Connection
The service uses the shared database connection handler from `utils/database.py` which provides:
- Automatic connection retries
- Connection pooling
- Error logging
- Health checks

## API Endpoints

### Payment Processing
- `POST /payments/process`: Process a new payment
- `GET /payments/{payment_id}`: Get payment details
- `POST /payments/{payment_id}/refund`: Process a refund

### Transaction History
- `GET /transactions`: List all transactions
- `GET /transactions/{transaction_id}`: Get transaction details

## Development

### Running Locally
1. Ensure PostgreSQL is running
2. Set up environment variables
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the service:
```bash
uvicorn main:app --reload --port 8001
```

### Docker
The service is containerized using Docker:
```bash
docker build -t payment-service .
docker run -p 8001:8001 payment-service
```

## Testing
Run tests with:
```bash
pytest
```

## API Documentation
Access the Swagger documentation at:
http://localhost:8001/docs

## Dependencies
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- uvicorn
