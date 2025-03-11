output "backend_instance_ip" {
  description = "IP privado da instância EC2 do backend"
  value       = module.ec2_backend.private_ip
}

output "database_endpoint" {
  description = "Endpoint de conexão do RDS"
  value       = module.database.endpoint
}

output "storage_bucket" {
  description = "Nome do bucket S3"
  value       = module.storage.bucket_id
}

output "cognito_user_pool_id" {
  description = "ID do User Pool do Cognito"
  value       = aws_cognito_user_pool.main.id
}

output "cognito_user_pool_client_id" {
  description = "ID do Client do User Pool do Cognito"
  value       = aws_cognito_user_pool.main.id
} 