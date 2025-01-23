# Docker Guide for EStore Microservices

This guide provides detailed information about running and managing the EStore microservices using Docker.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Docker Architecture](#docker-architecture)
- [Getting Started](#getting-started)
- [Service Configuration](#service-configuration)
- [Common Operations](#common-operations)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)
- [Production Deployment](#production-deployment)

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose (included in Docker Desktop)
- Git (for version control)

## Docker Architecture

Each microservice in EStore has its own Docker container:

```plaintext
┌─────────────────────────────────────────────────────────┐
│                   Docker Environment                     │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │UserService  │  │PaymentService│  │InventoryService│  │
│  │ Port: 8000  │  │  Port: 8001 │  │   Port: 8002  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  ┌─────────────┐  ┌─────────────────────────┐          │
│  │Verification │  │     PostgreSQL DB        │          │
│  │   Service   │  │ (Shared Database Server) │          │
│  │ Port: 8003  │  │      Port: 5432         │          │
│  └─────────────┘  └─────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd EStore
   ```

2. **Environment Setup**
   - Copy the example environment files:
     ```bash
     cp UserService/.env.example UserService/.env
     cp PaymentService/.env.example PaymentService/.env
     cp InventoryService/.env.example InventoryService/.env
     cp VerificationService/.env.example VerificationService/.env
     ```
   - Update the environment variables in each .env file

3. **Build and Start Services**
   ```bash
   docker-compose up --build
   ```

4. **Verify Installation**
   Access the service endpoints:
   - UserService: http://localhost:8000/docs
   - PaymentService: http://localhost:8001/docs
   - InventoryService: http://localhost:8002/docs
   - VerificationService: http://localhost:8003/docs

## Service Configuration

### Docker Compose Configuration
The `docker-compose.yml` file defines all services and their configurations:

- **UserService**: Authentication and user management
  - Port: 8000
  - Environment variables:
    - DATABASE_URL
    - SECRET_KEY
    - ALGORITHM

- **PaymentService**: Payment processing
  - Port: 8001
  - Environment variables:
    - DATABASE_URL
    - PAYMENT_API_KEY

- **InventoryService**: Product and inventory management
  - Port: 8002
  - Environment variables:
    - DATABASE_URL
    - STORAGE_PATH

- **VerificationService**: Email and notification handling
  - Port: 8003
  - Environment variables:
    - DATABASE_URL
    - SMTP_HOST
    - SMTP_PORT

### Database Configuration
PostgreSQL database configuration in docker-compose.yml:
```yaml
db:
  image: postgres:15
  environment:
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

## Common Operations

### Starting Services
```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# Start specific service
docker-compose up user-service
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop user-service
```

### Viewing Logs
```bash
# View all logs
docker-compose logs

# Follow log output
docker-compose logs -f

# View specific service logs
docker-compose logs user-service
```

### Managing Containers
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Remove all stopped containers
docker container prune
```

### Managing Images
```bash
# List images
docker images

# Remove unused images
docker image prune

# Remove all images
docker image prune -a
```

## Troubleshooting

### Common Issues and Solutions

1. **Port Conflicts**
   - Error: "port is already allocated"
   - Solution: Stop conflicting services or change port mapping in docker-compose.yml

2. **Database Connection Issues**
   - Error: "connection refused"
   - Solutions:
     - Check if database container is running
     - Verify database credentials
     - Ensure database initialization is complete

3. **Container Start Failures**
   - Error: "exit code 1"
   - Solutions:
     - Check service logs: `docker-compose logs [service-name]`
     - Verify environment variables
     - Check disk space

4. **Volume Permissions**
   - Error: "permission denied"
   - Solution: Check volume permissions and ownership

### Debug Commands
```bash
# Check container health
docker inspect [container-id]

# View container resources
docker stats

# Execute command in container
docker-compose exec [service] [command]
```

## Development Workflow

1. **Making Code Changes**
   - Edit code in your local environment
   - Rebuild affected service:
     ```bash
     docker-compose up --build [service-name]
     ```

2. **Testing Changes**
   - Run tests inside container:
     ```bash
     docker-compose exec [service] python -m pytest
     ```

3. **Debugging**
   - Access container shell:
     ```bash
     docker-compose exec [service] /bin/bash
     ```
   - View real-time logs:
     ```bash
     docker-compose logs -f [service]
     ```

## Production Deployment

### Security Considerations
1. Use production-grade environment variables
2. Never expose database ports in production
3. Use secure networks between services
4. Implement health checks
5. Set up monitoring and logging

### Performance Optimization
1. Use multi-stage builds
2. Optimize Docker image sizes
3. Implement caching strategies
4. Configure appropriate resource limits

### Deployment Checklist
- [ ] Update all environment variables
- [ ] Configure production database settings
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerting
- [ ] Review security settings
- [ ] Test all service integrations
