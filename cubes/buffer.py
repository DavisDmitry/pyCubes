import asyncio
from typing import Optional

from cubes import abc


class CubesBufferError(Exception):
    """Rised when buffer can't be reader or created."""


class EmptyBufferError(CubesBufferError):
    """Raised when buffer is empty."""


class InvalidLengthError(CubesBufferError):
    """Raised when packet length (VarInt) can't be readed."""


class ReadBuffer(abc.AbstractReadBuffer):
    """Class for parsing data by types."""

    def __init__(self, conn: abc.AbstractConnection, data: bytes = b""):
        super().__init__(conn, data)
        self._pos = 0

    @classmethod
    async def from_reader(
        cls, conn: abc.AbstractConnection, reader: asyncio.StreamReader
    ) -> abc.AbstractReadBuffer:
        r"""Creates a ReadBuffer instance from asyncio.StreamReader.

        Note:
            Max packet length is 2097151 (b'\xff\xff\x7f') bytes — 3 bytes
                VarInt prefix.

        Raises:
            EmptyBufferError: when buffer is empty
            InvalidLengthError: when packet length (VarInt) can't be reader

        Todo:
            * implement compression
        """
        length = 0
        for index in range(3):
            byte = await reader.read(1)
            if byte == b"":
                if index == 0:
                    raise EmptyBufferError
                raise InvalidLengthError
            byte = ord(byte)
            length |= (byte & 0x7F) << 7 * index
            if not byte & 0x80:
                break

        data = await reader.read(length)
        cur_len = length - len(data)
        while len(data) != length:
            await asyncio.sleep(0.001)
            chunk = await reader.read(cur_len)
            data += chunk
            cur_len -= len(chunk)
        return cls(conn, data)

    def read(self, length: Optional[int] = None) -> bytes:
        """Reads `length` bytes from buffer.

        Note:
            If `length` is `None` returns all buffer data from current position.

        Args:
            length: number of bytes to read
        """
        if length:
            result = self._data[self._pos : self._pos + length]
            self._pos += length
        else:
            result = self._data[self._pos :]
        return result


class WriteBuffer(abc.AbstractWriteBuffer):
    """Class for serializing data by types."""

    @property
    def packed(self) -> bytes:
        """bytes: Packed buffer data.

        Todo:
            * implement compression
        """
        return self._encode_varint(len(self._data), 3) + self._data
