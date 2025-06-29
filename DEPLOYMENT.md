# Sheily Light - Deployment Guide

This document provides instructions for deploying the Sheily Light application across different environments.

## Prerequisites

- Docker and Docker Compose
- AWS Account with appropriate permissions
- Terraform (for infrastructure as code)
- Node.js and npm (for frontend development)
- Python 3.9+ (for backend development)

## Local Development

### Using Docker Compose (Recommended)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your local configuration

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - PGAdmin: http://localhost:5050 (if enabled)

### Manual Setup

#### Backend

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r apps/sheily_light_api/requirements.txt
   ```

3. Set environment variables (copy from `.env.example`)

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn sheily_main_api:app --reload
   ```

#### Frontend

1. Install dependencies:
   ```bash
   cd web
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Production Deployment

### Infrastructure Setup

1. **Initialize Terraform** (first time only):
   ```bash
   cd terraform
   terraform init
   ```

2. **Plan and Apply Infrastructure** (for each environment):
   ```bash
   terraform workspace select dev  # or staging/prod
   terraform plan -var-file=environments/dev.tfvars
   terraform apply -var-file=environments/dev.tfvars
   ```

### CI/CD Pipeline

The GitHub Actions workflows will automatically handle:

1. **On Push to `main` branch**:
   - Run tests
   - Build and push Docker images to ECR
   - Deploy to the production environment

2. **On Pull Requests**:
   - Run tests and linting
   - Create a preview environment for review

### Manual Deployment

1. Build and push Docker images:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml push
   ```

2. Deploy to production:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Environment Variables

See `.env.example` for all available environment variables.

## Monitoring and Logging

- **Application Logs**: Check container logs with `docker-compose logs -f`
- **AWS CloudWatch**: Centralized logging for production environments
- **Sentry**: Error tracking (if configured)

## Backup and Recovery

### Database Backups

Automated daily backups are configured with AWS RDS. Manual snapshots can be created via the AWS Console.

### Restore from Backup

1. Create a new database from the latest snapshot
2. Update the `DATABASE_URL` in your environment variables
3. Restart the application

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify the database is running
   - Check connection string in environment variables
   - Ensure network connectivity between services

2. **Build Failures**:
   - Check for missing dependencies
   - Verify Docker build context and paths

3. **Deployment Failures**:
   - Check GitHub Actions logs
   - Verify IAM permissions
   - Check resource limits in AWS

## Security

- All sensitive data is stored in AWS Secrets Manager
- Database connections use SSL
- Regular security scans are performed by GitHub Actions

## Scaling

### Horizontal Scaling

1. **API Servers**:
   - Update the desired count in the ECS service
   - Configure auto-scaling policies

2. **Database**:
   - Enable read replicas for read-heavy workloads
   - Consider Aurora Serverless for variable workloads

## Maintenance

### Upgrading

1. Pull the latest changes
2. Update dependencies:
   ```bash
   pip install -r requirements.txt
   cd web && npm install
   ```
3. Run migrations if needed
4. Restart services

### Monitoring

- **Infrastructure**: AWS CloudWatch
- **Application**: Custom metrics and logs
- **Performance**: AWS X-Ray for distributed tracing

## Contact

For support, please contact the development team at [your-email@example.com](mailto:your-email@example.com)
