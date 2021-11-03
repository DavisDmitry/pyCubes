<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `connection`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CloseConnection`
Raising when connection should be closed. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConnectionStatus`
An enumeration. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Connection`
Client or server connection. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(reader: StreamReader, writer: StreamWriter)
```








---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `close`

```python
close() → None
```

Closes connection. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `get_current`

```python
get_current() → Optional[ForwardRef('Connection')]
```

Returns current `Connection` instance. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_packet`

```python
read_packet() → Optional[ReadBuffer]
```

Reads packet. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `send_packet`

```python
send_packet(_buffer: WriteBuffer) → None
```

Sends packet. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/connection.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_current`

```python
set_current() → None
```

Sets instance as a current. 


