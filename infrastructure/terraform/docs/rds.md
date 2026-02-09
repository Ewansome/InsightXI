# rds.tf

This file creates the RDS (Relational Database Service) MySQL instance - a managed database that AWS handles backups, patching, and maintenance for.

## Code Breakdown

### Subnet Group

```hcl
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-${var.environment}-db-subnet"
  }
}
```

**What:** Defines which subnets RDS can use.

**Why:**
- RDS needs to know where it can place database instances
- `aws_subnet.private[*].id` uses the splat operator (`[*]`) to get all private subnet IDs as a list
- We use private subnets because the database should never be publicly accessible
- Having 2 subnets in different AZs allows for Multi-AZ failover (if enabled)

---

### RDS Instance

```hcl
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-${var.environment}-db"
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = "db.t3.micro"
  ...
}
```

**What:** The basic identity and size of the database.

**Why:**
- `identifier`: Unique name for the RDS instance in AWS
- `engine = "mysql"`: We're using MySQL to match local development
- `engine_version = "8.0"`: MySQL 8.0 matches what we use in Docker
- `instance_class = "db.t3.micro"`:
  - Smallest instance type, ~$15/month
  - 2 vCPUs, 1GB RAM
  - Fine for dev/testing, upgrade for production

---

```hcl
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp3"
  storage_encrypted     = true
```

**What:** Storage configuration.

**Why:**
- `allocated_storage = 20`: Start with 20GB - minimum for gp3
- `max_allocated_storage = 100`: Enables storage autoscaling up to 100GB
  - If you hit 20GB, AWS automatically expands (no downtime)
  - You only pay for what you use
- `storage_type = "gp3"`:
  - General Purpose SSD, good balance of cost/performance
  - gp3 is newer and cheaper than gp2 with better baseline performance
- `storage_encrypted = true`: Data at rest is encrypted
  - Uses AWS-managed keys by default
  - Required for any production workload, good practice for dev too

---

```hcl
  db_name  = "insightxi_db"
  username = var.db_username
  password = var.db_password
```

**What:** Database credentials.

**Why:**
- `db_name`: Creates this database automatically on launch (matches our .env)
- `username/password`: From variables, so they're not hardcoded
- Password is marked `sensitive` in variables.tf so it won't appear in logs

---

```hcl
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
```

**What:** Network configuration.

**Why:**
- `vpc_security_group_ids`: Attaches the RDS security group we created
  - Only allows connections from ECS tasks
- `db_subnet_group_name`: Places the database in our private subnets

---

```hcl
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"
```

**What:** Backup and maintenance schedules.

**Why:**
- `backup_retention_period = 7`: Keep 7 days of automated backups
  - Allows point-in-time recovery if something goes wrong
  - AWS takes daily snapshots automatically
- `backup_window = "03:00-04:00"`: When to take backups (UTC)
  - Chosen for low-traffic hours (3-4am UK time)
- `maintenance_window`: When AWS can apply patches
  - Slightly after backup window
  - Monday early morning is typically lowest traffic

---

```hcl
  skip_final_snapshot = var.environment != "prod"
  deletion_protection = var.environment == "prod"
```

**What:** Safety settings that vary by environment.

**Why:**
- `skip_final_snapshot`:
  - In dev: `true` - just delete, don't bother with a final backup
  - In prod: `false` - forces a final snapshot before deletion
- `deletion_protection`:
  - In dev: `false` - easy to tear down and recreate
  - In prod: `true` - prevents accidental deletion
  - You'd have to explicitly disable this before deleting

## Cost Considerations

For dev environment:
- `db.t3.micro`: ~$15/month
- 20GB gp3 storage: ~$2/month
- Backups (within retention): Free up to DB size
- **Total: ~$17/month**

For production, you'd want:
- `db.t3.small` or larger
- Multi-AZ deployment (`multi_az = true`) for failover
- Longer backup retention
