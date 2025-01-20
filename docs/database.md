# Database Design

## Overview
The EStore platform uses a combination of PostgreSQL and Redis databases to handle different aspects of the system. PostgreSQL is used for persistent data storage (users, verification tokens), while Redis is used for high-performance data access (products, orders).

## Database Schema

### UserService (PostgreSQL)

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### VerificationTokens Table
```sql
CREATE TABLE verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
```

### InventoryService (Redis)

#### Product Model
```python
{
    "id": str,
    "name": str,
    "price": float,
    "quantity": int,
    "created_by": int,
    "category_id": Optional[str],
    "description": Optional[str],
    "tags": List[str],
    "image_url": Optional[str],
    "min_stock_level": Optional[int],
    "discount_percentage": Optional[float],
    "created_at": datetime,
    "updated_at": Optional[datetime]
}
```

#### Category Model
```python
{
    "id": str,
    "name": str,
    "description": Optional[str],
    "parent_id": Optional[str]
}
```

#### ProductAnalytics Model
```python
{
    "product_id": str,
    "views": int,
    "last_viewed": Optional[datetime],
    "stock_updates": int,
    "last_stock_update": Optional[datetime]
}
```

### PaymentService (Redis)

#### Order Model
```python
{
    "id": str,
    "product_id": str,
    "user_id": int,
    "quantity": int,
    "price": float,
    "fee": float,
    "total": float,
    "status": str,
    "payment_method_id": Optional[str],
    "created_at": datetime,
    "updated_at": Optional[datetime],
    "notes": List[str],
    "refund_amount": Optional[float],
    "payment_status": str,
    "payment_error": Optional[str]
}
```

#### PaymentMethod Model
```python
{
    "id": str,
    "user_id": int,
    "type": str,
    "details": Dict,
    "created_at": datetime
}
```

## Database Choice Rationale

### PostgreSQL
- Used for UserService due to:
  - ACID compliance for critical user data
  - Complex querying capabilities
  - Strong data consistency
  - Built-in support for relationships
  - Robust security features

### Redis
- Used for InventoryService and PaymentService due to:
  - High-performance read/write operations
  - In-memory data storage for fast access
  - Support for complex data structures
  - Built-in expiration functionality
  - Pub/Sub capabilities for real-time updates

## Backup and Recovery

### PostgreSQL Backup
```bash
# Daily backup
pg_dump -U postgres estore_users > backup_users_$(date +%Y%m%d).sql
```

### Redis Backup
Redis persistence is configured using both RDB and AOF:
```conf
# RDB Snapshot
save 900 1
save 300 10
save 60 10000

# AOF Configuration
appendonly yes
appendfsync everysec
```

## Scaling Considerations

### PostgreSQL
- Implement connection pooling
- Use read replicas for scaling reads
- Partition large tables
- Regular index optimization

### Redis
- Redis Cluster for horizontal scaling
- Redis Sentinel for high availability
- Implement proper key expiration policies
- Use Redis Enterprise for advanced features
