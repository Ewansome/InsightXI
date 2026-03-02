.PHONY: help install install-sportmonks install-database install-orchestrator lint lint-fix test up down inspect-db terraform-plan terraform-apply terraform-destroy terraform-destroy-db terraform-destroy-plan sync-leagues

SERVER_URL := http://127.0.0.1:8002
ROOT := $(shell pwd)


help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help             Show this help message"
	@echo "  install          Install dependencies for all services"
	@echo "  lint             Run Ruff linter on all services"
	@echo "  lint-fix         Run Ruff linter and auto-fix issues"
	@echo "  test             Run tests for all services"
	@echo "  up               Build and start all services with docker-compose"
	@echo "  down             Stop and remove all containers"
	@echo "  inspect-db       Connect to MySQL CLI in the container"
	@echo ""
	@echo "Terraform:"
	@echo "  terraform-plan         Preview infrastructure changes"
	@echo "  terraform-apply        Apply infrastructure changes"
	@echo "  terraform-destroy      Destroy all infrastructure"
	@echo "  terraform-destroy-db   Destroy only the RDS instance"
	@echo "  terraform-destroy-plan Preview what would be destroyed"
	@echo ""
	@echo "Individual service installs:"
	@echo "  install-sportmonks    Install sportmonks-service dependencies"
	@echo "  install-database      Install database-service dependencies"
	@echo "  install-orchestrator  Install orchestrator-service dependencies"

install: install-sportmonks install-database install-orchestrator

install-sportmonks:
	cd services/sportmonks-service && uv sync

install-database:
	cd services/database-service && uv sync

install-orchestrator:
	cd services/orchestrator-service && uv sync

lint:
	cd services/sportmonks-service && make lint
	cd services/database-service && make lint
	cd services/orchestrator-service && make lint

lint-fix:
	cd services/sportmonks-service && make lint-fix
	cd services/database-service && make lint-fix
	cd services/orchestrator-service && make lint-fix

test:
	cd services/sportmonks-service && make test
	cd services/database-service && make test
	cd services/orchestrator-service && make test

up:
	podman-compose up --build -d && sleep 10 && make health

down:
	podman-compose down

restart:
	make down
	make up

inspect-db:
	podman exec -it insightxi-mysql mysql -u root -p insightxi_db

sync-leagues:
	curl -s -X POST $(SERVER_URL)/sync/leagues | python3 -m json.tool

sync-teams:
	curl -s -X POST $(SERVER_URL)/sync/teams | python3 -m json.tool

sync-fixtures:
	curl -s -X POST $(SERVER_URL)/sync/fixtures | python3 -m json.tool

sync:
	make sync-leagues && make sync-teams && make sync-fixtures

health:                                                                                                                                                                                                                                  
	@echo "sportmonks-service: $$(curl -s http://localhost:8000/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unreachable")"                                                      
	@echo "database-service:   $$(curl -s http://localhost:8001/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unreachable")"                                                      
	@echo "orchestrator:       $$(curl -s http://localhost:8002/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unreachable")"                                                      
	@echo "mysql:              $$(podman exec insightxi-mysql mysqladmin ping -h localhost --silent 2>/dev/null && echo "healthy" || echo "unreachable")"                                                                             

terraform-plan:
	cd infrastructure/terraform && terraform plan

terraform-apply:
	cd infrastructure/terraform && terraform apply

terraform-destroy:
	cd infrastructure/terraform && terraform destroy

terraform-destroy-db:
	cd infrastructure/terraform && terraform destroy -target=aws_db_instance.main

terraform-destroy-plan:
	cd infrastructure/terraform && terraform plan -destroy
