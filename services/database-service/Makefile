.PHONY: run build run-container stop-container test lint lint-fix get-leagues get-league

SERVER_URL := http://127.0.0.1:8001
IMAGE_NAME := database-service
CONTAINER_NAME := database-service
ENV_FILE := ../../.env

run:
	uv run uvicorn app.main:app --reload --port 8001

build:
	podman build -t $(IMAGE_NAME) .

run-container:
	podman run -d --name $(CONTAINER_NAME) -p 8001:8001 --env-file $(ENV_FILE) $(IMAGE_NAME)

stop-container:
	podman stop $(CONTAINER_NAME) && podman rm $(CONTAINER_NAME)

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

get-leagues:
	curl -s $(SERVER_URL)/leagues | python -m json.tool

get-league:
	@if [ -z "$(id)" ]; then echo "Usage: make get-league id=<league_id>"; exit 1; fi
	curl -s $(SERVER_URL)/leagues/$(id) | python -m json.tool
