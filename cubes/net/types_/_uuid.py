import io
import uuid

from cubes.net.types_ import _abc


class UUID(_abc.AbstractType[uuid.UUID]):
    @classmethod
    def validate(cls, value: uuid.UUID) -> None:
        if not isinstance(value, uuid.UUID):
            raise ValueError

    def pack(self) -> bytes:
        return self._value.bytes

    @classmethod
    def unpack(cls, data: bytes) -> uuid.UUID:
        return uuid.UUID(bytes=data)

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.pack())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> uuid.UUID:
        return cls.unpack(buffer.read(16))
