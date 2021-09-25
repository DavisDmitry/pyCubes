import asyncio
import struct
from typing import Optional


class EmptyBuffer(Exception):
    pass


class Buffer:
    def __init__(self, data: bytes = b""):
        self._data, self._pos = data, 0

    @property
    def data(self) -> bytes:
        return self._data

    @property
    def packed(self) -> bytes:
        # TODO: implement compression
        return self.encode_varint(len(self._data)) + self._data

    def reset_pos(self) -> None:
        self._pos = 0

    @classmethod
    async def from_reader(
        cls, reader: asyncio.StreamReader, threshold: int = -1
    ) -> "Buffer":
        # TODO: implement compression
        length = 0
        for i in range(3):
            byte = await reader.read(1)
            if byte == b"":
                raise EmptyBuffer
            byte = byte[0]
            length |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        data = await reader.read(length)
        return cls(data)

    def read(self, length: Optional[int] = None) -> bytes:
        if length:
            result = self._data[self._pos : self._pos + length]
            self._pos += length
        else:
            result = self._data[self._pos]
        return result

    def write(self, data: bytes) -> "Buffer":
        self._data += data
        return self

    def unpack_varint(self) -> int:
        """
        https://wiki.vg/Protocol#VarInt_and_VarLong
        """
        result = 0
        for i in range(5):
            byte = self.read(1)
            if byte == b"":
                return result
            byte = byte[0]
            result |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        return result

    @staticmethod
    def encode_varint(value: int) -> bytes:
        """
        https://wiki.vg/Protocol#VarInt_and_VarLong
        """
        if value < 0:
            value += 1 << 32
        result = b""
        for _ in range(5):
            byte = value & 0x7F
            value >>= 7
            result += struct.pack(">B", byte | (0x80 if value > 0 else 0))
            if value == 0:
                break
        return result

    def pack_varint(self, value: int) -> "Buffer":
        """
        https://wiki.vg/Protocol#VarInt_and_VarLong
        """
        return self.write(self.encode_varint(value))

    def unpack_string(self) -> str:
        """
        Unpack string from https://wiki.vg/Protocol#Data_types
        """
        return self.read(self.unpack_varint()).decode()

    def pack_string(self, value: str) -> "Buffer":
        """
        Pack string from https://wiki.vg/Protocol#Data_types
        """
        self.pack_varint(len(value))
        return self.write(value.encode())
