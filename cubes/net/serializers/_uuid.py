import io
import uuid

from cubes.net.serializers import _abc


class UUIDSerializer(_abc.AbstractSerializer[uuid.UUID]):
    @classmethod
    def validate(cls, value: uuid.UUID) -> None:
        if not isinstance(value, uuid.UUID):
            raise ValueError

    def serialize(self) -> bytes:
        return self._value.bytes

    @classmethod
    def deserialize(cls, data: bytes) -> uuid.UUID:
        return uuid.UUID(bytes=data)

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.serialize())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> uuid.UUID:
        return cls.deserialize(buffer.read(16))
