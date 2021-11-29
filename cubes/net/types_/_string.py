import io

from cubes.net.types_ import _abc, _var_length

_MAX_STRING_LENGTH = 131068


class String(_abc.AbstractType[str]):
    @classmethod
    def validate(cls, value: str) -> None:
        if len(str(value)) > _MAX_STRING_LENGTH:
            raise ValueError

    def pack(self) -> bytes:
        return _var_length.VarInt(len(self._value)).pack() + self._value.encode()

    @classmethod
    def unpack(cls, data: bytes) -> str:
        buffer = io.BytesIO(data)
        buffer.seek(0)
        return cls.from_buffer(buffer)

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.pack())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> str:
        length = _var_length.VarInt.from_buffer(buffer)
        if length > _MAX_STRING_LENGTH:
            raise ValueError
        return buffer.read(length).decode()


class Identifier(String):
    pass
