import abc
import asyncio
import struct
import uuid
from typing import Any, Callable, Optional, Sequence, Union

from cubes import nbt, types_


class Application(abc.ABC):
    """Class for creating Minecraft Java Edition server implemetation."""

    __slots__ = ("_unhandled_packet_handler",)

    # pylint: disable=W0201
    @abc.abstractmethod
    def run(self, host: str, port: int = 25565) -> None:
        """Starts application."""

    @abc.abstractmethod
    def add_low_level_handler(
        self, conn_status: types_.ConnectionStatus, packet_id: int, func: Callable
    ) -> None:
        """Adds packet handler."""

    def _change_unhandled_packet_handler(self, func: Callable) -> None:
        self._unhandled_packet_handler = func

    unhandled_packet_handler = property(fset=_change_unhandled_packet_handler)


class _BaseBuffer:
    # pylint: disable=R0903
    __slots__ = ("_data",)

    def __init__(self, data: bytes = b""):
        self._data = data

    @property
    def data(self) -> bytes:
        """bytes: Buffer data."""
        return self._data


class AbstractReadBuffer(abc.ABC, _BaseBuffer):
    """Abstract class for parsing data by types."""

    __slots__ = ("_conn",)

    def __init__(self, conn: "AbstractConnection", data: bytes = b"") -> None:
        super().__init__(data)
        self._conn = conn

    @classmethod
    @abc.abstractmethod
    async def from_reader(
        cls, conn: "AbstractConnection", reader: asyncio.StreamReader
    ) -> "AbstractReadBuffer":
        """Creates a ReadBuffer instance from asyncio.StreamReader."""

    @abc.abstractmethod
    def read(self, length: Optional[int] = None) -> bytes:
        """Reads length bytes from buffer."""

    @property
    def connection(self) -> "AbstractConnection":
        """cubes.abc.Connection: Current connection."""
        return self._conn

    @property
    def boolean(self) -> bool:
        """bool: Either False or True."""
        return struct.unpack("?", self.read(1))[0]

    @property
    def byte(self) -> int:
        """int: Signed 8-bit integer."""
        return struct.unpack("b", self.read(1))[0]

    @property
    def unsigned_byte(self) -> int:
        """int: Unsigned 8-bit integer."""
        return struct.unpack("B", self.read(1))[0]

    @property
    def short(self) -> int:
        """int: Signed 16-bit integer."""
        return struct.unpack(">h", self.read(2))[0]

    @property
    def unsigned_short(self) -> int:
        """int: Unsigned 16-bit integer."""
        return struct.unpack(">H", self.read(2))[0]

    @property
    def integer(self) -> int:
        """int: Signed 32-bit integer."""
        return struct.unpack(">i", self.read(4))[0]

    @property
    def long(self) -> int:
        """int: Signed 64-bit integer."""
        return struct.unpack(">q", self.read(8))[0]

    @property
    def float(self) -> float:
        """float: Signed 32-bit float."""
        return struct.unpack(">f", self.read(4))[0]

    @property
    def double(self) -> float:
        """float: Signed 64-bit float."""
        return struct.unpack(">d", self.read(8))[0]

    @property
    def string(self) -> str:
        r"""str: UTF-8 string.

        Note:
            Max string length is 32767 (b'\xff\xff\x01') bytes —
                3 bytes VarInt prefix.
        """
        return self.read(self._unpack_varint(max_bytes=3)).decode()

    @property
    def identifier(self) -> tuple[str, str]:
        """tuple[str, str]: Identifier.

        Namespaced location in format `(namespace, location)`.
        """
        return tuple(self.string.split(":", 1))

    def _unpack_varint(self, max_bytes: int = 5) -> int:
        result = 0
        for i in range(max_bytes):
            byte = ord(self.read(1))
            result |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        if result & (1 << 31):
            result -= 1 << 32
        return result

    @property
    def varint(self) -> int:
        """int: Variable-length integer."""
        return self._unpack_varint()

    @property
    def varlong(self) -> int:
        """int: Variable-length integer."""
        result = 0
        for i in range(10):
            byte = ord(self.read(1))
            result |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        if result & (1 << 63):
            result -= 1 << 64
        return result

    @property
    def entity_metadata(self) -> Sequence[tuple[types_.EntitiMetadataType, Any]]:
        """typing.Sequence[tuple[cubes.EntityMetadataType, \
            typing.Any]]: Entity Metadata.

        Miscellaneous information about an entity. More information:
            https://wiki.vg/Entity_metadata#Entity_Metadata_Format

        Todo:
            * use match case in 3.10
        """
        # pylint: disable=R0912
        result = []
        next_index = self.unsigned_byte
        while next_index != 255:
            type_ = types_.EntitiMetadataType(self.varint)
            if type_ == types_.EntitiMetadataType.BYTE:
                data = self.byte
            elif type_ in (
                types_.EntitiMetadataType.VARINT,
                types_.EntitiMetadataType.DIRECTION,
            ):
                data = self.varint
            elif type_ == types_.EntitiMetadataType.FLOAT:
                data = self.float
            elif type_ in (
                types_.EntitiMetadataType.STRING,
                types_.EntitiMetadataType.CHAT,
                types_.EntitiMetadataType.POSE,
            ):
                data = self.string
            elif type_ == types_.EntitiMetadataType.OPTCHAT:
                data = self.boolean
                data = self.string if data else None
            elif type_ == types_.EntitiMetadataType.BOOLEAN:
                data = self.boolean
            elif type_ == types_.EntitiMetadataType.ROTATION:
                data = tuple(*[self.float for _ in range(3)])
            elif type_ == types_.EntitiMetadataType.OPTUUID:
                data = self.boolean
                data = self.uuid if data else None
            elif type_ == types_.EntitiMetadataType.OPTBLOCKID:
                data = self.boolean
                data = self.varint if data else None
            elif type_ == types_.EntitiMetadataType.NBT:
                data = self.nbt
            elif type_ == types_.EntitiMetadataType.VILLAGER_DATA:
                data = tuple(*[self.varint for _ in range(3)])
            elif type_ == types_.EntitiMetadataType.OPTVARINT:
                data = self.varint
                data = data - 1 if data != 0x00 else None
            else:
                raise NotImplementedError(
                    f"Unsupported Entity Metadata Type: {type_.value}."
                )

            result.append((type_, data))
            next_index = self.unsigned_byte

        return result

    @property
    def nbt(self) -> nbt.Compound:
        """cubes.nbt.Compound: Named Binary Tag.

        https://wiki.vg/NBT
        """
        return nbt.Compound.parse(self)

    @property
    def angle(self) -> int:
        """int: Angle.

        A rotation angle in steps of 1/256 of a full turn.
        """
        return self.unsigned_byte

    @property
    def uuid(self) -> uuid.UUID:
        """uuid.UUID: UUID."""
        return uuid.UUID(bytes=self.read(16))


