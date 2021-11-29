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

docs-serve:
	poetry run mkdocs serve

docs-build:
	poetry run mkdocs build

docs-deploy:
	poetry run mkdocs gh-deploy -m "📝 Update docs"
