# Infrastructure

Terraform configuration for deploying InsightXI to AWS.

## Architecture

- **VPC** with public and private subnets across 2 AZs
- **ALB** for load balancing with path-based routing
- **ECS Fargate** for running containerised services
- **RDS MySQL** for the database

## Prerequisites

1. AWS CLI configured
2. Terraform installed (`brew install terraform`)
3. ECR repositories created (done via CD pipeline)

## Usage

```bash
cd infrastructure/terraform

# Create terraform.tfvars from example
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Initialise Terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

## Variables

| Variable | Description |
|----------|-------------|
| `aws_region` | AWS region (default: eu-west-2) |
| `project_name` | Project name for resource naming |
| `environment` | Environment (dev/staging/prod) |
| `db_username` | RDS master username |
| `db_password` | RDS master password |
| `sportmonks_api_key` | SportMonks API key |

## Outputs

After applying, Terraform will output:
- `alb_dns_name` - URL to access the application
- `rds_endpoint` - Database connection endpoint
- `ecs_cluster_name` - ECS cluster name
