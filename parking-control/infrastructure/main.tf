terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC e Subnets (usando módulo existente ou criando novo)
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "parking-control-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# Backend EC2
module "ec2_backend" {
  source = "../../modules/ec2-linux"

  ami_id        = var.backend_ami_id
  instance_type = "t3.small"
  subnet_id     = module.vpc.private_subnets[0]
  
  instance_name = "parking-control-backend"
  key_name      = var.key_name

  security_group_ids = [aws_security_group.backend.id]
  
  root_volume_size = 20
  
  tags = {
    Environment = var.environment
    Project     = "parking-control"
  }
}

# RDS MySQL
module "database" {
  source = "../../modules/rds-mysql"

  identifier        = "parking-control-db"
  database_name     = "parking_control"
  username         = var.db_username
  password         = var.db_password

  instance_class    = "db.t3.small"
  allocated_storage = 20

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  skip_final_snapshot = true

  tags = {
    Environment = var.environment
    Project     = "parking-control"
  }
}

# S3 Buckets
module "storage" {
  source = "../../modules/s3"

  bucket_name = "parking-control-storage-${var.environment}"
  
  enable_versioning    = true
  block_public_access = true

  tags = {
    Environment = var.environment
    Project     = "parking-control"
  }
}

# Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "parking-control-users"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  schema {
    name                = "apartment"
    attribute_data_type = "String"
    required           = true
    mutable            = true
    string_attribute_constraints {
      min_length = 1
      max_length = 10
    }
  }
}

# Cognito Identity Provider (Google)
resource "aws_cognito_user_pool_identity_provider" "google" {
  user_pool_id  = aws_cognito_user_pool.main.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    client_id     = var.google_client_id
    client_secret = var.google_client_secret
    authorize_scopes = "email profile openid"
  }

  attribute_mapping = {
    email    = "email"
    username = "sub"
  }
}

# Security Groups
resource "aws_security_group" "backend" {
  name        = "parking-control-backend"
  description = "Security group for backend EC2"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "database" {
  name        = "parking-control-database"
  description = "Security group for RDS"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "parking-control"
  subnet_ids = module.vpc.private_subnets
} 