<h1 align="center">pyCubes</h1>

---

<p align="center">
<a href="https://pypi.org/project/pycubes"><img alt="PyPI" src="https://img.shields.io/pypi/v/pycubes"></a>
<a href="https://pypi.org/project/pycubes"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pycubes"></a>
<a href="https://pypi.org/project/pycubes"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/pyCubes"></a>
<a href="https://pepy.tech/project/pycubes"><img alt="Downloads" src="https://pepy.tech/badge/pycubes/month"></a>
</p>
<p align="center">
<a href="https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml"><img alt="Test" src="https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml/badge.svg?branch=master"></a>
<a href="https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml"><img alt="Lint" src="https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml/badge.svg?branch=master"></a>
<a href="https://codecov.io/gh/DavisDmitry/pyCubes"><img alt="codecov" src="https://codecov.io/gh/DavisDmitry/pyCubes/branch/master/graph/badge.svg?token=Y18ZNYT4YS"></a>
</p>
<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
</p>

---
<p align="center"><a href="https://wiki.vg/Protocol">Спецификация протокола</a></p>

---

pyCubes — это библиотека для создания серверов и клиентов Minecraft Java Edition (1.14+).

**❗ 0.x версии не стабильны, API библиотеки может изменяться.**

## Установка

```bash
pip install pyCubes
```

## Особенности

* Сериализаторы для [типов данных](https://wiki.vg/Data_types) (кроме Chat, используйте String вместо него)
* Класс подключения
* Низкоуровневый сервер
* NBT модуль (обёртка над [nbtlib](https://github.com/vberlier/nbtlib))
* `generate_uuid` утилита (генерирует UUID по нику игрока для использования в offline режиме)
* Поддержка [AnyIO](https://github.com/agronholm/anyio) (библиотека для асинхронной работы с сетью и конкурентости)

## TODO

* [x] Сериализаторы для всех типов данных
* [ ] Дескриптор пакетов
* [ ] Реализовать сжатие пакетов
* [ ] Высокоуровневый класс-приложение для сервера с event driven API
* [ ] Высокоуровневый класс-приложение для клиента с event driven API
* [ ] Высокоуровневый класс-приложение для прокси с event driven API
* [ ] Chat API (конструктор сообщений чата)
* [ ] Commands API
* [ ] Добавить описание API в документацию
