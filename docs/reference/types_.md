<!-- markdownlint-disable -->

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/types_.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `types_`






---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/types_.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConnectionStatus`
Connection Status enumeration. 

HANDSHAKE, STATUS, LOGIN, PlAY 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/types_.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EntityMetadataType`
Entity Metadata Type enumeration. 

BYTE, VARINT, FLOAT, STRING, CHAT, OPTCHAT, SLOT, BOOLEAN,  ROTATION, POSITION, OPTPOSITION, DIRECTION, OPTUUID,  OPTBLOCKID, NBT, PARTICLE, VILLAGER_DATA, OPTVARINT, POSE 





---

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/types_.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PlayerData`
Class for storing the most important player data. 

<a href="https://github.com/DavisDmitry/pyCubes/tree/0.3.0/cubes/types_.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(uuid: UUID, name: str)
```






---

#### <kbd>property</kbd> name

str: Player name. 

---

#### <kbd>property</kbd> uuid

uuid.UUID: Player UUID. 




