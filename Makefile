install:
	uv sync

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src

clean:
	find src tests -type d -name __pycache__ -prune -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	uv run flake8 . --extend-exclude=.venv,llm_sdk
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 . --extend-exclude=.venv,llm_sdk
	uv run mypy . --strict

test:
	chmod a-r src/data/input/invalid_permission.json
	uv run python -m unittest discover -s tests -v

.PHONY: install run debug clean lint lint-strict test
