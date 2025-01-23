# Database Design

## Overview
The EStore platform uses PostgreSQL as its primary database system for all services. This decision was made to ensure data consistency, ACID compliance, and to leverage PostgreSQL's powerful features like JSONB for flexible data storage.

## Database Schema

### UserService Database (estore_users)

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);
```

#### VerificationTokens Table
```sql
CREATE TABLE verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_verification_tokens_user ON verification_tokens(user_id);
CREATE INDEX idx_verification_tokens_token ON verification_tokens(token);
```

### InventoryService Database (estore_inventory)

#### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INTEGER NOT NULL, -- Stored in cents
    quantity INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER,
    image_url VARCHAR(255),
    min_stock_level INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT fk_category
        FOREIGN KEY(category_id)
        REFERENCES categories(id)
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_metadata ON products USING gin (metadata);
```

#### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_id INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_parent
        FOREIGN KEY(parent_id)
        REFERENCES categories(id)
);

CREATE INDEX idx_categories_parent ON categories(parent_id);
```

### PaymentService Database (estore_payments)

#### PaymentMethods Table
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

CREATE INDEX idx_payment_methods_user ON payment_methods(user_id);
CREATE INDEX idx_payment_methods_active ON payment_methods(is_active);
CREATE INDEX idx_payment_methods_details ON payment_methods USING gin (details);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount INTEGER NOT NULL, -- Stored in cents
    status VARCHAR NOT NULL DEFAULT 'pending',
    payment_method_id INTEGER REFERENCES payment_methods(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT fk_payment_method
        FOREIGN KEY(payment_method_id)
        REFERENCES payment_methods(id)
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_metadata ON orders USING gin (metadata);
```

## Database Design Principles

### 1. Data Integrity
- Foreign key constraints for referential integrity
- NOT NULL constraints where appropriate
- CHECK constraints for data validation
- UNIQUE constraints for preventing duplicates

### 2. Performance Optimization
- Strategic indexing on frequently queried columns
- JSONB indices for flexible querying
- Proper data types for efficient storage
- Timestamp with time zone for temporal data

### 3. Scalability Considerations
- Partitioning ready for large tables
- Efficient indexing strategy
- Normalized structure to prevent redundancy
- JSONB for flexible schema evolution

## Backup and Recovery

### Automated Backup Strategy
```bash
# Daily backup script (backup.sh)
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d)

# Backup each database
for DB in estore_users estore_inventory estore_payments; do
    pg_dump -Fc -U postgres $DB > "$BACKUP_DIR/${DB}_${DATE}.dump"
done

# Keep last 30 days of backups
find $BACKUP_DIR -type f -mtime +30 -delete
```

### Recovery Process
```bash
# Restore a database
pg_restore -U postgres -d database_name backup_file.dump
```

## Monitoring and Maintenance

### Key Metrics to Monitor
1. Query Performance
   - Slow query log analysis
   - Index usage statistics
   - Buffer cache hit ratio

2. Database Size
   - Table sizes
   - Index sizes
   - TOAST table usage

3. Connection Stats
   - Active connections
   - Connection duration
   - Connection errors

### Regular Maintenance Tasks
```sql
-- Regular VACUUM ANALYZE
VACUUM ANALYZE;

-- Update table statistics
ANALYZE tablename;

-- Rebuild indices
REINDEX TABLE tablename;
```

## Security Measures

1. **Access Control**
   - Role-based access
   - Row-level security policies
   - SSL connections

2. **Data Protection**
   - Encrypted passwords
   - Sensitive data in JSONB fields
   - Audit logging

3. **Backup Security**
   - Encrypted backups
   - Secure backup transfer
   - Regular backup testing

## Migration Strategy

### Version Control
- All schema changes are version controlled
- Use of migration tools (Alembic)
- Rollback procedures documented

### Example Migration
```python
# alembic/versions/xxxx_add_payment_status.py
def upgrade():
    op.add_column('orders', sa.Column('payment_status', sa.String()))
    op.create_index('idx_orders_payment_status', 'orders', ['payment_status'])

def downgrade():
    op.drop_index('idx_orders_payment_status')
    op.drop_column('orders', 'payment_status')
