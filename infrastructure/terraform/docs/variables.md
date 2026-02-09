# variables.tf

This file defines all input variables for the Terraform configuration. Variables make the infrastructure configurable and reusable.

## Code Breakdown

```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}
```

**What:** Defines which AWS region to deploy to.

**Why:**
- Having a default means you don't need to specify it every time
- `eu-west-2` (London) is chosen for low latency if you're UK-based
- `type = string` enforces that this must be text, not a number or list

---

```hcl
variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "insightxi"
}
```

**What:** A prefix used for naming all AWS resources.

**Why:**
- Consistent naming makes resources easy to identify in the AWS console
- Helps avoid name collisions if you have multiple projects in the same account
- Used in tags and resource names like `insightxi-dev-vpc`

---

```hcl
variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}
```

**What:** Identifies which environment this deployment is for.

**Why:**
- Allows running multiple environments (dev, staging, prod) in the same AWS account
- Used in resource names to distinguish between environments
- Some resources behave differently based on environment (e.g., `deletion_protection` in RDS)

---

```hcl
variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}
```

**What:** Database credentials for RDS.

**Why:**
- `sensitive = true` prevents the password from being shown in Terraform output or logs
- Username has a default, but password intentionally doesn't - forcing you to set it explicitly
- These are passed to RDS when creating the database and to ECS tasks for connecting

---

```hcl
variable "sportmonks_api_key" {
  description = "SportMonks API key"
  type        = string
  sensitive   = true
}
```

**What:** The API key for authenticating with SportMonks.

**Why:**
- Marked `sensitive` to keep it out of logs
- No default value - must be provided
- Passed to the sportmonks-service container as an environment variable
