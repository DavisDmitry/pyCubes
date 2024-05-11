import io
import struct

from cubes.net.serializers import _abc


class PositionSerializer(_abc.AbstractSerializer[tuple[int, int, int]]):
    # pylint: disable=C0103
    def __init__(self, x: int, y: int, z: int, *, validate: bool = True):
        super().__init__((x, y, z), validate=validate)

    @classmethod
    def validate(cls, value: tuple[int, int, int]) -> None:
        x, y, z = value
        if x > 30000000 or z > 30000000 or y > 2047:
            raise ValueError
        if x < -30000000 or z < -30000000 or y < -2048:
            raise ValueError

    @staticmethod
    def _to_twos_complement(num: int, bits: int) -> int:
        return num + (1 << bits) if num < 0 else num

    @staticmethod
    def _from_twos_complement(num: int, bits: int) -> int:
        if num & (1 << bits - 1) != 0:
            num -= 1 << bits
        return num

    def serialize(self) -> bytes:
        x, y, z = self._value
        value = sum(
            (
                self._to_twos_complement(x, 26) << 38,
                self._to_twos_complement(z, 26) << 12,
                self._to_twos_complement(y, 12),
            )
        )
        return struct.pack(">Q", value)

    @classmethod
    def deserialize(cls, data: bytes) -> tuple[int, int, int]:
        _data = struct.unpack(">Q", data)[0]
        x = cls._from_twos_complement(_data >> 38, 26)
        z = cls._from_twos_complement(_data >> 12 & 0x3FFFFFF, 26)
        y = cls._from_twos_complement(_data & 0xFFF, 12)
        return x, y, z

    def to_buffer(self, buffer: io.BytesIO) -> None:
        buffer.write(self.serialize())

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> tuple[int, int, int]:
        return cls.deserialize(buffer.read(struct.calcsize("Q")))
