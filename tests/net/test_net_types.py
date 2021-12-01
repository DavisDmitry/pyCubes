import io
import random
import string
import uuid

import nbtlib
import pytest

from cubes import nbt
from cubes.net import types_
from cubes.net.types_ import _string


@pytest.fixture
def buffer() -> io.BytesIO:
    return io.BytesIO()


def test_valid_nbt(buffer: io.BytesIO):
    with open("tests/data/test_data.snbt", "r") as file:
        value = nbtlib.parse_nbt(file.read())
    data = types_.NamedBinaryTag(value).pack()
    assert types_.NamedBinaryTag.unpack(data) == value
    types_.NamedBinaryTag(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.NamedBinaryTag.from_buffer(buffer) == value


def test_invalid_nbt():
    with pytest.raises(ValueError):
        types_.NamedBinaryTag("test")


@pytest.mark.parametrize(
    ("x", "y", "z"),
    ((-30000000, -2048, -30000000), (0, 0, 0), (30000000, 2047, 30000000)),
)
def test_valid_position(buffer: io.BytesIO, x: int, y: int, z: int):
    data = types_.Position(x, y, z).pack()
    assert types_.Position.unpack(data) == (x, y, z)
    types_.Position(x, y, z).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Position.from_buffer(buffer) == (x, y, z)


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
        types_.Position(x, y, z)


@pytest.mark.parametrize("value", (True, False, 0, 1, "test"))
def test_boolean(buffer: io.BytesIO, value):
    data = types_.Boolean(value).pack()
    assert types_.Boolean.unpack(data) is bool(value)
    types_.Boolean(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Boolean.from_buffer(buffer) is bool(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.Byte._RANGE[0],
        types_.Byte._RANGE[1],
        *[random.randint(*types_.Byte._RANGE) for _ in range(3)],
    ),
)
def test_valid_byte(buffer: io.BytesIO, value: int):
    data = types_.Byte(value).pack()
    assert types_.Byte.unpack(data) == value
    types_.Byte(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Byte.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value", (types_.Byte._RANGE[0] - 1, types_.Byte._RANGE[1] + 1, "test")
)
def test_invalid_byte(value):
    with pytest.raises(ValueError):
        types_.Byte.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.Int._RANGE[0],
        types_.Int._RANGE[1],
        *[random.randint(*types_.Int._RANGE) for _ in range(3)],
    ),
)
def test_valid_int(buffer: io.BytesIO, value: int):
    data = types_.Int(value).pack()
    assert types_.Int.unpack(data) == value
    types_.Int(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Int.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value", (types_.Int._RANGE[0] - 1, types_.Int._RANGE[1] + 1, "test")
)
def test_invalid_int(value):
    with pytest.raises(ValueError):
        types_.Int.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.Long._RANGE[0],
        types_.Long._RANGE[1],
        *[random.randint(*types_.Long._RANGE) for _ in range(3)],
    ),
)
def test_valid_long(buffer: io.BytesIO, value: int):
    data = types_.Long(value).pack()
    assert types_.Long.unpack(data) == value
    types_.Long(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Long.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value", (types_.Long._RANGE[0] - 1, types_.Long._RANGE[1] + 1, "test")
)
def test_invalid_long(value):
    with pytest.raises(ValueError):
        types_.Long.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.Short._RANGE[0],
        types_.Short._RANGE[1],
        *[random.randint(*types_.Short._RANGE) for _ in range(3)],
    ),
)
def test_valid_short(buffer: io.BytesIO, value: int):
    data = types_.Short(value).pack()
    assert types_.Short.unpack(data) == value
    types_.Short(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Short.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value", (types_.Short._RANGE[0] - 1, types_.Short._RANGE[1] + 1, "test")
)
def test_invalid_short(value):
    with pytest.raises(ValueError):
        types_.Short.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.UnsignedByte._RANGE[0],
        types_.UnsignedByte._RANGE[1],
        *[random.randint(*types_.UnsignedByte._RANGE) for _ in range(3)],
    ),
)
def test_valid_unsigned_byte(buffer: io.BytesIO, value: int):
    data = types_.UnsignedByte(value).pack()
    assert types_.UnsignedByte.unpack(data) == value
    types_.UnsignedByte(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.UnsignedByte.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (
        types_.Angle._RANGE[0],
        types_.Angle._RANGE[1],
        types_.Angle._RANGE[0] - 1,
        types_.Angle._RANGE[1] + 1,
    ),
)
def test_angle(value: int):
    value = types_.Angle(value)._value
    assert types_.Angle._RANGE[0] <= value <= types_.Angle._RANGE[1]


