variable "aws_region" {
  type        = string
  description = "AWS region."
  default     = "af-south-1"
}

variable "project_name" {
  type        = string
  description = "Name prefix for AWS resources."
  default     = "affirmation-intelligence"
}

variable "container_image" {
  type        = string
  description = "Container image URI for the FastAPI service."
  default     = "public.ecr.aws/docker/library/python:3.12-slim"
}

variable "desired_count" {
  type        = number
  default     = 1
}
