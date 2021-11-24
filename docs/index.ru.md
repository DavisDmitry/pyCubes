# pyCubes

---

[![PyPI](https://img.shields.io/pypi/v/pyCubes?style=flat)](https://pypi.org/project/pycubes) [![Test](https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml/badge.svg)](https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml) [![Lint](https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml/badge.svg)](https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml) [![codecov](https://codecov.io/gh/DavisDmitry/pyCubes/branch/master/graph/badge.svg?token=Y18ZNYT4YS)](https://codecov.io/gh/DavisDmitry/pyCubes) [![PyPI - License](https://img.shields.io/pypi/l/pyCubes)](https://pypi.org/project/pycubes) [![Downloads](https://pepy.tech/badge/pycubes/month)](https://pepy.tech/project/pycubes) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

---

pyCubes — это библиотека для создания серверов и клиентов Minecraft Java Edition.

**❗ 0.x версии не стабильны, API библиотеки может изменяться.**

Установка:

```bash
pip install pyCubes
```

## Использование

Сначала вам нужно создать экземпляр приложения:

```python3
import cubes

app = cubes.Application()
```

После этого добавьте низкоуровневый хендлер:

```python3
async def process_handshake(packet_id: int, packet: cubes.ReadBuffer) -> None:
    print('Protocol version:', packet.varint)
    print('Server host:', packet.string)
    print('Server port:', packet.unsigned_short)
    print('Next state:', cubes.ConnectionStatus(packet.varint))

app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
```

Остаётся только запустить приложение:

```python3
app.run('127.0.0.1', 25565)
```

Более подробный пример можно найти [здесь](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).

Все пакеты описаны [здесь](https://wiki.vg/Protocol).
