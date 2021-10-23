import asyncio
import struct
from typing import Optional


class EmptyBufferError(Exception):
    """Exception raising when buffer is empty."""


class _Buffer:
    # pylint: disable=R0903
    def __init__(self, data: bytes = b""):
        self._data = data

    @property
    def data(self) -> bytes:
        """Buffer data."""
        return self._data


class ReadBuffer(_Buffer):
    """Class for parsing data by types."""

    def __init__(self, data: bytes = b""):
        super().__init__(data=data)
        self._pos = 0

    @classmethod
    async def from_reader(cls, reader: asyncio.StreamReader) -> "ReadBuffer":
        r"""Creates a ReadBuffer instance from asyncio.StreamReader.

        Note:
            Packet length is 2097151 (b'\xff\xff\x7f') bytes — 3 bytes VarInt prefix.

        Raises:
            EmptyBufferError: when buffer is empty

        Todo:
            * implement compression
        """
        length = 0
        for index in range(3):
            byte = await reader.read(1)
            if byte == b"":
                raise EmptyBufferError
            byte = ord(byte)
            length |= (byte & 0x7F) << 7 * index
            if not byte & 0x80:
                break
        return cls(await reader.read(length))

    def read(self, length: Optional[int] = None) -> bytes:
        """Reads length bytes from buffer.

        Note:
            If length <= 0 or None returns all buffer data from current position.

        Args:
            length: number of bytes to read
        """
        if length:
            result = self._data[self._pos : self._pos + length]
            self._pos += length
        else:
            result = self._data[self._pos :]
        return result

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
            byte = self.read(1)
            byte = ord(byte)
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
            byte = self.read(1)
            byte = ord(byte)
            result |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        if result & (1 << 63):
            result -= 1 << 64
        return result


class WriteBuffer(_Buffer):
    """Class for serializing data by types."""

    @property
    def packed(self) -> bytes:
        """Packed buffer data.

        Todo:
            * implement compression
        """
        return self._encode_varint(len(self._data), 3) + self._data

    def write(self, data: bytes) -> "WriteBuffer":
        """Appends data to buffer."""
        self._data += data
        return self

    def pack_boolean(self, value: bool) -> "WriteBuffer":
        """Packs True or False."""
        return self.write(struct.pack("?", value))

    def pack_byte(self, value: int) -> "WriteBuffer":
        """Packs signed 8-bit integer."""
        return self.write(struct.pack("b", value))

    def pack_unsigned_byte(self, value: int) -> "WriteBuffer":
        """Packs unsigned 8-bit integer."""
        return self.write(struct.pack("B", value))

    def pack_short(self, value: int) -> "WriteBuffer":
        """Packs signed 16-bit integer."""
        return self.write(struct.pack(">h", value))

    def pack_unsigned_short(self, value: int) -> "WriteBuffer":
        """Packs unsigned 16-bit integer."""
        return self.write(struct.pack(">H", value))

    def pack_integer(self, value: int) -> "WriteBuffer":
        """Packs signed 32-bit integer."""
        return self.write(struct.pack(">i", value))

    def pack_long(self, value: int) -> "WriteBuffer":
        """Packs signed 64-bit integer."""
        return self.write(struct.pack(">q", value))

    def pack_float(self, value: float) -> "WriteBuffer":
        """Packs signed 32-bit float."""
        return self.write(struct.pack(">f", value))

    def pack_double(self, value: float) -> "WriteBuffer":
        """Packs signed 64-bit double."""
        return self.write(struct.pack(">d", value))

    def pack_string(self, value: str) -> "WriteBuffer":
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

    def pack_varint(self, value: int) -> "WriteBuffer":
        """Packs variable-length integer."""
        return self.write(self._encode_varint(value))

    def pack_varlong(self, value: int) -> "WriteBuffer":
        """Packs variable-length integer."""
        return self.write(self._encode_varlong(value))
