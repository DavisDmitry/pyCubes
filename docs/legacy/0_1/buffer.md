<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `buffer`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EmptyBufferError`
Exception raising when buffer is empty. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ReadBuffer`
Class for parsing data by types. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(data: bytes = b'')
```






---

#### <kbd>property</kbd> boolean

Either False or True. 

---

#### <kbd>property</kbd> byte

Signed 8-bit integer. 

---

#### <kbd>property</kbd> data

Buffer data. 

---

#### <kbd>property</kbd> double

Signed 64-bit float. 

---

#### <kbd>property</kbd> float

Signed 32-bit float. 

---

#### <kbd>property</kbd> integer

Signed 32-bit integer. 

---

#### <kbd>property</kbd> long

Signed 64-bit integer. 

---

#### <kbd>property</kbd> short

Signed 16-bit integer. 

---

#### <kbd>property</kbd> string

UTF-8 string. 



**Note:**

> Max string length is 32767 (b'\xff\xff\x01') bytes — 3 bytes VarInt prefix. 

---

#### <kbd>property</kbd> unsigned_byte

Unsigned 8-bit integer. 

---

#### <kbd>property</kbd> unsigned_short

Unsigned 16-bit integer. 

---

#### <kbd>property</kbd> varint

Variable-length integer. 

---

#### <kbd>property</kbd> varlong

Variable-length integer. 



---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_reader`

```python
from_reader(reader: StreamReader) → ReadBuffer
```

Creates a ReadBuffer instance from asyncio.StreamReader. 



**Note:**

> Packet length is 2097151 (b'\xff\xff\x7f') bytes — 3 bytes VarInt prefix. 
>

**Raises:**
 
 - <b>`EmptyBufferError`</b>:  when buffer is empty 



**Todo:**
 * implement compression 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read`

```python
read(length: Optional[int] = None) → bytes
```

Reads length bytes from buffer. 



**Note:**

> If length <= 0 or None returns all buffer data from current position. 
>

**Args:**
 
 - <b>`length`</b>:  number of bytes to read 


---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L174"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WriteBuffer`
Class for serializing data by types. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(data: bytes = b'')
```






---

#### <kbd>property</kbd> data

Buffer data. 

---

#### <kbd>property</kbd> packed

Packed buffer data. 



**Todo:**
  * implement compression 



---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L191"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_boolean`

```python
pack_boolean(value: bool) → WriteBuffer
```

Packs True or False. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L195"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_byte`

```python
pack_byte(value: int) → WriteBuffer
```

Packs signed 8-bit integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_double`

```python
pack_double(value: float) → WriteBuffer
```

Packs signed 64-bit double. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_float`

```python
pack_float(value: float) → WriteBuffer
```

Packs signed 32-bit float. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_integer`

```python
pack_integer(value: int) → WriteBuffer
```

Packs signed 32-bit integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_long`

```python
pack_long(value: int) → WriteBuffer
```

Packs signed 64-bit integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L203"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_short`

```python
pack_short(value: int) → WriteBuffer
```

Packs signed 16-bit integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_string`

```python
pack_string(value: str) → WriteBuffer
```

Packs UTF-8 string. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L199"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_unsigned_byte`

```python
pack_unsigned_byte(value: int) → WriteBuffer
```

Packs unsigned 8-bit integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_unsigned_short`

```python
pack_unsigned_short(value: int) → WriteBuffer
```

Packs unsigned 16-bit integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L258"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_varint`

```python
pack_varint(value: int) → WriteBuffer
```

Packs variable-length integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L262"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pack_varlong`

```python
pack_varlong(value: int) → WriteBuffer
```

Packs variable-length integer. 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.1.1/cubes/buffer.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write`

```python
write(data: bytes) → WriteBuffer
```

Appends data to buffer. 


