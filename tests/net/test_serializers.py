import io
import random
import string
import uuid

import anyio.abc
import nbtlib  # type: ignore
import pytest

from cubes.net import serializers
from cubes.net.serializers import _string


@pytest.fixture
def buffer() -> io.BytesIO:
    return io.BytesIO()


def test_valid_nbt(buffer: io.BytesIO):
    with open("tests/data/test_data.snbt", "r") as file:
        value = nbtlib.parse_nbt(file.read())
    serializers.NBTSerializer.validate(value)
    data = serializers.NBTSerializer(value).serialize()
    assert serializers.NBTSerializer.deserialize(data) == value
    serializers.NBTSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.NBTSerializer.from_buffer(buffer) == value


def test_invalid_nbt():
    with pytest.raises(ValueError):
        serializers.NBTSerializer("test")


@pytest.mark.parametrize(
    ("x", "y", "z"),
    ((-30000000, -2048, -30000000), (0, 0, 0), (30000000, 2047, 30000000)),
)
def test_valid_position(buffer: io.BytesIO, x: int, y: int, z: int):
    data = serializers.PositionSerializer(x, y, z).serialize()
    assert serializers.PositionSerializer.deserialize(data) == (x, y, z)
    serializers.PositionSerializer(x, y, z).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.PositionSerializer.from_buffer(buffer) == (x, y, z)


@pytest.mark.parametrize(
    ("x", "y", "z"),
    (
        (30000001, 0, 0),
        (0, 2048, 0),
        (0, 0, 30000001),
        (-30000001, 0, 0),
        (0, -2049, 0),
        (0, 0, -30000001),
    ),
)
def test_invalid_position(x: int, y: int, z: int):
    with pytest.raises(ValueError):
        serializers.PositionSerializer(x, y, z)


