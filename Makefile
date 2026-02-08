.PHONY: help install install-sportmonks install-database install-orchestrator lint lint-fix test up down inspect-db

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
	podman-compose up --build -d

down:
	podman-compose down

inspect-db:
	podman exec -it insightxi-mysql mysql -u root -p insightxi_db
