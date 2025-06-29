# Staging Environment Variables

# VPC Configuration
vpc_cidr = "10.1.0.0/16"
public_subnets = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
private_subnets = ["10.1.101.0/24", "10.1.102.0/24", "10.1.103.0/24"]

# ECS Configuration
desired_count = 2
container_cpu = 512
container_memory = 1024

# RDS Configuration
db_instance_class = "db.t3.small"
db_allocated_storage = 50
multi_az = true

# Load Balancer Configuration
internal = false

# Auto Scaling
min_capacity = 2
max_capacity = 4

# Environment-specific tags
environment = "staging"

# Enable/Disable Features
enable_cloudwatch_logging = true
enable_xray_tracing = true

# Domain Configuration
# domain_name = "staging.sheily.example.com"
# zone_id = ""

# Container Images
docker_image_tag = "staging"

# Monitoring
create_cloudwatch_dashboard = true
enable_container_insights = true
