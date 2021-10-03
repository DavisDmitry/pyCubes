format:
	poetry run isort .
	poetry run black .
lint:
	poetry run pylint cubes
	poetry run flake8 cubes
	poetry run isort --check --diff .
	poetry run black --check --diff .
