# alb.tf

This file creates the Application Load Balancer (ALB) - an **internal** load balancer that distributes requests across ECS tasks. It's not publicly accessible; all traffic comes through API Gateway.

## Traffic Flow

```
Internet
    │
    ▼
┌─────────────────┐
│  API Gateway    │  ◄── Public entry point
└────────┬────────┘
         │ VPC Link
         ▼
┌─────────────────┐
│  Internal ALB   │  ◄── This file
└────────┬────────┘
         │
   ┌─────┼─────┐
   ▼     ▼     ▼
 Orch  Sport  DB
 Svc   Monks  Svc
```

## Code Breakdown

### Application Load Balancer

```hcl
resource "aws_lb" "main" {
  name               = "${var.project_name}-${var.environment}-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-${var.environment}-alb"
  }
}
```

**What:** Creates the load balancer itself.

**Why:**
- `internal = true`: Only accessible within the VPC (via API Gateway VPC Link)
  - `internal = false` would make it internet-facing
- `load_balancer_type = "application"`:
  - Layer 7 (HTTP/HTTPS) load balancer
  - Can route based on URL paths, headers, etc.
  - Alternative is "network" (Layer 4, TCP/UDP) - faster but less flexible
- `security_groups`: Controls what traffic reaches the ALB (port 80 from within VPC only)
- `subnets`: Placed in private subnets since it's internal

---

### Target Groups

```hcl
resource "aws_lb_target_group" "orchestrator" {
  name        = "${var.project_name}-${var.environment}-orch-tg"
  port        = 8002
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    timeout             = 5
    unhealthy_threshold = 3
  }
  ...
}
```

**What:** Defines a group of targets (ECS tasks) that can receive traffic.

**Why:**
- `port = 8002`: The port the service listens on inside the container
- `protocol = "HTTP"`: ALB communicates with targets via HTTP
- `target_type = "ip"`:
  - Required for Fargate - targets are registered by IP address
  - Alternative is "instance" for EC2-based ECS
- **Health check**:
  - `path = "/health"`: ALB calls this endpoint to check if the service is alive
  - `interval = 30`: Check every 30 seconds
  - `healthy_threshold = 2`: Mark healthy after 2 consecutive successes
  - `unhealthy_threshold = 3`: Mark unhealthy after 3 consecutive failures
  - `matcher = "200"`: Expect HTTP 200 response
  - `timeout = 5`: Fail if no response within 5 seconds

**Why health checks matter:**
- ALB only sends traffic to healthy targets
- If a container crashes, ALB stops sending it traffic within ~90 seconds
- ECS sees the unhealthy status and replaces the container

---

### Listener

```hcl
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.orchestrator.arn
  }
}
```

**What:** Tells the ALB to listen on port 80 and where to send traffic by default.

**Why:**
- `port = 80`: Listen for HTTP traffic
- `default_action`: What to do if no listener rules match
  - Sends to orchestrator service by default
  - This means `/sync/leagues` goes to orchestrator
- **Why no HTTPS?**
  - HTTPS requires an SSL certificate
  - You'd add a certificate from ACM (AWS Certificate Manager) and add a port 443 listener
  - For dev, HTTP is fine; for prod, you'd add HTTPS

---

### Listener Rules

```hcl
resource "aws_lb_listener_rule" "sportmonks" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.sportmonks.arn
  }

  condition {
    path_pattern {
      values = ["/leagues*", "/teams*", "/fixtures*"]
    }
  }
}
```

**What:** Routes specific URL paths to specific services.

**Why:**
- `priority = 100`: Rules are evaluated in order (lower number = higher priority)
- `path_pattern`: Match URLs that start with `/leagues`, `/teams`, or `/fixtures`
- `forward`: Send matching requests to the sportmonks target group

**Current routing:**
| Path | Service | Priority |
|------|---------|----------|
| `/leagues*`, `/teams*`, `/fixtures*` | SportMonks | 100 |
| `/db/*` | Database | 200 |
| Everything else | Orchestrator | Default |

**Note:** The path routing might need adjustment based on your actual API design. Currently:
- External clients hit the orchestrator
- Orchestrator internally calls sportmonks-service and database-service
- The ALB rules for sportmonks/database are there if you want to expose them directly

## HTTPS Configuration (for production)

To add HTTPS, you would:

1. Create/import a certificate in ACM
2. Add an HTTPS listener:

```hcl
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.orchestrator.arn
  }
}
```

3. Optionally redirect HTTP to HTTPS:

```hcl
default_action {
  type = "redirect"
  redirect {
    port        = "443"
    protocol    = "HTTPS"
    status_code = "HTTP_301"
  }
}
```
