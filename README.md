<h1 align="center">pyCubes</h1>

<p align="center">
<a href="https://pypi.org/projects/pycubes"><img alt="PyPI" src="https://img.shields.io/pypi/v/pycubes"></a>
<a href="https://pypi.org/projects/pycubes"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pycubes"></a>
<a href="https://pypi.org/projects/pycubes"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/pyCubes"></a>
<a href="https://pepy.tech/project/pycubes"><img alt="Downloads" src="https://pepy.tech/badge/pycubes/month"></a>
</p>
<p align="center">
<a href="https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml"><img alt="Test" src="https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml/badge.svg"></a>
<a href="https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml"><img alt="Lint" src="https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml/badge.svg"></a>
<a href="https://codecov.io/gh/DavisDmitry/pyCubes"><img alt="codecov" src="https://codecov.io/gh/DavisDmitry/pyCubes/branch/master/graph/badge.svg?token=Y18ZNYT4YS"></a>
</p>
<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
</p>

---
<p align="center"><a href="https://pycubes.dmitrydavis.xyz/">Documentation</a></p>

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
