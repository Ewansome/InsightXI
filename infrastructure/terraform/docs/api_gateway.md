# api_gateway.tf

This file creates the API Gateway - the public entry point that sits in front of the internal ALB. API Gateway handles authentication, rate limiting, and routes requests to the private services.

## Architecture

```
Internet
    │
    ▼
┌─────────────────┐
│  API Gateway    │  ◄── Public endpoint (https://xxx.execute-api.eu-west-2.amazonaws.com)
│  (HTTP API)     │
└────────┬────────┘
         │
         │ VPC Link (private connection)
         ▼
┌─────────────────┐
│  Internal ALB   │  ◄── Private (no public access)
│                 │
└────────┬────────┘
         │
         ▼
    ECS Services
```

## Why API Gateway + Internal ALB?

| Feature | Public ALB | API Gateway + Internal ALB |
|---------|-----------|---------------------------|
| Authentication | Application code | Built-in (Cognito, JWT, API keys) |
| Rate limiting | Need custom solution | Built-in |
| API keys | Manual | Built-in management |
| Usage plans | No | Yes (throttle by client) |
| Request validation | Application code | Can validate before reaching app |
| Cost | ~$20/month | ~$1/million requests |
| Latency | Lower | Slightly higher (~10-20ms) |

For most APIs, API Gateway's features outweigh the small latency cost.

## Code Breakdown

### HTTP API

```hcl
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project_name}-${var.environment}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }
  ...
}
```

**What:** Creates the API Gateway itself.

**Why:**
- `protocol_type = "HTTP"`: HTTP APIs are cheaper and faster than REST APIs
  - HTTP API: ~$1.00 per million requests
  - REST API: ~$3.50 per million requests
  - HTTP API lacks some REST API features (usage plans, API keys) but has JWT auth
- **CORS configuration:**
  - Required if the frontend (browser) is on a different domain
  - `allow_origins = ["*"]`: Allow any domain (tighten for production)
  - `allow_headers`: Must include `Authorization` for JWT tokens
  - `max_age = 300`: Browser caches CORS preflight for 5 minutes

---

### VPC Link

```hcl
resource "aws_apigatewayv2_vpc_link" "main" {
  name               = "${var.project_name}-${var.environment}-vpc-link"
  security_group_ids = [aws_security_group.api_gateway.id]
  subnet_ids         = aws_subnet.private[*].id
  ...
}
```

**What:** Creates a private connection from API Gateway into the VPC.

**Why:**
- API Gateway runs on AWS's public infrastructure, not in the VPC
- VPC Link creates an elastic network interface (ENI) in the private subnets
- This ENI allows API Gateway to reach the internal ALB
- Without VPC Link, API Gateway can only reach public endpoints
- `security_group_ids`: Controls what the VPC Link can access (just port 80 to ALB)

---

### Integration

```hcl
resource "aws_apigatewayv2_integration" "alb" {
  api_id             = aws_apigatewayv2_api.main.id
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  integration_uri    = aws_lb_listener.http.arn
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.main.id
}
```

**What:** Defines how API Gateway connects to the backend.

**Why:**
- `integration_type = "HTTP_PROXY"`: Pass requests through to the backend as-is
  - Alternative: `AWS_PROXY` for Lambda integration
- `integration_method = "ANY"`: Accept all HTTP methods
- `integration_uri`: Points to the ALB listener (the entry point)
- `connection_type = "VPC_LINK"`: Use the private VPC Link connection
  - Alternative: `INTERNET` for public endpoints

---

### Route

```hcl
resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.alb.id}"
}
```

**What:** Routes all requests to the ALB integration.

**Why:**
- `route_key = "$default"`: Catch-all route for any path/method
- The ALB's listener rules then route to specific services
- You could add specific routes here if needed:
  ```hcl
  route_key = "POST /sync/leagues"  # Only match this path
  ```

---

### Stage

```hcl
resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId        = "$context.requestId"
      ip               = "$context.identity.sourceIp"
      ...
    })
  }
  ...
}
```

**What:** Creates a deployment stage for the API.

**Why:**
- `name = "$default"`: The default stage (no path prefix)
  - Alternative: `name = "v1"` would make URLs like `/v1/sync/leagues`
- `auto_deploy = true`: Changes deploy automatically
  - For production, you might want manual deployments
- **access_log_settings**: Logs every request to CloudWatch
  - Useful for debugging, monitoring, and security auditing
  - Logs include: request ID, source IP, path, status code, etc.

## Adding Authentication (Future)

### JWT Authorizer (Cognito or any OIDC provider)

```hcl
resource "aws_apigatewayv2_authorizer" "jwt" {
  api_id           = aws_apigatewayv2_api.main.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name             = "jwt-authorizer"

  jwt_configuration {
    audience = ["the-client-id"]
    issuer   = "https://cognito-idp.eu-west-2.amazonaws.com/eu-west-2_xxxxx"
  }
}

resource "aws_apigatewayv2_route" "protected" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "POST /sync/leagues"
  target             = "integrations/${aws_apigatewayv2_integration.alb.id}"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
}
```

This would:
1. Require a valid JWT in the `Authorization` header
2. Validate it against Cognito (or another OIDC provider)
3. Reject requests with invalid/expired tokens before they reach the app

### API Keys (for machine-to-machine)

For REST APIs (not HTTP APIs), you can use API keys:

```hcl
resource "aws_api_gateway_api_key" "client" {
  name = "client-api-key"
}

resource "aws_api_gateway_usage_plan" "main" {
  name = "standard"

  throttle_settings {
    burst_limit = 100
    rate_limit  = 50
  }

  quota_settings {
    limit  = 10000
    period = "MONTH"
  }
}
```

## Cost Estimate

- HTTP API: $1.00 per million requests
- VPC Link: ~$0.01/hour (~$7/month)
- CloudWatch Logs: ~$0.50/GB ingested

For low traffic (< 1M requests/month), total cost is ~$10/month.
