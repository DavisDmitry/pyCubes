import io

from cubes.net.serializers import _abc, _mixins, _var_length

_MAX_STRING_LENGTH = 131068


class StringSerializer(_mixins.BufferSerializeMixin[str], _abc.AbstractSerializer[str]):
    @classmethod
    def validate(cls, value: str) -> None:
        if len(str(value)) > _MAX_STRING_LENGTH:
            raise ValueError

    @classmethod
    def deserialize(cls, data: bytes) -> str:
        buffer = io.BytesIO(data)
        buffer.seek(0)
        return cls.from_buffer(buffer)

    def to_buffer(self, buffer: io.BytesIO) -> None:
        value = self._value.encode()
        _var_length.VarIntSerializer(len(value)).to_buffer(buffer)
        buffer.write(value)

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> str:
        length = _var_length.VarIntSerializer.from_buffer(buffer)
        if length > _MAX_STRING_LENGTH:
            raise ValueError
        return buffer.read(length).decode()


class IdentifierSerializer(StringSerializer):
    @classmethod
    def validate(cls, value: str) -> None:
        super().validate(value)
        if ":" not in value:
            raise ValueError
