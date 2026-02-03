.PHONY: install install-sportmonks install-database

install: install-sportmonks install-database

install-sportmonks:
	cd services/sportmonks-service && uv sync

install-database:
	cd services/database-service && uv sync
