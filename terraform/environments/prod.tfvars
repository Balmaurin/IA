# Production Environment Variables

# VPC Configuration
vpc_cidr = "10.2.0.0/16"
public_subnets = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
private_subnets = ["10.2.101.0/24", "10.2.102.0/24", "10.2.103.0/24"]

# ECS Configuration
desired_count = 3
container_cpu = 1024
container_memory = 2048

# RDS Configuration
db_instance_class = "db.t3.medium"
db_allocated_storage = 100
multi_az = true

# Load Balancer Configuration
internal = false

# Auto Scaling
min_capacity = 3
max_capacity = 10

# Environment-specific tags
environment = "prod"

# Enable/Disable Features
enable_cloudwatch_logging = true
enable_xray_tracing = true

# Domain Configuration
# domain_name = "sheily.example.com"
# zone_id = ""

# Container Images
docker_image_tag = "latest"

# Monitoring
create_cloudwatch_dashboard = true
enable_container_insights = true
