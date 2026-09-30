output "s3_bucket_name" {
  value = aws_s3_bucket.data_lake.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.metrics.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.api.name
}
