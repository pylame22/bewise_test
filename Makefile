run:
	uv run python -m src

format:
	uv run ruff format src migrations

lint:
	uv run ruff check src --fix
	uv run mypy src