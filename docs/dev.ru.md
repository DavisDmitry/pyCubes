# Разработка

## Cкрипты

Запуск форматирования:

```bash
pdm format
```

Запуск линтеров:

```bash
pdm lint
```

Запуск тестов:

```bash
pdm test
```

### Работа с документацией

Cначала нужно установить необходимые утилиты:

```bash
pdm install -d -G docs
```

Запуск dev-сервера:

```bash
pdm docs-serve
```

Сборка (рендер) документации:

```bash
pdm docs-build
```

Сборка и загрузка на github pages:

```bash
pdm docs-deploy
```
