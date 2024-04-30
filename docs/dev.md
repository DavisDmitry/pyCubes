# Development

## Scripts

Run formatting:

```bash
pdm format
```

Run linters:

```bash
pdm lint
```

Run tests:

```bash
pdm test
```

### Working with documentation

First you need to install requirments:

```bash
pdm install -d -G docs
```

Run the development server:

```bash
pdm docs-serve
```

Build (render) the docs:

```bash
pdm docs-build
```

Build and deploy the documentation to github pages:

```bash
pdm docs-deploy
```
