# pyCubes

---

![PyPI](https://img.shields.io/pypi/v/pyCubes?style=flat) ![example workflow](https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml/badge.svg) ![example workflow](https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml/badge.svg) [![codecov](https://codecov.io/gh/DavisDmitry/pyCubes/branch/master/graph/badge.svg?token=Y18ZNYT4YS)](https://codecov.io/gh/DavisDmitry/pyCubes) ![PyPI - License](https://img.shields.io/pypi/l/pyCubes) [![Downloads](https://pepy.tech/badge/pycubes/month)](https://pepy.tech/project/pycubes) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

---
pyCubes is a library for creating servers and clients Minecraft Java Edition.

**❗ 0.x versions are not stable. The library API is subject to change.**

Installation:

```bash
pip install pyCubes
```

## Usage

First you need to create application instance:

```python3
import cubes

app = cubes.Application()
```

After that add a low-level handler:

```python3
async def process_handshake(packet_id: int, packet: cubes.ReadBuffer):
    print('Protocol version:', packet.varint)
    print('Server host:', packet.string)
    print('Server port:', packet.unsigned_short)
    print('Next state:', cubes.ConnectionStatus(packet.varint))

app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
```

All that remains is to launch the application:

```python3
app.run('127.0.0.1', 25565)
```

A more detailed example can be found [here](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).

All packages are described [here](https://wiki.vg/Protocol).
