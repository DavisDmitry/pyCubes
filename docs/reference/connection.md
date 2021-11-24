<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `connection`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CloseConnection`
Raised when a connection should be closed. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(reason: Optional[str] = None)
```









---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DisconnectedByServerError`
Raised when a disconnect packet is received from a server. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(state: ConnectionStatus, reason: str) → None
```









---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnexpectedPacketError`
Raised when an unexpected packet is received from a server. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(packet_id: int) → None
```









---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `InvalidPlayerNameError`
Raised when a Successful Login packet with an invalid name is received        from a server. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(valid_name: str, invalid_name: str) → None
```









---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PlayerConnection`
Player-to-server connection. 



**Attributes:**
 
 - <b>`status`</b> (cubes.ConnectionStatus):  Connection status. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(reader: StreamReader, writer: StreamWriter, app: Application)
```






---

#### <kbd>property</kbd> app

cubes.abc.AbstractApplication: Current application. 

---

#### <kbd>property</kbd> is_closing

bool: Is connection closing. 

---

#### <kbd>property</kbd> peername

tuple[str, int]: Client host and port. 

---

#### <kbd>property</kbd> sockname

tuple[str, int]: Server host and port. 



---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `close`

```python
close(reason: Optional[str] = None) → None
```

Closes the connection. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_packet`

```python
read_packet() → Optional[AbstractReadBuffer]
```

Reads a packet. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `send_packet`

```python
send_packet(buffer: AbstractWriteBuffer) → None
```

Sends the packet. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wait_packet`

```python
wait_packet() → AbstractReadBuffer
```

Waits and reads a packet. 


---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ClientConnection`
Client connection. 



**Attributes:**
 
 - <b>`status`</b> (cubes.ConnectionStatus):  Connection status 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(reader: StreamReader, writer: StreamWriter, player: PlayerData)
```






---

#### <kbd>property</kbd> is_closing

bool: Is connection closing. 

---

#### <kbd>property</kbd> peername

tuple[str, int]: Client host and port. 

---

#### <kbd>property</kbd> player

cubes.PlayerData: Player data (UUID and name). 

---

#### <kbd>property</kbd> sockname

tuple[str, int]: Server host and port. 



---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `close`

```python
close() → None
```

Closes the connection. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `connect`

```python
connect(
    host: str,
    port: int,
    protocol: int,
    player_name: str
) → AbstractClientConnection
```





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_packet`

```python
read_packet() → Optional[AbstractReadBuffer]
```

Reads a packet. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `send_packet`

```python
send_packet(buffer: AbstractWriteBuffer) → None
```

Sends the packet. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.2.0/cubes/connection.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wait_packet`

```python
wait_packet() → AbstractReadBuffer
```

Waits and reads a packet. 


