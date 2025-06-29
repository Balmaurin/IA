# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
  
  # Allow version 4.x of the AWS provider
  version = "~> 4.0"
}

# Create a VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "${var.app_name}-${var.environment}-vpc"
  cidr = var.vpc_cidr
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
  
  enable_nat_gateway = true
  single_nat_gateway = true
  
  tags = {
    Environment = var.environment
    Terraform   = "true"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-${var.environment}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Environment = var.environment
    Terraform   = "true"
  }
}

# ECR Repositories
resource "aws_ecr_repository" "api" {
  name                 = "${var.app_name}-api"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "web" {
  name                 = "${var.app_name}-web"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# RDS Database
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 5.0"
  
  identifier = "${var.app_name}-${var.environment}-db"
  
  engine               = "postgres"
  engine_version       = "15.5"
  instance_class       = var.db_instance_class
  allocated_storage    = 20
  storage_encrypted   = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = "5432"
  
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  
  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window     = "03:00-06:00"
  
  # Enhanced Monitoring - see example for details on how to create the role
  # by yourself, in case you don't want to create it automatically
  monitoring_interval = "30"
  monitoring_role_name = "MyRDSMonitoringRole"
  create_monitoring_role = true
  
  tags = {
    Environment = var.environment
    Terraform   = "true"
  }
  
  # DB subnet group
  create_db_subnet_group = true
  subnet_ids             = module.vpc.private_subnets
  
  # DB parameter group
  family = "postgres15"
  
  # DB option group
  major_engine_version = "15"
  
  # Database Deletion Protection
  deletion_protection = var.environment == "prod" ? true : false
}

# Outputs
output "ecr_api_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "ecr_web_repository_url" {
  value = aws_ecr_repository.web.repository_url
}

output "rds_endpoint" {
  value = module.db.db_instance_endpoint
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnets" {
  value = module.vpc.private_subnets
}

output "public_subnets" {
  value = module.vpc.public_subnets
}
