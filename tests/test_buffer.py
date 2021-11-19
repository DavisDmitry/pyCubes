import asyncio
import random
import uuid

import nbtlib
import pytest

import cubes
import cubes.buffer

_MIN_BYTE, _MAX_BYTE = -128, 127
_MIN_UNSIGNED_BYTE, _MAX_UNSIGNED_BYTE = 0, 255
_MIN_SHORT, _MAX_SHORT = -32768, 32767
_MIN_UNSIGNED_SHORT, _MAX_UNSIGNED_SHORT = 0, 65535
_MIN_INT, _MAX_INT = -2147483648, 2147483647
_MIN_LONG, _MAX_LONG = -9223372036854775808, 9223372036854775807
_MIN_VARINT, _MAX_VARINT = -2147483648, 2147483647
_MIN_VARLONG, _MAX_VARLONG = -9223372036854775808, 9223372036854775807


def test_read_None():
    data = b"\x00\x01\x02"
    assert cubes.ReadBuffer(None, data).read() == data


@pytest.mark.parametrize("value", (True, False))
def test_boolean(value: bool):
    data = cubes.WriteBuffer().pack_boolean(value).data
    assert cubes.ReadBuffer(None, data).boolean == value


@pytest.mark.parametrize(
    "value",
    [_MIN_BYTE, _MAX_BYTE, *[random.randint(_MIN_BYTE, _MAX_BYTE) for _ in range(3)]],
)
def test_byte(value: int):
    data = cubes.WriteBuffer().pack_byte(value).data
    assert cubes.ReadBuffer(None, data).byte == value


@pytest.mark.parametrize(
    "value",
    [
        _MIN_UNSIGNED_BYTE,
        _MAX_UNSIGNED_BYTE,
        *[random.randint(_MIN_UNSIGNED_BYTE, _MAX_UNSIGNED_BYTE) for _ in range(3)],
    ],
)
def test_unsigned_byte(value: int):
    data = cubes.WriteBuffer().pack_unsigned_byte(value).data
    assert cubes.ReadBuffer(None, data).unsigned_byte == value


@pytest.mark.parametrize(
    "value",
    [
        _MIN_SHORT,
        _MAX_SHORT,
        *[random.randint(_MIN_SHORT, _MAX_SHORT) for _ in range(3)],
    ],
)
def test_short(value: int):
    data = cubes.WriteBuffer().pack_short(value).data
    assert cubes.ReadBuffer(None, data).short == value


@pytest.mark.parametrize(
    "value",
    [
        _MIN_UNSIGNED_SHORT,
        _MAX_UNSIGNED_SHORT,
        *[random.randint(_MIN_UNSIGNED_SHORT, _MAX_UNSIGNED_SHORT) for _ in range(3)],
    ],
)
def test_unsigned_short(value: int):
    data = cubes.WriteBuffer().pack_unsigned_short(value).data
    assert cubes.ReadBuffer(None, data).unsigned_short == value


@pytest.mark.parametrize(
    "value",
    [_MIN_INT, _MAX_INT, *[random.randint(_MIN_INT, _MAX_INT) for _ in range(3)]],
)
def test_integer(value: int):
    data = cubes.WriteBuffer().pack_integer(value).data
    assert cubes.ReadBuffer(None, data).integer == value


@pytest.mark.parametrize(
    "value",
    [_MIN_LONG, _MAX_LONG, *[random.randint(_MIN_LONG, _MAX_LONG) for _ in range(3)]],
)
def test_long(value: int):
    data = cubes.WriteBuffer().pack_long(value).data
    assert cubes.ReadBuffer(None, data).long == value


def test_string():
    string = "test"
    data = cubes.WriteBuffer().pack_string(string).data
    assert cubes.ReadBuffer(None, data).string == string


def test_identifier():
    identrifier = ("minecraft", "thing")
    data = cubes.WriteBuffer().pack_identifier(*identrifier).data
    assert cubes.ReadBuffer(None, data).string == "minecraft:thing"
    assert cubes.ReadBuffer(None, data).identifier == identrifier


