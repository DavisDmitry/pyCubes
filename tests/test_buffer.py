import random

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
    assert cubes.ReadBuffer(data).read() == data


@pytest.mark.parametrize("value", (True, False))
def test_boolean(value: bool):
    data = cubes.WriteBuffer().pack_boolean(value).data
    assert cubes.ReadBuffer(data).boolean == value


@pytest.mark.parametrize(
    "value",
    [_MIN_BYTE, _MAX_BYTE, *[random.randint(_MIN_BYTE, _MAX_BYTE) for _ in range(3)]],
)
def test_byte(value: int):
    data = cubes.WriteBuffer().pack_byte(value).data
    assert cubes.ReadBuffer(data).byte == value


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
    assert cubes.ReadBuffer(data).unsigned_byte == value


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
    assert cubes.ReadBuffer(data).short == value


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
    assert cubes.ReadBuffer(data).unsigned_short == value


@pytest.mark.parametrize(
    "value",
    [_MIN_INT, _MAX_INT, *[random.randint(_MIN_INT, _MAX_INT) for _ in range(3)]],
)
def test_int(value: int):
    data = cubes.WriteBuffer().pack_int(value).data
    assert cubes.ReadBuffer(data).int == value


@pytest.mark.parametrize(
    "value",
    [_MIN_LONG, _MAX_LONG, *[random.randint(_MIN_LONG, _MAX_LONG) for _ in range(3)]],
)
def test_long(value: int):
    data = cubes.WriteBuffer().pack_long(value).data
    assert cubes.ReadBuffer(data).long == value


def test_string():
    string = "test"
    data = cubes.WriteBuffer().pack_string(string).data
    assert cubes.ReadBuffer(data).string == string


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
    assert cubes.ReadBuffer(data).varint == value


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
    assert cubes.ReadBuffer(data).varlong == value


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
    buff = await cubes.ReadBuffer.from_reader(_FakeStreamReader(data))
    assert buff.varint == packet_id
    assert buff.string == string


@pytest.mark.asyncio
async def test_pack_unpack_empty_buffer():
    with pytest.raises(cubes.buffer.EmptyBufferError):
        await cubes.ReadBuffer.from_reader(_FakeStreamReader())
