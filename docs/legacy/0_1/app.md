<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/app.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `app`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/app.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GracefulExit`
Exception raising when server should stop. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/app.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Application`
Class for creating Minecraft Java Edition server implemetation. 



**Examples:**
 ``` app = Application('0.0.0.0', 25565)```


<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/app.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(host: str, port: int)
```






---

#### <kbd>property</kbd> unhandled_packet_handler







---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/app.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_low_level_handler`

```python
add_low_level_handler(
    conn_status: ConnectionStatus,
    packet_id: int,
    func: Callable
) → None
```

Adds packet handler. 



**Raises:**
 
 - <b>`ValueError`</b>:  when handler with the same filter (conn_status and packet_id)  already added 



**Examples:**
 ``` server.add_low_level_handler(ConnectionStatus.HANDSHAKE,```
             0x00, process_handshake)


---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/app.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run() → None
```

Starts application. 


