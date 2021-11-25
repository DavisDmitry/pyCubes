format:
	poetry run isort .
	poetry run black .

lint:
	poetry run pylint cubes
	poetry run flake8 cubes
	poetry run isort --check --diff .
	poetry run black --check --diff .

test:
	poetry run pytest --cov=cubes --cov-report=term-missing

edit-version:
	poetry run python scripts/edit_version.py

validate-docstrings:
	poetry run pydocstyle --convention=google --add-ignore=D100,D101,D102,D103,D104,D105,D107,D202 cubes

docs-generate-reference:
	poetry run python scripts/generate_reference.py

docs-move-to-legacy:
	poetry run python scripts/move_reference_to_legacy.py

docs-serve:
	poetry run mkdocs serve

docs-build:
	poetry run mkdocs build

docs-deploy:
	poetry run mkdocs gh-deploy -m "📝 Update docs"
