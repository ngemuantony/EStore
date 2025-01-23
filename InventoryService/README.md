# Inventory Service

A microservice for managing product inventory in the E-Store platform using Redis for real-time operations.

## Features
- Real-time inventory tracking
- Product management
- Category management
- Stock level monitoring
- Inventory alerts

## Database
- Uses Redis for fast, real-time operations
- Redis OM for object mapping
- Real-time data updates
- In-memory performance

## Configuration

### Environment Variables
Create a `.env` file in the InventoryService directory with:

```env
REDIS_HOST=your-redis-host
REDIS_PORT=your-redis-port
REDIS_PASSWORD=your-redis-password
```

### Database Connection
The service uses the shared database connection handler from `utils/database.py` which provides:
- Automatic connection retries
- Error logging
- Health checks
- Conditional Redis import

## API Endpoints

### Products
- `POST /products`: Create a new product
- `GET /products`: List all products
- `GET /products/{product_id}`: Get product details
- `PUT /products/{product_id}`: Update product
- `DELETE /products/{product_id}`: Delete product

### Inventory Management
- `PUT /products/{product_id}/stock`: Update stock level
- `GET /products/{product_id}/stock`: Get current stock
- `POST /products/bulk-update`: Bulk update stock levels

### Categories
- `POST /categories`: Create category
- `GET /categories`: List categories
- `GET /categories/{category_id}/products`: List products in category

## Development

### Running Locally
1. Ensure Redis is running
2. Set up environment variables
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the service:
```bash
uvicorn main:app --reload --port 8002
```

### Docker
The service is containerized using Docker:
```bash
docker build -t inventory-service .
docker run -p 8002:8002 inventory-service
```

## Testing
Run tests with:
```bash
pytest
```

## API Documentation
Access the Swagger documentation at:
http://localhost:8002/docs

## Dependencies
- FastAPI
- Redis
- redis-om
- Pydantic
- uvicorn
