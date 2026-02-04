.PHONY: install install-sportmonks install-database install-orchestrator up down

install: install-sportmonks install-database install-orchestrator

install-sportmonks:
	cd services/sportmonks-service && uv sync

install-database:
	cd services/database-service && uv sync

install-orchestrator:
	cd services/orchestrator-service && uv sync

up:
	podman-compose up --build -d

down:
	podman-compose down

inspect-db:
	podman exec -it insightxi-mysql mysql -u root -p insightxi_db
