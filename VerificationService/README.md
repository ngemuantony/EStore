# Verification Service

A microservice for handling verification and validation processes in the E-Store platform.

## Features
- Email verification
- Phone number verification
- Document validation
- Identity verification
- Security checks

## Database
- Uses PostgreSQL for persistent storage
- Database name: `verificationdb`
- Connection managed through SQLAlchemy with retry mechanism

## Configuration

### Environment Variables
Create a `.env` file in the VerificationService directory with:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/verificationdb
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

### Email Verification
- `POST /verify/email`: Send verification email
- `GET /verify/email/{token}`: Verify email token
- `POST /verify/email/resend`: Resend verification email

### Phone Verification
- `POST /verify/phone`: Send verification SMS
- `POST /verify/phone/confirm`: Confirm SMS code
- `POST /verify/phone/resend`: Resend verification SMS

### Document Verification
- `POST /verify/documents`: Submit documents for verification
- `GET /verify/documents/{document_id}`: Check document verification status

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
uvicorn main:app --reload --port 8003
```

### Docker
The service is containerized using Docker:
```bash
docker build -t verification-service .
docker run -p 8003:8003 verification-service
```

## Testing
Run tests with:
```bash
pytest
```

## API Documentation
Access the Swagger documentation at:
http://localhost:8003/docs

## Dependencies
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- uvicorn
