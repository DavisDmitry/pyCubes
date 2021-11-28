import io

from cubes import nbt
from cubes.net.types_ import _abc, _mixins, _nbt, _simple, _var_length


class Slot(
    _mixins.BufferPackMixin[tuple[int, int, nbt.Compound | None] | None],
    _abc.AbstractType[tuple[int, int, nbt.Compound | None] | None],
):
    @classmethod
    def validate(cls, value: tuple[int, int, nbt.Compound | None] | None) -> None:
        if value is None:
            return
        item_id, count, tag = value
        _var_length.VarInt.validate(item_id)
        _simple.Byte.validate(count)
        if tag is None:
            return
        _nbt.NamedBinaryTag.validate(tag)

    @classmethod
    def unpack(cls, data: bytes) -> tuple[int, int, nbt.Compound | None] | None:
        return cls.from_buffer(io.BytesIO(data))

    def to_buffer(self, buffer: io.BytesIO) -> None:
        if self._value is None:
            _simple.Boolean(False).to_buffer(buffer)
            return
        _simple.Boolean(True).to_buffer(buffer)
        item_id, count, tag = self._value
        _var_length.VarInt(item_id).to_buffer(buffer)
        _simple.Byte(count).to_buffer(buffer)
        if tag is None:
            _simple.Boolean(False).to_buffer(buffer)
            return
        _nbt.NamedBinaryTag(tag).to_buffer(buffer)

    @classmethod
    def from_buffer(
        cls, buffer: io.BytesIO
    ) -> tuple[int, int, nbt.Compound | None] | None:
        is_present = _simple.Boolean.from_buffer(buffer)
        if not is_present:
            return None
        item_id = _var_length.VarInt.from_buffer(buffer)
        count = _simple.Byte.from_buffer(buffer)
        is_tag_present = buffer.read(1) != b"\x00"
        if not is_tag_present:
            return item_id, count, None
        buffer.seek(buffer.tell() - 1)
        tag = _nbt.NamedBinaryTag.from_buffer(buffer)
        return item_id, count, tag
