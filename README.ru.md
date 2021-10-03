# pyCubes

pyCubes — это библиотека для получения и обработки пакетов от клиента Minecraft Java Edition.

**❗ 0.x версии не стабильны, API библиотеки может изменяться.**

Установка:

```bash
pip install pyCubes
```

## Использование

Сначала вам нужно создать экземпляр приложения:

```python3
import cubes

app = cubes.Application('127.0.0.1', 25565)
```

После этого добавьте низкоуровневый хендлер:

```python3
async def process_handshake(packet: cubes.ReadBuffer) -> None:
    print('Protocol version:', packet.varint)
    print('Server host:', packet.string)
    print('Server port:', packet.unsigned_short)
    print('Next state:', cubes.ConnectionStatus(packet.varint))

app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
```

Остаётся только запустить приложение:

```python3
app.run()
```

Более подробный пример можно найти [здесь](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).

Все пакеты описаны [здесь](https://wiki.vg/Protocol).

## Разработка

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
