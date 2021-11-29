import io
import struct

from cubes.net.types_ import _abc, _mixins


class _BaseType(_abc.AbstractType[_abc.T]):
    FMT: str

    def pack(self) -> bytes:
        return struct.pack(f">{self.FMT}", self._value)

    @classmethod
    def unpack(cls, data: bytes) -> _abc.T:
        value = struct.unpack(f">{cls.FMT}", data)[0]
        cls.validate(value)
        return value

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.pack())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> _abc.T:
        size = struct.calcsize(f"{cls.FMT}")
        return cls.unpack(buffer.read(size))


class _OneByteBaseType(_BaseType[_abc.T]):
    def pack(self) -> bytes:
        return struct.pack(self.FMT, self._value)

    @classmethod
    def unpack(cls, data: bytes) -> _abc.T:
        value = struct.unpack(cls.FMT, data)[0]
        cls.validate(value)
        return value


class Boolean(_mixins.StupidValidationMixin[bool], _OneByteBaseType[bool]):
    FMT = "?"
    _TYPE = bool


class Byte(_mixins.RangeValidationMixin[int], _OneByteBaseType[int]):
    FMT = "b"
    _TYPE = int
    _RANGE = (-128, 127)


class UnsignedByte(_mixins.RangeValidationMixin[int], _OneByteBaseType[int]):
    FMT = "B"
    _TYPE = int
    _RANGE = (0, 255)


class Angle(UnsignedByte):
    def __init__(self, value: int):
        if value > 255 or value < 0:
            value %= 255

        super().__init__(value)


class Short(_mixins.RangeValidationMixin[int], _BaseType[int]):
    FMT = "h"
    _TYPE = int
    _RANGE = (-32678, 32767)


class UnsignedShort(_mixins.RangeValidationMixin[int], _BaseType[int]):
    FMT = "H"
    _TYPE = int
    _RANGE = (0, 65535)


class Int(_mixins.RangeValidationMixin[int], _BaseType[int]):
    FMT = "i"
    _TYPE = int
    _RANGE = (-2147483648, 2147483647)


class Long(_mixins.RangeValidationMixin[int], _BaseType[int]):
    FMT = "q"
    _TYPE = int
    _RANGE = (-9223372036854775808, 9223372036854775807)


class Float(_mixins.StupidValidationMixin[float], _BaseType[float]):
    FMT = "f"
    _TYPE = float


class Double(_mixins.StupidValidationMixin[float], _BaseType[float]):
    FMT = "d"
    _TYPE = float
