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
export VERSION=0.4.0
```

Затем просто запустите скрипт:

```bash
make edit-version
```

## Работа с документацией

Cначала нужно установить необходимые утилиты:

```bash
poetry install -E docs
```

### Валидация строк документации в коде

```bash
make validate-docstrings
```

### Генерация API Reference

Для генерации используется переменная окружения `VERSION` . Её нужно экспортировать, например:

```bash
export VERSION=0.4.0
```

Генерация:

```bash
make docs-generate-reference
```

### Перенос API Reference в раздел Legacy

```bash
make docs-move-to-legacy
```

### Запуск dev-сервера

```bash
make docs-serve
```

### Сборка (рендер) документации

```bash
make docs-build
```

### Сборка и загрузка на github pages

```bash
make docs-deploy
```
