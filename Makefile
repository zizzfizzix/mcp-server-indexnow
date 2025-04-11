.PHONY: install lint format test build deploy ship_it start mcp_inspector clean

install:
	uv sync

lint:
	uv run mypy --strict mcp_server_indexnow/
	uv run ruff check --fix mcp_server_indexnow/

format:
	uv run ruff format mcp_server_indexnow/

test:
	uv run pytest mcp_server_indexnow \
		--doctest-modules \
		--junitxml=reports/test-results-$(shell cat .python-version).xml

build: clean
	uv run build

deploy: install build

ship_it: build
	git push

start:
	uv run mcp_server_indexnow/main.py

mcp_inspector:
	npx @modelcontextprotocol/inspector uv --directory ${PWD} run mcp_server_indexnow/main.py

clean:
	rm -rf dist/ build/ reports/ *.egg-info/ *cache