@pytest.mark.parametrize(
    "value",
    (types_.UnsignedByte._RANGE[0] - 1, types_.UnsignedByte._RANGE[1] + 1, "test"),
)
def test_invalid_unsigned_byte(value):
    with pytest.raises(ValueError):
        types_.UnsignedByte.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.UnsignedShort._RANGE[0],
        types_.UnsignedShort._RANGE[1],
        *[random.randint(*types_.UnsignedShort._RANGE) for _ in range(3)],
    ),
)
def test_valid_unsigned_short(buffer: io.BytesIO, value: int):
    data = types_.UnsignedShort(value).pack()
    assert types_.UnsignedShort.unpack(data) == value
    types_.UnsignedShort(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.UnsignedShort.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value",
    (types_.UnsignedShort._RANGE[0] - 1, types_.UnsignedShort._RANGE[1] + 1, "test"),
)
def test_invalid_unsigned_short(value):
    with pytest.raises(ValueError):
        types_.UnsignedShort.validate(value)


def test_valid_uuid(buffer: io.BytesIO):
    value = uuid.uuid4()
    data = types_.UUID(value).pack()
    assert types_.UUID.unpack(data) == value
    types_.UUID(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.UUID.from_buffer(buffer) == value


def test_invalid_uuid():
    with pytest.raises(ValueError):
        types_.UUID("test")


@pytest.mark.parametrize(
    "value",
    (
        types_.VarInt._RANGE[0],
        types_.VarInt._RANGE[1],
        *[random.randint(*types_.VarInt._RANGE) for _ in range(3)],
    ),
)
def test_valid_varint(buffer: io.BytesIO, value: int):
    data = types_.VarInt(value).pack()
    assert types_.VarInt.unpack(data) == value
    types_.VarInt(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.VarInt.from_buffer(buffer) == value


class _FakeStream(io.BytesIO):
    async def receive(self, max_bytes: int = 65536) -> bytes:
        return self.read(max_bytes)


@pytest.mark.anyio()
@pytest.mark.parametrize(
    "value",
    (
        types_.VarInt._RANGE[0],
        types_.VarInt._RANGE[1],
        *[random.randint(*types_.VarInt._RANGE) for _ in range(3)],
    ),
)
async def test_valid_varint_async(value: int):
    stream = _FakeStream()
    types_.VarInt(value).to_buffer(stream)
    stream.seek(0)
    assert await types_.VarInt.from_stream(stream) == value


@pytest.mark.parametrize(
    "value", (types_.VarInt._RANGE[0] - 1, types_.VarInt._RANGE[1] + 1, "test")
)
def test_invalid_varint(value):
    with pytest.raises(ValueError):
        types_.VarInt.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        types_.VarLong._RANGE[0],
        types_.VarLong._RANGE[1],
        *[random.randint(*types_.VarLong._RANGE) for _ in range(3)],
    ),
)
def test_valid_varlong(buffer: io.BytesIO, value: int):
    data = types_.VarLong(value).pack()
    assert types_.VarLong.unpack(data) == value
    types_.VarLong(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.VarLong.from_buffer(buffer) == value


@pytest.mark.parametrize(
    "value", (types_.VarLong._RANGE[0] - 1, types_.VarLong._RANGE[1] + 1, "test")
)
def test_invalid_varlong(value):
    with pytest.raises(ValueError):
        types_.VarLong.validate(value)


@pytest.mark.parametrize(
    "value", ((1, 64, None), (276, 1, nbt.Compound({"Name": nbt.String("test")})), None)
)
def test_slot(buffer: io.BytesIO, value: tuple[int, int, nbt.Compound] | None):
    data = types_.Slot(value).pack()
    assert types_.Slot.unpack(data) == value
    types_.Slot(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.Slot.from_buffer(buffer) == value


def test_valid_string(buffer: io.BytesIO):
    value = "test"
    data = types_.String(value).pack()
    assert types_.String.unpack(data) == value
    types_.String(value).to_buffer(buffer)
    buffer.seek(0)
    assert types_.String.from_buffer(buffer) == value


def test_invalid_string():
    value = "".join(
        random.choices(
            string.ascii_letters + string.digits, k=_string._MAX_STRING_LENGTH + 1
        )
    )
    with pytest.raises(ValueError):
        types_.String(value)


def test_invalid_string_from_buffer(buffer: io.BytesIO):
    data = random.randbytes(_string._MAX_STRING_LENGTH + 1)
    types_.VarInt(len(data)).to_buffer(buffer)
    buffer.write(data)
    buffer.seek(0)
    with pytest.raises(ValueError):
        types_.String.from_buffer(buffer)
