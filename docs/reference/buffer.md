<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `buffer`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CubesBufferError`
Rised when buffer can't be reader or created. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EmptyBufferError`
Raised when buffer is empty. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `InvalidLengthError`
Raised when packet length (VarInt) can't be readed. 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ReadBuffer`
Class for parsing data by types. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    conn: Union[AbstractPlayerConnection, AbstractClientConnection],
    data: bytes = b''
)
```






---

#### <kbd>property</kbd> angle

int: Angle. 

A rotation angle in steps of 1/256 of a full turn. 

---

#### <kbd>property</kbd> boolean

bool: Either False or True. 

---

#### <kbd>property</kbd> byte

int: Signed 8-bit integer. 

---

#### <kbd>property</kbd> connection

cubes.abc.Connection: Current connection. 

---

#### <kbd>property</kbd> data

bytes: Buffer data. 

---

#### <kbd>property</kbd> double

float: Signed 64-bit float. 

---

#### <kbd>property</kbd> entity_metadata

typing.Sequence[tuple[cubes.EntityMetadataType,             typing.Any]]: Entity Metadata. 

Miscellaneous information about an entity. More information:  https://wiki.vg/Entity_metadata#Entity_Metadata_Format 

---

#### <kbd>property</kbd> float

float: Signed 32-bit float. 

---

#### <kbd>property</kbd> identifier

tuple[str, str]: Identifier. 

Namespaced location in format `(namespace, location)`. 

---

#### <kbd>property</kbd> integer

int: Signed 32-bit integer. 

---

#### <kbd>property</kbd> long

int: Signed 64-bit integer. 

---

#### <kbd>property</kbd> nbt

cubes.nbt.Compound: Named Binary Tag. 

https://wiki.vg/NBT 

---

#### <kbd>property</kbd> short

int: Signed 16-bit integer. 

---

#### <kbd>property</kbd> slot

Optional[tuple[int, int, nbt.Compound]]: Slot data structure. 

https://wiki.vg/Slot_Data 

---

#### <kbd>property</kbd> string

str: UTF-8 string. 



**Note:**

> Max string length is 32767 (b'\xff\xff\x01') bytes — 3 bytes VarInt prefix. 

---

#### <kbd>property</kbd> unsigned_byte

int: Unsigned 8-bit integer. 

---

#### <kbd>property</kbd> unsigned_short

int: Unsigned 16-bit integer. 

---

#### <kbd>property</kbd> uuid

uuid.UUID: UUID. 

---

#### <kbd>property</kbd> varint

int: Variable-length integer. 

---

#### <kbd>property</kbd> varlong

int: Variable-length integer. 



---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_reader`

```python
from_reader(
    conn: Union[AbstractPlayerConnection, AbstractClientConnection],
    reader: StreamReader
) → AbstractReadBuffer
```

Creates a ReadBuffer instance from asyncio.StreamReader. 



**Note:**

> Max packet length is 2097151 (b'\xff\xff\x7f') bytes — 3 bytes VarInt prefix. 
>

**Raises:**
 
 - <b>`EmptyBufferError`</b>:  when buffer is empty 
 - <b>`InvalidLengthError`</b>:  when packet length (VarInt) can't be reader 



**Todo:**
 * implement compression 

---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read`

```python
read(length: Optional[int] = None) → bytes
```

Reads `length` bytes from buffer. 



**Note:**

> If `length` is `None` returns all buffer data from current position. 
>

**Args:**
 
 - <b>`length`</b>:  number of bytes to read 


---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/buffer.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WriteBuffer`
Class for serializing data by types. 


---

#### <kbd>property</kbd> data

bytes: Buffer data. 

---

#### <kbd>property</kbd> packed

bytes: Packed buffer data. 



**Todo:**
  * implement compression 