class AbstractWriteBuffer(abc.ABC, _BaseBuffer):
    """Abstract class for serializing data by types."""

    @property
    @abc.abstractmethod
    def packed(self) -> bytes:
        """bytes: Packed buffer data."""

    def write(self, data: bytes) -> "AbstractWriteBuffer":
        """Appends data to buffer."""
        self._data += data
        return self

    def pack_boolean(self, value: bool) -> "AbstractWriteBuffer":
        """Packs True or False."""
        return self.write(struct.pack("?", value))

    def pack_byte(self, value: int) -> "AbstractWriteBuffer":
        """Packs signed 8-bit integer."""
        return self.write(struct.pack("b", value))

    def pack_unsigned_byte(self, value: int) -> "AbstractWriteBuffer":
        """Packs unsigned 8-bit integer."""
        return self.write(struct.pack("B", value))

    def pack_short(self, value: int) -> "AbstractWriteBuffer":
        """Packs signed 16-bit integer."""
        return self.write(struct.pack(">h", value))

    def pack_unsigned_short(self, value: int) -> "AbstractWriteBuffer":
        """Packs unsigned 16-bit integer."""
        return self.write(struct.pack(">H", value))

    def pack_integer(self, value: int) -> "AbstractWriteBuffer":
        """Packs signed 32-bit integer."""
        return self.write(struct.pack(">i", value))

    def pack_long(self, value: int) -> "AbstractWriteBuffer":
        """Packs signed 64-bit integer."""
        return self.write(struct.pack(">q", value))

    def pack_float(self, value: float) -> "AbstractWriteBuffer":
        """Packs signed 32-bit float."""
        return self.write(struct.pack(">f", value))

    def pack_double(self, value: float) -> "AbstractWriteBuffer":
        """Packs signed 64-bit double."""
        return self.write(struct.pack(">d", value))

    def pack_string(self, value: str) -> "AbstractWriteBuffer":
        """Packs UTF-8 string."""
        self.write(self._encode_varint(len(value), 3))
        return self.write(value.encode())

    def pack_identifier(self, namespace: str, location: str) -> "AbstractWriteBuffer":
        """Packs Identifier (namespaced location)."""
        return self.pack_string(f"{namespace}:{location}")

    @staticmethod
    def _encode_varint(value: int, max_bytes: int = 5) -> bytes:
        if value < 0:
            value += 1 << 32
        result = b""
        for _ in range(max_bytes):
            byte = value & 0x7F
            value >>= 7
            result += struct.pack("B", byte | (0x80 if value > 0 else 0))
            if value == 0:
                break
        return result

    @staticmethod
    def _encode_varlong(value: int) -> bytes:
        if value < 0:
            value += 1 << 64
        result = b""
        for _ in range(10):
            byte = value & 0x7F
            value >>= 7
            result += struct.pack("B", byte | (0x80 if value > 0 else 0))
            if value == 0:
                break
        return result

    def pack_varint(self, value: int) -> "AbstractWriteBuffer":
        """Packs variable-length integer."""
        return self.write(self._encode_varint(value))

    def pack_varlong(self, value: int) -> "AbstractWriteBuffer":
        """Packs variable-length integer."""
        return self.write(self._encode_varlong(value))

    def pack_entity_metadata(
        self, values: Sequence[tuple[types_.EntitiMetadataType, Any]]
    ) -> "AbstractWriteBuffer":
        """Packs Entity Metadata.

        https://wiki.vg/Entity_metadata#Entity_Metadata_Format

        Todo:
            * use match case in 3.10
        """
        # pylint: disable=R0912
        for index, (type_, value) in enumerate(values):
            type_: types_.EntitiMetadataType
            self.pack_unsigned_byte(index)
            self.pack_varint(type_.value)
            if type_ == types_.EntitiMetadataType.BYTE:
                self.pack_byte(value)
            elif type_ in (
                types_.EntitiMetadataType.VARINT,
                types_.EntitiMetadataType.DIRECTION,
                types_.EntitiMetadataType.POSE,
            ):
                self.pack_varint(value)
            elif type_ == types_.EntitiMetadataType.FLOAT:
                self.pack_float(value)
            elif type_ in (
                types_.EntitiMetadataType.STRING,
                types_.EntitiMetadataType.CHAT,
            ):
                self.pack_string(value)
            elif type_ == types_.EntitiMetadataType.OPTCHAT:
                if value is None:
                    self.pack_boolean(False)
                else:
                    self.pack_boolean(True)
                    self.pack_string(value)
            elif type_ == types_.EntitiMetadataType.BOOLEAN:
                self.pack_boolean(value)
            elif type_ == types_.EntitiMetadataType.ROTATION:
                value: tuple[float, float, float]
                for data in value:
                    self.pack_float(data)
            elif type_ == types_.EntitiMetadataType.OPTUUID:
                if value is None:
                    self.pack_boolean(False)
                else:
                    self.pack_boolean(True)
                    self.pack_uuid(value)
            elif type_ == types_.EntitiMetadataType.OPTBLOCKID:
                if value is None:
                    self.pack_boolean(False)
                else:
                    self.pack_boolean(True)
                    self.pack_varint(value)
            elif type_ == types_.EntitiMetadataType.NBT:
                self.pack_nbt(value)
            elif type_ == types_.EntitiMetadataType.VILLAGER_DATA:
                value: tuple[int, int, int]
                for data in value:
                    self.pack_varint(data)
            elif type_ == types_.EntitiMetadataType.OPTVARINT:
                if value is None:
                    self.pack_varint(0)
                else:
                    self.pack_varint(value + 1)
            else:
                raise NotImplementedError(
                    f"Unsupported Entity Metadata Type: {type_.value}."
                )

    def pack_nbt(self, value: nbt.Compound) -> "AbstractReadBuffer":
        """Packs NBT Tag."""
        value.write(self)
        return self

    def pack_angle(self, value: int) -> "AbstractWriteBuffer":
        """Packs Angle."""
        return self.pack_unsigned_byte(value)

    def pack_uuid(self, value: uuid.UUID) -> "AbstractWriteBuffer":
        """Packs UUID."""
        return self.write(value.bytes)


