import io
from typing import Any, Sequence

from cubes.net.serializers import (
    _abc,
    _mixins,
    _nbt,
    _particle,
    _position,
    _simple,
    _slot,
    _string,
    _uuid,
    _var_length,
)
from cubes.types_ import entity

_SERIALIZERS_MAP = {
    entity.FieldType.BYTE: _simple.ByteSerializer,
    entity.FieldType.VARINT: _var_length.VarIntSerializer,
    entity.FieldType.FLOAT: _simple.FloatSerializer,
    entity.FieldType.STRING: _string.StringSerializer,
    entity.FieldType.CHAT: _string.StringSerializer,
    entity.FieldType.OPT_CHAT: _string.StringSerializer,
    entity.FieldType.SLOT: _slot.SlotSerializer,
    entity.FieldType.BOOLEAN: _simple.BooleanSerializer,
    entity.FieldType.POSITION: _position.PositionSerializer,
    entity.FieldType.OPT_POSITION: _position.PositionSerializer,
    entity.FieldType.OPT_UUID: _uuid.UUIDSerializer,
    entity.FieldType.NBT: _nbt.NBTSerializer,
    entity.FieldType.PARTICLE: _particle.ParticleSerializer,
}


class EntityMetadataSerializer(
    _mixins.BufferSerializeMixin[Sequence[Any]],
    _abc.AbstractSerializer[Sequence[Any]],
):
    _type_map: list[entity.FieldType]
    _value: list[Any]

    __slots__ = ("_type_map",)

    def __init__(self, *values: tuple[entity.FieldType, Any]):
        self._type_map = []
        new_value = []
        for value in values:
            self.validate_one(*value)
            self._type_map.append(value[0])
            new_value.append(value[1])
        super().__init__(new_value, validate=False)

    @classmethod
    def validate(cls, *values: tuple[entity.FieldType, Any]) -> None:
        for value in values:
            cls.validate_one(*value)

    @classmethod
    def validate_one(cls, type_: entity.FieldType, value: Any) -> None:
        if type_.name.startswith("OPT_") and value is None:
            return
        serializer = _SERIALIZERS_MAP.get(type_)
        if serializer is not None:
            serializer.validate(value)
            return
        match type_:
            case entity.FieldType.ROTATION:
                cls.validate_rotation(value)
            case entity.FieldType.DIRECTION:
                entity.Direction(value)
            case entity.FieldType.VILLAGER_DATA:
                cls.validate_villager_data(value)
            case entity.FieldType.POSE:
                entity.Pose(value)
            case entity.FieldType.OPT_BLOCK_ID | entity.FieldType.OPT_VARINT:
                _var_length.VarIntSerializer.validate(value)

    @staticmethod
    def validate_rotation(value: tuple[float, float, float]) -> None:
        for val in value:
            _simple.FloatSerializer.validate(val)

    @staticmethod
    def validate_villager_data(
        value: tuple[entity.VillagerType, entity.VillagerProfession, int]
    ):
        type_, profession, level = value
        entity.VillagerType(type_)
        entity.VillagerProfession(profession)
        if 0 <= level <= 5:
            return
        raise ValueError

    @classmethod
    def deserialize(cls, data: bytes) -> Sequence[Any]:
        return cls.from_buffer(io.BytesIO(data))

    def to_buffer(self, buffer: io.BytesIO) -> None:
        for index in range(len(self._value)):
            self._to_buffer_one(index, buffer)
        buffer.write(b"\xff")

    def _to_buffer_one(self, index: int, buffer: io.BytesIO) -> None:
        type_, value = self._type_map[index], self._value[index]

        _simple.UnsignedByteSerializer(index).to_buffer(buffer)
        _var_length.VarIntSerializer(type_).to_buffer(buffer)

        if type_ in (
            entity.FieldType.OPT_CHAT,
            entity.FieldType.OPT_POSITION,
            entity.FieldType.OPT_UUID,
        ):
            if value is None:
                _simple.BooleanSerializer(False).to_buffer(buffer)
                return
            _simple.BooleanSerializer(True).to_buffer(buffer)

        if type_ == entity.FieldType.SLOT and value is None:
            _simple.BooleanSerializer(False).to_buffer(buffer)
            return

        if (
            type_ in (entity.FieldType.OPT_VARINT, entity.FieldType.OPT_BLOCK_ID)
            and value is None
        ):
            buffer.write(b"\x00")
            return

        # pylint: disable=C0103
        Serializer: type[_abc.AbstractSerializer] = _SERIALIZERS_MAP.get(type_)
        if Serializer is not None:
            if type_ in (entity.FieldType.POSITION, entity.FieldType.OPT_POSITION):
                Serializer(*value, validate=False).to_buffer(buffer)
                return
            Serializer(value, validate=False).to_buffer(buffer)
            return

        match type_:
            case entity.FieldType.ROTATION:
                self._sequence_to_buffer(_simple.FloatSerializer, value, buffer)
            case entity.FieldType.VILLAGER_DATA:
                self._sequence_to_buffer(_var_length.VarIntSerializer, value, buffer)
            case entity.FieldType.DIRECTION | entity.FieldType.POSE:
                _var_length.VarIntSerializer(value).to_buffer(buffer)
            case entity.FieldType.OPT_VARINT | entity.FieldType.OPT_BLOCK_ID:
                _var_length.VarIntSerializer(value + 1, validate=False).to_buffer(
                    buffer
                )

    @staticmethod
    def _sequence_to_buffer(
        Serializer: type[_abc.AbstractSerializer], value: Sequence, buffer: io.BytesIO
    ) -> None:
        # pylint: disable=C0103
        for val in value:
            Serializer(val, validate=False).to_buffer(buffer)

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> Sequence[Any]:
        result = []
        byte = buffer.read(1)
        while byte != b"\xff":
            type_ = entity.FieldType(_var_length.VarIntSerializer.from_buffer(buffer))
            result.append(cls._from_buffer_one(buffer, type_))
            byte = buffer.read(1)
        return result

    @classmethod
    def _from_buffer_one(cls, buffer: io.BytesIO, type_: entity.FieldType) -> Any:
        if type_ in (
            entity.FieldType.OPT_CHAT,
            entity.FieldType.OPT_POSITION,
            entity.FieldType.OPT_UUID,
        ):
            if not _simple.BooleanSerializer.from_buffer(buffer):
                return None

        if type_ in (entity.FieldType.OPT_VARINT, entity.FieldType.OPT_BLOCK_ID):
            value = _var_length.VarIntSerializer.from_buffer(buffer)
            if value == 0:
                return None
            return value - 1

        # pylint: disable=C0103
        Serializer: type[_abc.AbstractSerializer] = _SERIALIZERS_MAP.get(type_)
        if Serializer is not None:
            return Serializer.from_buffer(buffer)

        match type_:
            case entity.FieldType.ROTATION:
                value = cls._sequence_from_buffer(buffer, _simple.FloatSerializer, 3)
            case entity.FieldType.VILLAGER_DATA:
                value = cls._sequence_from_buffer(
                    buffer, _var_length.VarIntSerializer, 3
                )
                value[0] = entity.VillagerType(value[0])
                value[1] = entity.VillagerProfession(value[1])
            case entity.FieldType.DIRECTION:
                value = entity.Direction(
                    _var_length.VarIntSerializer.from_buffer(buffer)
                )
            case entity.FieldType.POSE:
                value = entity.Pose(_var_length.VarIntSerializer.from_buffer(buffer))
        return value

    @staticmethod
    def _sequence_from_buffer(
        buffer: io.BytesIO, Serializer: type[_abc.AbstractSerializer], count: int
    ) -> Sequence[Any]:
        # pylint: disable=C0103
        return [Serializer.from_buffer(buffer) for _ in range(count)]
