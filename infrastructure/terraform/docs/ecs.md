# ecs.tf

This file creates the ECS (Elastic Container Service) cluster, task definitions, and services. ECS runs the Docker containers on AWS.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       ECS Cluster                           │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐ │
│  │ Service:        │ │ Service:        │ │ Service:      │ │
│  │ sportmonks      │ │ database        │ │ orchestrator  │ │
│  │                 │ │                 │ │               │ │
│  │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌───────────┐ │ │
│  │ │ Task        │ │ │ │ Task        │ │ │ │ Task      │ │ │
│  │ │ (Container) │ │ │ │ (Container) │ │ │ │(Container)│ │ │
│  │ │ Port 8000   │ │ │ │ Port 8001   │ │ │ │ Port 8002 │ │ │
│  │ └─────────────┘ │ │ └─────────────┘ │ │ └───────────┘ │ │
│  └─────────────────┘ └─────────────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Code Breakdown

### ECS Cluster

```hcl
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  ...
}
```

**What:** Creates the ECS cluster - a logical grouping of services.

**Why:**
- A cluster is just a namespace for the services
- `containerInsights = enabled`: Sends detailed metrics to CloudWatch
  - CPU/memory usage per container
  - Useful for debugging and scaling decisions
  - Adds ~$0.50/month per task

---

### IAM Roles

```hcl
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-${var.environment}-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
```

**What:** Two IAM roles for ECS tasks.

**Why two roles?**

1. **Execution Role** (`ecs_task_execution`):
   - Used by ECS itself (not the code)
   - Permissions to:
     - Pull images from ECR
     - Write logs to CloudWatch
     - Retrieve secrets (if using Secrets Manager)
   - The `AmazonECSTaskExecutionRolePolicy` is an AWS-managed policy with these permissions

2. **Task Role** (`ecs_task`):
   - Used by the application code
   - Would include permissions like:
     - Access S3 buckets
     - Call other AWS services
   - Currently empty, add policies as needed

**assume_role_policy:**
- This is the "trust policy" - who can assume this role
- `Principal: ecs-tasks.amazonaws.com` means only ECS can use this role
- Prevents other services/users from using it

---

### CloudWatch Log Groups

```hcl
resource "aws_cloudwatch_log_group" "services" {
  for_each = toset(["sportmonks-service", "database-service", "orchestrator-service"])

  name              = "/ecs/${var.project_name}-${var.environment}/${each.key}"
  retention_in_days = 30
  ...
}
```

**What:** Creates log groups for each service.

**Why:**
- `for_each`: Creates 3 log groups using a loop (more elegant than copy-paste)
- `retention_in_days = 30`: Auto-delete logs after 30 days
  - Prevents unbounded log storage costs
  - Increase for production if you need longer retention
- Logs are viewable in CloudWatch console or via `aws logs` CLI

---

### ECR Repository Data Sources

```hcl
data "aws_ecr_repository" "sportmonks" {
  name = "sportmonks-service"
}
```

**What:** Looks up the existing ECR repositories.

**Why:**
- These repos were created by the CD pipeline
- `data` sources read existing resources (vs `resource` which creates them)
- We need the repository URL to tell ECS where to pull images from
- If the repo doesn't exist, Terraform will error - this is a safety check

---

### Task Definitions

```hcl
resource "aws_ecs_task_definition" "sportmonks" {
  family                   = "${var.project_name}-${var.environment}-sportmonks"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name  = "sportmonks-service"
      image = "${data.aws_ecr_repository.sportmonks.repository_url}:latest"
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
      environment = [
        { name = "API_KEY", value = var.sportmonks_api_key },
        { name = "BASE_URL", value = "https://api.sportmonks.com/v3" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.services["sportmonks-service"].name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}
```

**What:** Defines how to run a container - like a docker-compose service definition.

**Why each setting:**

- `family`: Name for this task definition (versioned automatically)
- `network_mode = "awsvpc"`: Each task gets its own network interface
  - Required for Fargate
  - Allows security group attachment
- `requires_compatibilities = ["FARGATE"]`: Run on Fargate (serverless containers)
  - Alternative is "EC2" where you manage the servers
- `cpu = 256` / `memory = 512`:
  - 0.25 vCPU and 512MB RAM
  - Smallest Fargate size, ~$10/month per task
  - Fargate has specific valid combinations (can't do 256 CPU with 2GB RAM)

**Container definition:**
- `image`: Pull from ECR with `latest` tag
- `portMappings`: Expose port 8000 (matches the Dockerfile)
- `environment`: Environment variables passed to the container
  - **Security note:** For production, use Secrets Manager instead of plain text
- `logConfiguration`: Send stdout/stderr to CloudWatch
  - `awslogs-stream-prefix = "ecs"` creates streams like `ecs/sportmonks-service/abc123`

---

### ECS Services

```hcl
resource "aws_ecs_service" "sportmonks" {
  name            = "${var.project_name}-${var.environment}-sportmonks"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.sportmonks.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.sportmonks.arn
    container_name   = "sportmonks-service"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.http]
}
```

**What:** Runs and maintains tasks based on the task definition.

**Why each setting:**

- `desired_count = 1`: Run 1 instance of this task
  - Increase for high availability (2+) or to handle more load
  - ECS will maintain this count - if a task dies, it starts a new one
- `launch_type = "FARGATE"`: Serverless - no servers to manage
- **network_configuration:**
  - `subnets = private`: Tasks run in private subnets (not directly accessible from internet)
  - `security_groups`: Apply the ECS tasks security group
  - `assign_public_ip = false`: No public IPs (traffic goes through ALB)
- **load_balancer:**
  - Registers tasks with the ALB target group
  - ALB health checks determine if tasks receive traffic
- `depends_on`:
  - Wait for ALB listener to exist before creating service
  - Without this, Terraform might try to register with a non-existent target group

## Service Discovery (Future Enhancement)

Currently, the orchestrator uses hardcoded URLs. For proper service discovery, you could add:

```hcl
resource "aws_service_discovery_private_dns_namespace" "main" {
  name = "insightxi.local"
  vpc  = aws_vpc.main.id
}

resource "aws_service_discovery_service" "sportmonks" {
  name = "sportmonks"
  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id
    dns_records {
      ttl  = 10
      type = "A"
    }
  }
}
```

Then services could reach each other via `sportmonks.insightxi.local:8000`.

## Scaling (Future Enhancement)

To add auto-scaling:

```hcl
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = 4
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.sportmonks.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  name               = "cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}
```

This would scale up when CPU exceeds 70% and scale down when it drops.
