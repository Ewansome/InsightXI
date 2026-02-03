.PHONY: install install-sportmonks

install: install-sportmonks

install-sportmonks:
	cd services/sportmonks-service && uv sync
