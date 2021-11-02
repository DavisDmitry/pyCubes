import enum
import uuid as _uuid


class ConnectionStatus(enum.IntEnum):
    # pylint: disable=C0115
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


class PlayerData:
    """Class for storing the most important player data."""

    def __init__(self, uuid: _uuid.UUID, name: str):
        self._uuid, self._name = uuid, name

    @property
    def uuid(self) -> _uuid.UUID:
        """Player UUID."""
        return self._uuid

    @property
    def name(self) -> str:
        """Player name."""
        return self._name

    def __eq__(self, other: "PlayerData") -> bool:
        return self.uuid == other.uuid and self.name == other.name

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(uuid={repr(self.uuid)}, name='{self.name}')"
