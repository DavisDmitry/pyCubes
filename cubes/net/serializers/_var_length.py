import io
import struct

import anyio.abc

from cubes.net.serializers import _abc, _mixins


class _BaseVarSerializer(_abc.AbstractSerializer[int]):
    _BYTES_SHIFT: int
    _MAX_BYTES: int

    def serialize(self) -> bytes:
        value = self._value
        if value < 0:
            value += 1 << self._BYTES_SHIFT
        result = b""
        for _ in range(self._MAX_BYTES):
            byte = value & 0x7F
            value >>= 7
            result += struct.pack("B", byte | (0x80 if value > 0 else 0))
            if value == 0:
                break
        return result

    @classmethod
    def deserialize(cls, data: bytes) -> int:
        return cls.from_buffer(io.BytesIO(data))

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.serialize())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> int:
        result = 0
        for index in range(cls._MAX_BYTES):
            byte = ord(buffer.read(1))
            result |= (byte & 0x7F) << 7 * index
            if not byte & 0x80:
                break
        if result & (1 << (cls._BYTES_SHIFT - 1)):
            result -= 1 << cls._BYTES_SHIFT
        return result

    @classmethod
    async def from_stream(cls, buffer: anyio.abc.ByteReceiveStream) -> int:
        result = 0
        for index in range(cls._MAX_BYTES):
            byte = ord(await buffer.receive(1))
            result |= (byte & 0x7F) << 7 * index
            if not byte & 0x80:
                break
        if result & (1 << (cls._BYTES_SHIFT - 1)):
            result -= 1 << cls._BYTES_SHIFT
        return result


class VarIntSerializer(_BaseVarSerializer, _mixins.RangeValidationMixin[int]):
    _BYTES_SHIFT = 32
    _MAX_BYTES = 5
    _TYPE = int
    _RANGE = (-2147483648, 2147483647)


class VarLongSerializer(_BaseVarSerializer, _mixins.RangeValidationMixin[int]):
    _BYTES_SHIFT = 64
    _MAX_BYTES = 10
    _TYPE = int
    _RANGE = (-9223372036854775808, 9223372036854775807)