@pytest.mark.parametrize("value", (True, False, 0, 1, "test"))
def test_boolean(buffer: io.BytesIO, value):
    serializer = serializers.BooleanSerializer(value)
    assert serializer.value is value
    data = serializer.serialize()
    assert serializers.BooleanSerializer.deserialize(data) is bool(value)
    serializer.to_buffer(buffer)
    buffer.seek(0)
    assert serializers.BooleanSerializer.from_buffer(buffer) is bool(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.ByteSerializer._RANGE[0],
        serializers.ByteSerializer._RANGE[1],
        *[random.randint(*serializers.ByteSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_byte(buffer: io.BytesIO, value: int):
    data = serializers.ByteSerializer(value).serialize()
    assert serializers.ByteSerializer.deserialize(data) == value
    serializers.ByteSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.ByteSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.ByteSerializer._RANGE[0] - 1,
        serializers.ByteSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_byte(value):
    with pytest.raises(ValueError):
        serializers.ByteSerializer(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.IntSerializer._RANGE[0],
        serializers.IntSerializer._RANGE[1],
        *[random.randint(*serializers.IntSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_int(buffer: io.BytesIO, value: int):
    data = serializers.IntSerializer(value).serialize()
    assert serializers.IntSerializer.deserialize(data) == value
    serializers.IntSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.IntSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.IntSerializer._RANGE[0] - 1,
        serializers.IntSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_int(value):
    with pytest.raises(ValueError):
        serializers.IntSerializer(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.LongSerializer._RANGE[0],
        serializers.LongSerializer._RANGE[1],
        *[random.randint(*serializers.LongSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_long(buffer: io.BytesIO, value: int):
    data = serializers.LongSerializer(value).serialize()
    assert serializers.LongSerializer.deserialize(data) == value
    serializers.LongSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.LongSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.LongSerializer._RANGE[0] - 1,
        serializers.LongSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_long(value):
    with pytest.raises(ValueError):
        serializers.LongSerializer(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.ShortSerializer._RANGE[0],
        serializers.ShortSerializer._RANGE[1],
        *[random.randint(*serializers.ShortSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_short(buffer: io.BytesIO, value: int):
    data = serializers.ShortSerializer(value).serialize()
    assert serializers.ShortSerializer.deserialize(data) == value
    serializers.ShortSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.ShortSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.ShortSerializer._RANGE[0] - 1,
        serializers.ShortSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_short(value):
    with pytest.raises(ValueError):
        serializers.ShortSerializer(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.UnsignedByteSerializer._RANGE[0],
        serializers.UnsignedByteSerializer._RANGE[1],
        *[random.randint(*serializers.UnsignedByteSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_unsigned_byte(buffer: io.BytesIO, value: int):
    data = serializers.UnsignedByteSerializer(value).serialize()
    assert serializers.UnsignedByteSerializer.deserialize(data) == value
    serializers.UnsignedByteSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.UnsignedByteSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.AngleSerializer._RANGE[0],
        serializers.AngleSerializer._RANGE[1],
        serializers.AngleSerializer._RANGE[0] - 1,
        serializers.AngleSerializer._RANGE[1] + 1,
    ),
)
def test_angle(value: int):
    value = serializers.AngleSerializer(value)._value
    assert (
        serializers.AngleSerializer._RANGE[0]
        <= value
        <= serializers.AngleSerializer._RANGE[1]
    )


@pytest.mark.parametrize(
    "value",
    (
        serializers.UnsignedByteSerializer._RANGE[0] - 1,
        serializers.UnsignedByteSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_unsigned_byte(value):
    with pytest.raises(ValueError):
        serializers.UnsignedByteSerializer(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.UnsignedShortSerializer._RANGE[0],
        serializers.UnsignedShortSerializer._RANGE[1],
        *[
            random.randint(*serializers.UnsignedShortSerializer._RANGE)
            for _ in range(3)
        ],
    ),
)
def test_valid_unsigned_short(buffer: io.BytesIO, value: int):
    data = serializers.UnsignedShortSerializer(value).serialize()
    assert serializers.UnsignedShortSerializer.deserialize(data) == value
    serializers.UnsignedShortSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.UnsignedShortSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.UnsignedShortSerializer._RANGE[0] - 1,
        serializers.UnsignedShortSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_unsigned_short(value):
    with pytest.raises(ValueError):
        serializers.UnsignedShortSerializer(value)


def test_valid_uuid(buffer: io.BytesIO):
    value = uuid.uuid4()
    data = serializers.UUIDSerializer(value).serialize()
    assert serializers.UUIDSerializer.deserialize(data) == value
    serializers.UUIDSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.UUIDSerializer.from_buffer(buffer) == value


def test_invalid_uuid():
    with pytest.raises(ValueError):
        serializers.UUIDSerializer("test")


@pytest.mark.parametrize(
    "value",
    (
        serializers.VarIntSerializer._RANGE[0],
        serializers.VarIntSerializer._RANGE[1],
        *[random.randint(*serializers.VarIntSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_varint(buffer: io.BytesIO, value: int):
    data = serializers.VarIntSerializer(value).serialize()
    assert serializers.VarIntSerializer.deserialize(data) == value
    serializers.VarIntSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.VarIntSerializer.from_buffer(buffer) == value


class _FakeStream(anyio.abc.ByteReceiveStream):
    def __init__(self, stream: io.BytesIO):
        self._stream = stream

    async def receive(self, max_bytes: int = 65536) -> bytes:
        return self._stream.read(max_bytes)

    async def aclose(self) -> None:
        self._stream.close()


@pytest.mark.anyio()
@pytest.mark.parametrize(
    "value",
    (
        serializers.VarIntSerializer._RANGE[0],
        serializers.VarIntSerializer._RANGE[1],
        *[random.randint(*serializers.VarIntSerializer._RANGE) for _ in range(3)],
    ),
)
async def test_valid_varint_async(value: int):
    stream = io.BytesIO()
    serializers.VarIntSerializer(value).to_buffer(stream)
    stream.seek(0)
    assert await serializers.VarIntSerializer.from_stream(_FakeStream(stream)) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.VarIntSerializer._RANGE[0] - 1,
        serializers.VarIntSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_varint(value):
    with pytest.raises(ValueError):
        serializers.VarIntSerializer(value)


@pytest.mark.parametrize(
    "value",
    (
        serializers.VarLongSerializer._RANGE[0],
        serializers.VarLongSerializer._RANGE[1],
        *[random.randint(*serializers.VarLongSerializer._RANGE) for _ in range(3)],
    ),
)
def test_valid_varlong(buffer: io.BytesIO, value: int):
    data = serializers.VarLongSerializer(value).serialize()
    assert serializers.VarLongSerializer.deserialize(data) == value
    serializers.VarLongSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.VarLongSerializer.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        serializers.VarLongSerializer._RANGE[0] - 1,
        serializers.VarLongSerializer._RANGE[1] + 1,
        "test",
    ),
)
def test_invalid_varlong(value):
    with pytest.raises(ValueError):
        serializers.VarLongSerializer(value)


def test_valid_string(buffer: io.BytesIO):
    value = "test"
    data = serializers.StringSerializer(value).serialize()
    assert serializers.StringSerializer.deserialize(data) == value
    serializers.StringSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.StringSerializer.from_buffer(buffer) == value


def test_invalid_string():
    value = "".join(
        random.choices(
            string.ascii_letters + string.digits, k=_string._MAX_STRING_LENGTH + 1
        )
    )
    with pytest.raises(ValueError):
        serializers.StringSerializer(value)


def test_invalid_string_from_buffer(buffer: io.BytesIO):
    data = random.randbytes(_string._MAX_STRING_LENGTH + 1)
    serializers.VarIntSerializer(len(data)).to_buffer(buffer)
    buffer.write(data)
    buffer.seek(0)
    with pytest.raises(ValueError):
        serializers.StringSerializer.from_buffer(buffer)


def test_valid_identifier(buffer: io.BytesIO):
    value = "some:thing"
    data = serializers.IdentifierSerializer(value).serialize()
    assert serializers.IdentifierSerializer.deserialize(data) == value
    serializers.IdentifierSerializer(value).to_buffer(buffer)
    buffer.seek(0)
    assert serializers.IdentifierSerializer.from_buffer(buffer) == value


def test_invalid_identifier():
    with pytest.raises(ValueError):
        serializers.IdentifierSerializer("something")
