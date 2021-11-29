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

### Working with documentation

First you need to install requirments:

```bash
poetry install -E docs
```

Run the development server:

```bash
make docs-serve
```

Build (render) the docs:

```bash
make docs-build
```

Build and deploy the documentation to github pages:

```bash
make docs-deploy
```
