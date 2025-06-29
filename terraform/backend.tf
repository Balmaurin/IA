terraform {
  backend "s3" {
    # This will be configured when initializing the backend
    # Example configuration (uncomment and update with your values):
    # bucket         = "your-terraform-state-bucket"
    # key            = "sheily/terraform.tfstate"
    # region         = "us-east-1"
    # dynamodb_table = "terraform-lock"
    # encrypt        = true
  }
}
