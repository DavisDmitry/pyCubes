# Разработка

## Cкрипты

### Запуск форматирования

```bash
make format
```

### Запуск линтеров

```bash
make lint
```

### Запуск тестов

```bash
make test
```

### Изменение версии

Необходимо создать переменную окружения `VERSION` . Например:

```bash
export VERSION=0.2.0
```

Затем просто запустить скрипт:

```bash
python scripts/edit_version.py
```

## Работа с документацией

Cначала нужно установить необходимые утилиты:

```bash
poetry install --no-root -E docs
```

### Генерация API Reference

Для генерации используется переменная окружения `VERSION` . Её нужно экспортировать, например:

```bash
export VERSION=0.2.0
```

Генерация:

```bash
poetry run scripts/generate_reference.py
```

### Перенос API Reference в раздел Legacy

```bash
python scripts/move_reference_to_legacy.py
```

### Запуск dev-сервера

```bash
poetry run mkdocs serve
```

### Сборка (рендер) документации

```bash
poetry run mkdocs build
```

### Сборка и загрузка на github pages

```bash
poetry run mkdocs gh-build
```