@pytest.mark.parametrize(
    "value",
    [
        _MIN_VARINT,
        _MAX_VARINT,
        *[random.randint(_MIN_VARINT, _MAX_VARINT) for _ in range(3)],
    ],
)
def test_varint(value: int):
    data = cubes.WriteBuffer().pack_varint(value).data
    assert cubes.ReadBuffer(None, data).varint == value


@pytest.mark.parametrize(
    "value",
    [
        _MIN_VARLONG,
        _MAX_VARLONG,
        *[random.randint(_MIN_VARLONG, _MAX_VARLONG) for _ in range(3)],
    ],
)
def test_varlong(value: int):
    data = cubes.WriteBuffer().pack_varlong(value).data
    assert cubes.ReadBuffer(None, data).varlong == value


def test_nbt():
    tag = nbtlib.Compound(
        {
            "nested compound test": nbtlib.Compound(
                {
                    "egg": nbtlib.Compound(
                        {"name": nbtlib.String("Eggbert"), "value": nbtlib.Float(0.5)}
                    ),
                    "ham": nbtlib.Compound(
                        {"name": nbtlib.String("Hampus"), "value": nbtlib.Float(0.75)}
                    ),
                }
            ),
            "intTest": nbtlib.Int(2147483647),
            "byteTest": nbtlib.Byte(127),
            "stringTest": nbtlib.String(
                "HELLO WORLD THIS IS A TEST STRING \xc5\xc4\xd6!"
            ),
            "listTest (long)": nbtlib.List(
                (
                    nbtlib.Long(11),
                    nbtlib.Long(12),
                    nbtlib.Long(13),
                    nbtlib.Long(14),
                    nbtlib.Long(15),
                )
            ),
            "doubleTest": nbtlib.Double(0.49312871321823148),
            "floatTest": nbtlib.Float(0.49823147058486938),
            "longTest": nbtlib.Long(9223372036854775807),
            "listTest (compound)": nbtlib.List(
                (
                    nbtlib.Compound(
                        {
                            "created-on": nbtlib.Long(1264099775885),
                            "name": nbtlib.String("Compound tag #0"),
                        }
                    ),
                    nbtlib.Compound(
                        {
                            "created-on": nbtlib.Long(1264099775885),
                            "name": nbtlib.String("Compound tag #1"),
                        }
                    ),
                )
            ),
            "shortTest": nbtlib.Short(32767),
        }
    )
    data = cubes.WriteBuffer().pack_nbt(tag).data
    assert cubes.ReadBuffer(None, data).nbt == tag


@pytest.mark.parametrize(
    "value",
    [
        _MIN_UNSIGNED_BYTE,
        _MAX_UNSIGNED_BYTE,
        *[random.randint(_MIN_UNSIGNED_BYTE, _MAX_UNSIGNED_BYTE) for _ in range(3)],
    ],
)
def test_angle(value: int):
    data = cubes.WriteBuffer().pack_angle(value).data
    assert cubes.ReadBuffer(None, data).angle == value


def test_uuid():
    value = uuid.uuid4()
    data = cubes.WriteBuffer().pack_uuid(value).data
    assert cubes.ReadBuffer(None, data).uuid == value


class _FakeStreamReader:
    def __init__(self, data: bytes = b""):
        self._data, self._pos = data, 0

    async def read(self, n: int) -> bytes:
        result = self._data[self._pos : self._pos + n]
        self._pos += n
        return result


@pytest.mark.asyncio
async def test_pack_unpack():
    packet_id = 0x00
    string = "test"
    data = cubes.WriteBuffer().pack_varint(packet_id).pack_string(string).packed
    buff = await cubes.ReadBuffer.from_reader(None, _FakeStreamReader(data))
    assert buff.varint == packet_id
    assert buff.string == string


@pytest.mark.asyncio
async def test_pack_unpack_empty_buffer():
    with pytest.raises(cubes.buffer.EmptyBufferError):
        await cubes.ReadBuffer.from_reader(None, _FakeStreamReader())


@pytest.mark.asyncio
async def test_invalid_length_error():
    with pytest.raises(cubes.buffer.InvalidLengthError):
        await cubes.ReadBuffer.from_reader(None, _FakeStreamReader(b"\x80"))


@pytest.mark.asyncio
async def test_invalid_buffer():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(
            cubes.ReadBuffer.from_reader(None, _FakeStreamReader(b"\x01")), 0.5
        )
