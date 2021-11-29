# Разработка

## Cкрипты

Запуск форматирования:

```bash
make format
```

Запуск линтеров:

```bash
make lint
```

Запуск тестов:

```bash
make test
```

### Работа с документацией

Cначала нужно установить необходимые утилиты:

```bash
poetry install -E docs
```

Запуск dev-сервера:

```bash
make docs-serve
```

Сборка (рендер) документации:

```bash
make docs-build
```

Сборка и загрузка на github pages:

```bash
make docs-deploy
```
