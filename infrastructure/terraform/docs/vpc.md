# vpc.tf

This file creates the Virtual Private Cloud (VPC) - an isolated network in AWS where all your resources live.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                          VPC (10.0.0.0/16)                  │
│                                                             │
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │   Public Subnet 1   │      │   Public Subnet 2   │      │
│  │    10.0.1.0/24      │      │    10.0.2.0/24      │      │
│  │        AZ-a         │      │        AZ-b         │      │
│  │    ┌─────────┐      │      │                     │      │
│  │    │   NAT   │      │      │                     │      │
│  │    └────┬────┘      │      │                     │      │
│  └─────────┼───────────┘      └─────────────────────┘      │
│            │                                                │
│            │ Internet Gateway                               │
│            │                                                │
│  ┌─────────▼───────────┐      ┌─────────────────────┐      │
│  │  Private Subnet 1   │      │  Private Subnet 2   │      │
│  │    10.0.10.0/24     │      │    10.0.11.0/24     │      │
│  │        AZ-a         │      │        AZ-b         │      │
│  │  ┌───┐ ┌───┐ ┌───┐  │      │                     │      │
│  │  │ECS│ │ECS│ │RDS│  │      │       ┌───┐         │      │
│  │  └───┘ └───┘ └───┘  │      │       │RDS│         │      │
│  └─────────────────────┘      └───────┴───┴─────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Code Breakdown

### VPC

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}
```

**What:** Creates the VPC with a large IP address range.

**Why:**
- `10.0.0.0/16` gives us 65,536 IP addresses - plenty of room to grow
- `enable_dns_hostnames` allows instances to get DNS names (e.g., `ec2-x-x-x-x.region.compute.amazonaws.com`)
- `enable_dns_support` enables DNS resolution within the VPC - required for services to find each other by name
- Tags with a consistent naming pattern make resources easy to find in the AWS console

---

### Internet Gateway

```hcl
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  ...
}
```

**What:** Creates an Internet Gateway and attaches it to the VPC.

**Why:**
- The Internet Gateway is the door between your VPC and the public internet
- Without it, nothing in your VPC can reach the internet (or be reached)
- Required for the ALB to receive traffic from users
- `aws_vpc.main.id` references the VPC we created above - this is how Terraform links resources together

---

### Subnets

```hcl
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  ...
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  ...
}
```

**What:** Creates 2 public and 2 private subnets across different Availability Zones.

**Why:**
- **count = 2**: Creates 2 subnets using a loop. `count.index` gives us 0, then 1
- **Public subnets** (`10.0.1.0/24`, `10.0.2.0/24`):
  - `map_public_ip_on_launch = true` means instances get public IPs automatically
  - Used for the ALB which needs to be publicly accessible
- **Private subnets** (`10.0.10.0/24`, `10.0.11.0/24`):
  - No public IPs - instances are hidden from the internet
  - Used for ECS tasks and RDS - they don't need direct internet access
- **2 Availability Zones**: If one data centre fails, your app keeps running in the other
  - AWS requires ALB to be in at least 2 AZs
  - RDS can failover to another AZ

---

### NAT Gateway

```hcl
resource "aws_eip" "nat" {
  domain = "vpc"
  ...
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
  ...
}
```

**What:** Creates a NAT Gateway with an Elastic IP.

**Why:**
- Resources in private subnets can't reach the internet directly (that's the point of private)
- But they still need internet access to pull Docker images, call external APIs, etc.
- NAT Gateway acts as a middleman: private resources → NAT Gateway → Internet
- **Elastic IP**: A static public IP that doesn't change if the NAT Gateway is recreated
- Placed in a public subnet so it can reach the Internet Gateway
- This is a common pattern: private resources stay hidden but can make outbound requests

**Cost note:** NAT Gateways cost ~$30/month + data transfer. For a cheaper dev setup, you could remove this and give ECS tasks public IPs, but that's less secure.

---

### Route Tables

```hcl
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  ...
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
  ...
}
```

**What:** Defines routing rules for public and private subnets.

**Why:**
- Route tables are like GPS for network traffic - they tell packets where to go
- `0.0.0.0/0` means "all destinations not in the VPC" (i.e., the internet)
- **Public route table**: "To reach the internet, go through the Internet Gateway"
- **Private route table**: "To reach the internet, go through the NAT Gateway"
- Traffic within the VPC (e.g., ECS → RDS) is automatically routed locally

---

### Route Table Associations

```hcl
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
```

**What:** Links each subnet to its appropriate route table.

**Why:**
- Subnets don't automatically know which route table to use
- Associations explicitly say "this subnet uses this route table"
- Using `count` to associate all public subnets with the public route table (and same for private)
