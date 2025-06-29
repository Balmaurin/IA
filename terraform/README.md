# Sheily Infrastructure as Code

This directory contains the Terraform configuration for deploying the Sheily application to AWS.

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) (>= 1.0.0)
2. [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate credentials
3. S3 bucket for storing Terraform state
4. DynamoDB table for state locking

## Directory Structure

```
terraform/
├── main.tf              # Main Terraform configuration
├── variables.tf         # Variable declarations
├── outputs.tf           # Output values
├── backend.tf           # Backend configuration
├── environments/        # Environment-specific variable files
│   ├── dev.tfvars      # Development environment
│   ├── staging.tfvars  # Staging environment
│   └── prod.tfvars     # Production environment
└── modules/            # Reusable Terraform modules
    ├── vpc/           # VPC and networking
    ├── ecs/           # ECS cluster and services
    ├── rds/           # Database configuration
    └── monitoring/    # CloudWatch and monitoring
```

## Getting Started

### 1. Configure the Backend

Update the `backend.tf` file with your S3 bucket and DynamoDB table names:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "sheily/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. Select Workspace

```bash
# For development
terraform workspace select dev || terraform workspace new dev

# For staging
terraform workspace select staging || terraform workspace new staging

# For production
terraform workspace select prod || terraform workspace new prod
```

### 4. Plan Changes

```bash
# For development
terraform plan -var-file=environments/dev.tfvars

# For staging
terraform plan -var-file=environments/staging.tfvars

# For production
terraform plan -var-file=environments/prod.tfvars
```

### 5. Apply Changes

```bash
# For development
terraform apply -var-file=environments/dev.tfvars

# For staging (requires confirmation)
terraform apply -var-file=environments/staging.tfvars

# For production (requires confirmation)
terraform apply -var-file=environments/prod.tfvars
```

## CI/CD Integration

The GitHub Actions workflow will automatically handle Terraform plans and applies based on the branch:

- **Feature Branches**: No automatic Terraform execution
- **Develop Branch**: Auto-plan for staging environment
- **Main Branch**: Auto-apply for production (with approval)

## Environment Variables

### Required Variables

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_DEFAULT_REGION`: AWS region (e.g., us-east-1)

### Optional Variables

- `TF_VAR_environment`: Environment name (dev/staging/prod)
- `TF_VAR_domain_name`: Custom domain name
- `TF_VAR_zone_id`: Route53 zone ID for DNS records

## Security Considerations

1. **Secrets Management**:
   - Use AWS Secrets Manager or Parameter Store for sensitive data
   - Never commit secrets to version control

2. **Least Privilege**:
   - Use IAM roles with minimal required permissions
   - Follow the principle of least privilege

3. **Network Security**:
   - Use private subnets for application instances
   - Restrict database access to application subnets
   - Enable VPC Flow Logs for monitoring

## Monitoring and Logging

- **CloudWatch Logs**: Application and system logs
- **CloudWatch Metrics**: Performance and resource utilization
- **X-Ray**: Distributed tracing for microservices
- **Container Insights**: Container performance monitoring

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify AWS credentials are correctly configured
   - Check IAM permissions for the Terraform user

2. **State Locking Issues**:
   - Check DynamoDB table for stale locks
   - Use `terraform force-unlock` if needed

3. **Resource Creation Failures**:
   - Check AWS service limits
   - Verify VPC and subnet configurations

### Debugging

Enable debug logging:

```bash
TF_LOG=DEBUG terraform plan
```

## Cleanup

To destroy all resources (use with caution):

```bash
# For development
terraform destroy -var-file=environments/dev.tfvars

# For staging
terraform destroy -var-file=environments/staging.tfvars

# For production (be extremely careful)
terraform destroy -var-file=environments/prod.tfvars
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
