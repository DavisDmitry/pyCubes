import io

from cubes import nbt
from cubes.net.types_ import _abc, _mixins

_WRAPPER_PREFIX = b"\x0A\x00\x00"


class NamedBinaryTag(
    _mixins.BufferPackMixin[nbt.Compound], _abc.AbstractType[nbt.Compound]
):
    @classmethod
    def validate(cls, value: nbt.Compound) -> None:
        if not isinstance(value, nbt.Compound):
            raise ValueError

    @classmethod
    def unpack(cls, data: bytes) -> nbt.Compound:
        return cls.from_buffer(io.BytesIO(data))

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(_WRAPPER_PREFIX)
        self._value.write(buffer)

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> nbt.Compound:
        buffer.read(3)
        result = nbt.Compound.parse(buffer)
        cls.validate(result)
        return result
