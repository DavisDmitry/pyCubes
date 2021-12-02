import io

from cubes.net.serializers import _abc, _mixins, _nbt, _simple, _var_length
from cubes.types_ import slot


class SlotSerializer(
    _mixins.BufferSerializeMixin[slot.Slot],
    _abc.AbstractSerializer[slot.Slot],
):
    @classmethod
    def validate(cls, value: slot.Slot) -> None:
        """"""

    @classmethod
    def deserialize(cls, data: bytes) -> slot.Slot | None:
        return cls.from_buffer(io.BytesIO(data))

    def to_buffer(self, buffer: io.BytesIO) -> None:
        _simple.BooleanSerializer(True, validate=False).to_buffer(buffer)
        _var_length.VarIntSerializer(self._value.item_id, validate=False).to_buffer(
            buffer
        )
        _simple.ByteSerializer(self._value.count, validate=False).to_buffer(buffer)
        if self._value.nbt is None:
            buffer.write(b"\x00")
            return
        _nbt.NBTSerializer(self._value.nbt, validate=False).to_buffer(buffer)

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> slot.Slot | None:
        is_present = _simple.BooleanSerializer.from_buffer(buffer)
        if not is_present:
            return None
        item_id = _var_length.VarIntSerializer.from_buffer(buffer)
        count = _simple.ByteSerializer.from_buffer(buffer)
        nbt = _nbt.NBTSerializer.from_buffer(buffer)
        return slot.Slot(item_id, count, nbt=nbt)
