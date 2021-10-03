# pyCubes

pyCubes is a library for serializing and deserializing Minecraft Java Edition packets.

**❗ 0.x versions are not stable. The library API is subject to change.**

[Русская версия](https://github.com/DavisDmitry/pyCubes/blob/master/README.ru.md)

Installation:

```bash
pip install pyCubes
```

## Usage:

First you need to create application instance:

```python3
import cubes

app = cubes.Application('127.0.0.1', 25565)
```

After that add a low-level handler:

```python3
async def process_handshake(packet: cubes.ReadBuffer) -> None:
    print('Protocol version:', packet.varint)
    print('Server host:', packet.string)
    print('Server port:', packet.unsigned_short)
    print('Next state:', cubes.ConnectionStatus(packet.varint))

app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
```

All that remains is to launch the application:

```python3
app.run()
```

A more detailed example can be found [here](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).

All packages are described [here](https://wiki.vg/Protocol).

## Development

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
