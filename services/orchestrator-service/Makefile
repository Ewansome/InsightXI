.PHONY: run build run-container stop-container test lint lint-fix sync-leagues

IMAGE_NAME := orchestrator-service
CONTAINER_NAME := orchestrator-service
ENV_FILE := ../../.env

run:
	uv run uvicorn app.main:app --reload --port 8002

build:
	podman build -t $(IMAGE_NAME) .

run-container:
	podman run -d --name $(CONTAINER_NAME) -p 8002:8002 --env-file $(ENV_FILE) $(IMAGE_NAME)

stop-container:
	podman stop $(CONTAINER_NAME) && podman rm $(CONTAINER_NAME)

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

sync-leagues:
	curl -s -X POST $(SERVER_URL)/sync/leagues | python -m json.tool
