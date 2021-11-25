# Development

## Scripts

### Run formatting

```bash
make format
```

### Run linters

```bash
make lint
```

### Run tests

```bash
make test
```

### Change version

It is necessary to create the environment variable `VERSION` . For example:

```bash
export VERSION=0.4.0
```

Then just run the script:

```bash
make edit-version
```

## Working with documentation

First you need to install requirments:

```bash
poetry install -E docs
```

### Validate docstrings in code

```bash
make validate-docstrings
```

### Generate API Reference

The environment variable `VERSION` is used for generation. It needs to be exported, for example:

```bash
export VERSION=0.4.0
```

Generate:

```bash
make docs-generate-reference
```

### Move current API Reference to Legacy

```bash
make docs-move-to-legacy
```

### Run the development server

```bash
make docs-serve
```

### Build (render) the docs

```bash
make docs-build
```

### Build and deploy the documentation to github pages

```bash
make docs-deploy
```
