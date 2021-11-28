import enum
import uuid as _uuid


class EntityMetadataType(enum.IntEnum):
    """Entity Metadata Type enumeration.

    BYTE, VARINT, FLOAT, STRING, CHAT, OPTCHAT, SLOT, BOOLEAN,
        ROTATION, POSITION, OPTPOSITION, DIRECTION, OPTUUID,
        OPTBLOCKID, NBT, PARTICLE, VILLAGER_DATA, OPTVARINT, POSE
    """

    BYTE = 0
    VARINT = 1
    FLOAT = 2
    STRING = 3
    CHAT = 4
    OPTCHAT = 5
    SLOT = 6
    BOOLEAN = 7
    ROTATION = 8
    POSITION = 9
    OPTPOSITION = 10
    DIRECTION = 11
    OPTUUID = 12
    OPTBLOCKID = 13
    NBT = 14
    PARTICLE = 15
    VILLAGER_DATA = 16
    DATA = 17
    OPTVARINT = 18
    POSE = 19


class PlayerData:
    """Class for storing the most important player data."""

    __slots__ = ("_uuid", "_name")

    def __init__(self, uuid: _uuid.UUID, name: str):
        self._uuid, self._name = uuid, name

    @property
    def uuid(self) -> _uuid.UUID:
        """uuid.UUID: Player UUID."""
        return self._uuid

    @property
    def name(self) -> str:
        """str: Player name."""
        return self._name

    def __eq__(self, other: "PlayerData") -> bool:
        return self.uuid == other.uuid and self.name == other.name

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(uuid={repr(self.uuid)}, name='{self.name}')"
