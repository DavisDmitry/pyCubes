<h1 align="center">pyCubes</h1>

<p align="center">
<a href="https://pypi.org/project/pycubes"><img alt="PyPI" src="https://img.shields.io/pypi/v/pycubes"></a>
<a href="https://pypi.org/project/pycubes"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pycubes"></a>
<a href="https://pypi.org/project/pycubes"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/pyCubes"></a>
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
<p align="center">
<a href="https://pycubes.dmitrydavis.xyz">Documentation</a> | 
<a href="https://github.com/DavisDmitry/pyCubes/tree/master/examples">Examples</a> | 
<a href="https://wiki.vg/Protocol">Protocol Specification</a>
</p>

---
pyCubes is a library for creating servers and clients for Minecraft Java Edition (1.14+).

**❗ 0.x versions are not stable. The library API is subject to change.**

## Installation

```bash
pip install pyCubes
```

With `fast` extra (includes ujson and uvloop):

```bash
pip install pyCubes[fast]
```

## Features

* [Data types](https://wiki.vg/Data_types) (missing Chat, Entity Metadata, Particle, BitSet, Shunk Section (1.18) and Palleted container (1.18))
* Connection
* Low level server
* NBT module (wrapper over the [nbtlib](https://github.com/vberlier/nbtlib))
* `generate_uuid` utility (generates UUID by player_name for using in offline mode)
* [AnyIO](https://github.com/agronholm/anyio) support (an asynchronous networking and concurrency library)

## TODO

* [ ] All packets Data types
* [ ] Packets descriptor
* [ ] Implement compression
* [ ] High level server application with event driven API
* [ ] High level client application with event driven API
* [ ] High level proxy application with event driven API
* [ ] Chat API (chat messages constructor)
* [ ] Commands API
* [ ] Add API Reference to docs