class _AbstractBaseConnection(abc.ABC):
    status: types_.ConnectionStatus

    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    __slots__ = ("status", "_reader", "_writer")

    @property
    def is_closing(self) -> bool:
        """bool: Is connection closing."""
        return self._writer.is_closing()

    @property
    def peername(self) -> tuple[str, int]:
        """tuple[str, int]: Client host and port."""
        return self._writer.get_extra_info("peername")

    @property
    def sockname(self) -> tuple[str, int]:
        """tuple[str, int]: Server host and port."""
        return self._writer.get_extra_info("sockname")

    @abc.abstractmethod
    async def read_packet(self) -> Optional[AbstractReadBuffer]:
        """Reads a packet."""

    @abc.abstractmethod
    async def wait_packet(self) -> AbstractReadBuffer:
        """Waits and reads a packet."""

    @abc.abstractmethod
    async def send_packet(self, buffer: AbstractWriteBuffer) -> None:
        """Sends packet."""


class AbstractPlayerConnection(_AbstractBaseConnection, abc.ABC):
    """Abstract player-to-server connection.

    Attributes:
        status (cubes.ConnectionStatus): Connection status
    """

    _app: Application

    __slots__ = ("_app",)

    @property
    def app(self) -> Application:
        """cubes.abc.AbstractApplication: Current application."""
        return self._app

    @abc.abstractmethod
    async def close(self, reason: Optional[str] = None) -> None:
        """Closes connection."""


class AbstractClientConnection(_AbstractBaseConnection, abc.ABC):
    """Abstract client connection.

    Attributes:
        status (cubes.ConnectionStatus): Connection status
    """

    _player: types_.PlayerData

    __slots__ = ("_player",)

    @property
    def player(self) -> types_.PlayerData:
        """cubes.PlayerData: Player data (UUID and name)."""
        return self._player

    @classmethod
    @abc.abstractmethod
    async def connect(
        cls, host: str, port: int, protocol: int, player_name: str
    ) -> "AbstractClientConnection":
        """Creates client connection."""

    @abc.abstractmethod
    async def close(self) -> None:
        """Closes connection."""


AbstractConnection = Union[AbstractPlayerConnection, AbstractClientConnection]
