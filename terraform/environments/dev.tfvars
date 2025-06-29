# Development Environment Variables

# VPC Configuration
vpc_cidr = "10.0.0.0/16"
public_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
private_subnets = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

# ECS Configuration
desired_count = 1
container_cpu = 256
container_memory = 512

# RDS Configuration
db_instance_class = "db.t3.micro"
db_allocated_storage = 20
multi_az = false

# Load Balancer Configuration
internal = false

# Auto Scaling
min_capacity = 1
max_capacity = 2

# Environment-specific tags
environment = "dev"

# Enable/Disable Features
enable_cloudwatch_logging = true
enable_xray_tracing = true

# Domain Configuration
# domain_name = "dev.sheily.example.com"
# zone_id = ""

# Container Images
docker_image_tag = "latest"

# Monitoring
create_cloudwatch_dashboard = true
enable_container_insights = true
