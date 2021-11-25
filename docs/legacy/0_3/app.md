<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/app.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `app`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/app.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GracefulExit`
Rises when the server should stop. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/app.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Application`
Class for creating Minecraft Java Edition server implemetation. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/app.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(packet_read_timeout: int = 20, process_packet_timeout: int = 20)
```






---

#### <kbd>property</kbd> unhandled_packet_handler

Setter for unhandled packets handler. 



---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/app.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_low_level_handler`

```python
add_low_level_handler(
    conn_status: ConnectionStatus,
    packet_id: int,
    func: Callable[[int, AbstractReadBuffer], Coroutine]
) → None
```

Adds packet handler. 



**Raises:**
 
 - <b>`ValueError`</b>:  when handler with the same filter (conn_status and packet_id)  already added 



**Examples:**
 ``` app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE,```
             0x00, process_handshake)


---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/app.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(host: str, port: int = 25565) → None
```

Starts application. 


