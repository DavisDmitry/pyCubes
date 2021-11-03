# Development

## Scripts

Run formatting:

```bash
make format
```

Run linters:

```bash
make lint
```

Run tests:

```bash
make test
```

## Working with documentation

First you need to install requirments:

```bash
poetry install --no-root -E docs
```

Generate API Reference:

```bash
poetry run scripts/generate_reference.py
```

Move current API Reference to Legacy:

```bash
python scripts/move_reference_to_legacy.py
```

Run the development server:

```bash
poetry run mkdocs serve
```

Build (render) the docs:

```bash
poetry run mkdocs build
```

Build and deploy the documentation to github pages:

```bash
poetry run mkdocs gh-build
```
