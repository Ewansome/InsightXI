# security_groups.tf

Security groups act as virtual firewalls, controlling what traffic can flow in and out of your resources.

## Traffic Flow

```
Internet
    │
    ▼ (port 80/443)
┌───────────┐
│    ALB    │ ◄── alb security group
└─────┬─────┘
      │ (any port, from ALB only)
      ▼
┌───────────┐
│ ECS Tasks │ ◄── ecs_tasks security group
└─────┬─────┘
      │ (port 3306, from ECS only)
      ▼
┌───────────┐
│    RDS    │ ◄── rds security group
└───────────┘
```

## Code Breakdown

### ALB Security Group

```hcl
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
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
  ...
}
```

**What:** Defines what traffic the ALB can receive and send.

**Why:**
- **Ingress (incoming)**:
  - Port 80 (HTTP) and 443 (HTTPS) from `0.0.0.0/0` (anywhere)
  - This is intentional - the ALB is the public entry point
  - Users need to reach it from the internet
- **Egress (outgoing)**:
  - `protocol = "-1"` means all protocols (TCP, UDP, ICMP, etc.)
  - `from_port = 0, to_port = 0` with protocol `-1` means all ports
  - ALB needs to forward traffic to ECS tasks on various ports
- **vpc_id**: Security groups are VPC-specific

---

### ECS Tasks Security Group

```hcl
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-${var.environment}-ecs-tasks-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "From ALB"
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description = "Inter-service communication"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    self        = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ...
}
```

**What:** Controls traffic to/from ECS containers.

**Why:**
- **First ingress rule - "From ALB"**:
  - `security_groups = [aws_security_group.alb.id]` - only accepts traffic from the ALB
  - Not from the internet directly, not from random IPs - only the ALB
  - This is the key security pattern: ALB is the gatekeeper
- **Second ingress rule - "Inter-service communication"**:
  - `self = true` means "allow traffic from other resources with this same security group"
  - Lets orchestrator-service call sportmonks-service and database-service
  - Services can talk to each other but outsiders can't
- **Egress**:
  - All outbound traffic allowed
  - ECS needs to pull images from ECR, call SportMonks API, etc.

---

### RDS Security Group

```hcl
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.environment}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "MySQL from ECS"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ...
}
```

**What:** Controls who can connect to the database.

**Why:**
- **Ingress**:
  - Only port 3306 (MySQL's default port)
  - Only from ECS tasks security group - not the ALB, not the internet
  - This is critical for database security - the DB is only accessible from your application
- **Why not allow direct access?**
  - Databases should never be publicly accessible
  - All queries go through your application which can validate/sanitise input
  - If someone compromises the ALB, they still can't directly query the database

## Security Pattern Summary

This creates a layered security model:

1. **Internet → ALB**: Only HTTP/HTTPS allowed
2. **ALB → ECS**: Only ALB can reach ECS tasks
3. **ECS → RDS**: Only ECS can reach the database

Each layer only trusts the layer above it, minimising the blast radius if any component is compromised.
