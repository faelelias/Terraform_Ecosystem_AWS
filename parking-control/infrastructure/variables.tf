variable "aws_region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "backend_ami_id" {
  description = "ID da AMI para a instância EC2 do backend"
  type        = string
}

variable "key_name" {
  description = "Nome do par de chaves SSH para a instância EC2"
  type        = string
}

variable "db_username" {
  description = "Nome do usuário master do RDS"
  type        = string
}

variable "db_password" {
  description = "Senha do usuário master do RDS"
  type        = string
  sensitive   = true
}

variable "google_client_id" {
  description = "ID do cliente Google para SSO"
  type        = string
}

variable "google_client_secret" {
  description = "Secret do cliente Google para SSO"
  type        = string
  sensitive   = true
} 