# InsightXI
### Overview
Application for collating sports data for visualisation. Data sourced from [SportMonks API](https://docs.sportmonks.com/football).

-----
### Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python, FastAPI, Pydantic |
| **Database** | MySQL, SQLAlchemy |
| **Infrastructure** | Docker, Terraform, GitHub Actions |
| **AWS** | ECS Fargate, RDS, API Gateway, ALB, ECR |
| **Development** | uv, Ruff, pytest |

-----
### Architecture

```mermaid
flowchart TB
    trigger[Manual Trigger] --> orchestrator

    subgraph orchestrator[Orchestrator Service]
        orch_endpoints["POST /sync/leagues<br>POST /sync/teams<br>POST /sync/fixtures"]
    end

    orchestrator --> sportmonks
    orchestrator --> database

    subgraph sportmonks[SportMonks Service]
        sm_endpoints["GET /leagues<br>GET /teams<br>GET /fixtures"]
    end

    subgraph database[Database Service]
        db_endpoints["POST /leagues<br>POST /leagues/bulk<br>GET /leagues/{id}"]
    end

    sportmonks --> api[(SportMonks API)]
    database --> mysql[(MySQL)]
```
-----
### Services

**Orchestrator Service** - Coordinates data sync workflows between services
- Exposes sync endpoints for manual triggers
- Fetches data from SportMonks Service, stores via Database Service
- Handles errors and returns sync status

**SportMonks Service** - Handles all SportMonks API interactions
- Fetches and validates data from SportMonks
- Manages authentication, rate limiting, retries

**Database Service** - Handles all database operations
- CRUD endpoints per entity
- Bulk operations for data ingestion

-----
### Project Structure

```
services/
├── orchestrator-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── clients/
│   │   └── models/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── sportmonks-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── clients/
│   │   └── models/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
└── database-service/
    ├── app/
    │   ├── main.py
    │   ├── controllers/
    │   ├── services/
    │   ├── repositories/
    │   └── models/
    ├── tests/
    ├── Dockerfile
    └── pyproject.toml
```

-----
### Getting Started

**Run with Docker/Podman (recommended):**
```bash
make up           # Build and start all services + MySQL
make down         # Stop and remove all containers
make inspect-db   # Connect to MySQL CLI
```

**Local development:**
```bash
make install      # Install dependencies for all services
```

**Trigger a sync:**
```bash
curl -X POST http://localhost:8002/sync/leagues
```

-----
### CI/CD Pipeline

```mermaid
flowchart LR
    subgraph CI[CI - Pull Requests]
        pr[Pull Request] --> lint[Lint]
        lint --> test[Test]
    end

    subgraph CD[CD - Main Branch]
        push[Push to Main] --> build[Build Images]
        build --> ecr[Push to ECR]
    end

    pr -.->|merge| push
```

**CI (on every PR):**
- Runs Ruff linter on all services
- Runs pytest for all services

**CD (on merge to main):**
- Builds Docker images for all services
- Pushes to Amazon ECR with commit SHA and `latest` tags

-----
### AWS Architecture

```mermaid
flowchart TB
    subgraph internet[Internet]
        client[Client]
    end

    subgraph aws[AWS]
        subgraph vpc[VPC]
            subgraph public[Public Subnets]
                nat[NAT Gateway]
            end

            subgraph private[Private Subnets]
                subgraph ecs[ECS Fargate]
                    orch[Orchestrator<br>Service]
                    sm[SportMonks<br>Service]
                    db_svc[Database<br>Service]
                end
                alb[Internal ALB]
                rds[(RDS MySQL)]
            end
        end

        apigw[API Gateway]
        ecr[ECR]
    end

    client --> apigw
    apigw -->|VPC Link| alb
    alb --> orch
    alb --> sm
    alb --> db_svc
    orch --> sm
    orch --> db_svc
    db_svc --> rds
    sm -->|NAT| nat
    nat --> sportmonks_api[(SportMonks API)]
    ecr -.->|Pull Images| ecs
```

**Traffic Flow:**
1. Client requests hit API Gateway (public endpoint)
2. API Gateway routes through VPC Link to internal ALB
3. ALB routes to ECS services based on path
4. Services communicate internally via ALB
5. Outbound API calls go through NAT Gateway
