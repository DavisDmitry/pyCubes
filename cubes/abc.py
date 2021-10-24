import abc
import asyncio
import struct
from typing import Callable, Optional

from cubes import types


class Application(abc.ABC):
    """Class for creating Minecraft Java Edition server implemetation."""

    # pylint: disable=W0201

    def __init__(self, packet_read_timeout: int = 20):
        self._packet_read_timeout = packet_read_timeout

    @abc.abstractmethod
    def run(self, host: str, port: int = 25565) -> None:
        """Starts application."""

    @abc.abstractmethod
    def add_low_level_handler(
        self, conn_status: types.ConnectionStatus, packet_id: int, func: Callable
    ) -> None:
        """Adds packet handler."""

    def _change_unhandled_packet_handler(self, func: Callable) -> None:
        self._unhandled_packet_handler = func

    unhandled_packet_handler = property(fset=_change_unhandled_packet_handler)


class _BaseBuffer:
    # pylint: disable=R0903
    def __init__(self, data: bytes = b""):
        self._data = data

    @property
    def data(self) -> bytes:
        """Buffer data."""
        return self._data


class AbstractReadBuffer(abc.ABC, _BaseBuffer):
    """Abstract class for parsing data by types."""

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
        """Current connection."""
        return self._conn

    @property
    def boolean(self) -> bool:
        """Either False or True."""
        return struct.unpack("?", self.read(1))[0]

    @property
    def byte(self) -> int:
        """Signed 8-bit integer."""
        return struct.unpack("b", self.read(1))[0]

    @property
    def unsigned_byte(self) -> int:
        """Unsigned 8-bit integer."""
        return struct.unpack("B", self.read(1))[0]

    @property
    def short(self) -> int:
        """Signed 16-bit integer."""
        return struct.unpack(">h", self.read(2))[0]

    @property
    def unsigned_short(self) -> int:
        """Unsigned 16-bit integer."""
        return struct.unpack(">H", self.read(2))[0]

    @property
    def integer(self) -> int:
        """Signed 32-bit integer."""
        return struct.unpack(">i", self.read(4))[0]

    @property
    def long(self) -> int:
        """Signed 64-bit integer."""
        return struct.unpack(">q", self.read(8))[0]

    @property
    def float(self) -> float:
        """Signed 32-bit float."""
        return struct.unpack(">f", self.read(4))[0]

    @property
    def double(self) -> float:
        """Signed 64-bit float."""
        return struct.unpack(">d", self.read(8))[0]

    @property
    def string(self) -> str:
        r"""UTF-8 string.

        Note:
            Max string length is 32767 (b'\xff\xff\x01') bytes — 3 bytes VarInt prefix.
        """
        return self.read(self._unpack_varint(max_bytes=3)).decode()

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
        """Variable-length integer."""
        return self._unpack_varint()

    @property
    def varlong(self) -> int:
        """Variable-length integer."""
        result = 0
        for i in range(10):
            byte = ord(self.read(1))
            result |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        if result & (1 << 63):
            result -= 1 << 64
        return result


class AbstractWriteBuffer(abc.ABC, _BaseBuffer):
    """Abstract class for serializing data by types."""

    @property
    @abc.abstractmethod
    def packed(self) -> bytes:
        """Packed buffer data."""

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


class AbstractConnection(abc.ABC):
    """Abstract client or server connection."""

    status: types.ConnectionStatus

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        app: Application,
    ):
        self._reader, self._writer, self._app = reader, writer, app

    @property
    def app(self) -> Application:
        """Current application."""
        return self._app

    @property
    def is_closing(self) -> bool:
        """Is connection closing."""
        return self._writer.is_closing()

    @property
    def peername(self) -> tuple[str, int]:
        """Client host and port."""
        return self._writer.get_extra_info("peername")

    @property
    def sockname(self) -> tuple[str, int]:
        """Server host and port."""
        return self._writer.get_extra_info("sockname")

    @abc.abstractmethod
    async def close(self, reason: Optional[str] = None) -> None:
        """Closes connection."""

    @abc.abstractmethod
    async def read_packet(self) -> Optional[AbstractReadBuffer]:
        """Reads packet."""

    @abc.abstractmethod
    async def send_packet(self, _buffer: AbstractWriteBuffer) -> None:
        """Sends packet."""