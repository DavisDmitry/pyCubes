# pyCubes

pyCubes — это библиотека для получения и обработки пакетов от клиента Minecraft Java Edition.

**❗ 0.x версии не стабильны, классы, их методы и аргументы могут изменяться.**

Для использования PyCubes склонируйте этот репозиторий и перейдите в директорию с ним:

```bash
git clone git@github.com:DavisDmitry/pyCubes.git
cd pyCubes
```

## Использование

Сначала вам нужно создать экземпляр сервера:

```python3
from cubes import Server

server = Server('127.0.0.1', 25565)
```

После этого добавьте низкоуровневый хендлер:

```python3
import struct
from cubes import Buffer, ConnectionStatus

async def process_handshake(packet: Buffer) -> None:
    print('Protocol version:', packet.unpack_varint())
    print('Server host:', packet.unpack_string())
    print('Server port:', struct.unpack('>B', packet.read(2)))
    print('Next state:', ConnectionStatus(packet.unpack_varint()))

server.add_low_level_handler(ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
```

Остаётся только запустить сервер:

```python3
server.run()
```

Более подробный пример можно найти [здесь](https://github.com/DavisDmitry/pyCubes/blob/main/example.py).

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
