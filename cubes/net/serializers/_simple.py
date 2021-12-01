import io
import struct

from cubes.net.serializers import _abc, _mixins


class _BaseSimpleSerializer(_abc.AbstractSerializer[_abc.T]):
    FMT: str

    def serialize(self) -> bytes:
        return struct.pack(f">{self.FMT}", self._value)

    @classmethod
    def deserialize(cls, data: bytes) -> _abc.T:
        value = struct.unpack(f">{cls.FMT}", data)[0]
        return value

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.serialize())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> _abc.T:
        size = struct.calcsize(f"{cls.FMT}")
        return cls.deserialize(buffer.read(size))


class _OneByteBaseType(_BaseSimpleSerializer[_abc.T]):
    def serialize(self) -> bytes:
        return struct.pack(self.FMT, self._value)

    @classmethod
    def deserialize(cls, data: bytes) -> _abc.T:
        return struct.unpack(cls.FMT, data)[0]


class BooleanSerializer(_mixins.StupidValidationMixin[bool], _OneByteBaseType[bool]):
    FMT = "?"
    _TYPE = bool


class ByteSerializer(_mixins.RangeValidationMixin[int], _OneByteBaseType[int]):
    FMT = "b"
    _TYPE = int
    _RANGE = (-128, 127)


class UnsignedByteSerializer(_mixins.RangeValidationMixin[int], _OneByteBaseType[int]):
    FMT = "B"
    _TYPE = int
    _RANGE = (0, 255)


class AngleSerializer(UnsignedByteSerializer):
    def __init__(self, value: int):
        if value > 255 or value < 0:
            value %= 255

        super().__init__(value)


class ShortSerializer(_mixins.RangeValidationMixin[int], _BaseSimpleSerializer[int]):
    FMT = "h"
    _TYPE = int
    _RANGE = (-32678, 32767)


class UnsignedShortSerializer(
    _mixins.RangeValidationMixin[int], _BaseSimpleSerializer[int]
):
    FMT = "H"
    _TYPE = int
    _RANGE = (0, 65535)


class IntSerializer(_mixins.RangeValidationMixin[int], _BaseSimpleSerializer[int]):
    FMT = "i"
    _TYPE = int
    _RANGE = (-2147483648, 2147483647)


class LongSerializer(_mixins.RangeValidationMixin[int], _BaseSimpleSerializer[int]):
    FMT = "q"
    _TYPE = int
    _RANGE = (-9223372036854775808, 9223372036854775807)


class FloatSerializer(
    _mixins.StupidValidationMixin[float], _BaseSimpleSerializer[float]
):
    FMT = "f"
    _TYPE = float


class DoubleSerializer(
    _mixins.StupidValidationMixin[float], _BaseSimpleSerializer[float]
):
    FMT = "d"
    _TYPE = float
