import asyncio
import json
import uuid
from typing import Iterator

import pytest

import cubes

_HOST = "127.0.0.1"
_PORT = 25565
_PROTOCOL = 756
_PLAYER_NAME = "_Smesharik_"
_CLOSE_CONN_REASON = "I hate u, player!"


pytestmark = pytest.mark.asyncio


@pytest.fixture
def app() -> cubes.Application:
    return cubes.Application(1, 1)


@pytest.fixture
async def server(app: cubes.Application) -> Iterator[tuple[str, int]]:
    host, port = _HOST, _PORT
    task = asyncio.create_task(app._run(host, port))
    await asyncio.sleep(0.001)
    try:
        yield host, port
    finally:
        task.cancel()


async def test_wait_packet(server: tuple[str, int]):
    conn = cubes.ClientConnection(*(await asyncio.open_connection(*server)), None)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(conn.wait_packet(), 1.005)


async def _login_close_conn(_, packet: cubes.ReadBuffer):
    packet.connection.status = cubes.ConnectionStatus.LOGIN
    raise cubes.CloseConnection(_CLOSE_CONN_REASON)


@pytest.fixture
async def login_close_conn_server(
    app: cubes.Application, server: tuple[str, int]
) -> tuple[str, int]:
    app.unhandled_packet_handler = _login_close_conn
    return server


async def test_login_close_conn(login_close_conn_server: tuple[str, int]):
    conn = cubes.ClientConnection(
        *(await asyncio.open_connection(*login_close_conn_server)), None
    )
    await conn.send_packet(cubes.WriteBuffer(b"\x00"))
    packet = await asyncio.wait_for(conn.wait_packet(), 1)
    assert packet.varint == 0x00
    assert packet.string == json.dumps({"text": _CLOSE_CONN_REASON})
    await asyncio.wait_for(conn.close(), 1)


async def _play_close_conn(_, packet: cubes.ReadBuffer):
    packet.connection.status = cubes.ConnectionStatus.PLAY
    raise cubes.CloseConnection(_CLOSE_CONN_REASON)


@pytest.fixture
async def play_close_conn_server(
    app: cubes.Application, server: tuple[str, int]
) -> tuple[str, int]:
    app.unhandled_packet_handler = _play_close_conn
    return server


async def test_play_close_conn(play_close_conn_server: tuple[str, int]):
    conn = cubes.ClientConnection(
        *(await asyncio.open_connection(*play_close_conn_server)), None
    )
    await asyncio.wait_for(conn.send_packet(cubes.WriteBuffer(b"\x00")), 1)
    packet = await asyncio.wait_for(conn.wait_packet(), 1)
    assert packet.varint == 0x1A
    assert packet.string == json.dumps({"text": _CLOSE_CONN_REASON})
    await asyncio.wait_for(conn.close(), 1)


async def _handshake(_, packet: cubes.ReadBuffer):
    packet.varint
    packet.string
    packet.unsigned_short
    packet.connection.status = cubes.ConnectionStatus(packet.varint)


async def _login_start(_, packet: cubes.ReadBuffer):
    player_name = packet.string
    await packet.connection.send_packet(
        cubes.WriteBuffer()
        .pack_varint(0x02)
        .write(uuid.uuid4().bytes)
        .pack_string(player_name)
    )


@pytest.fixture
async def server_login(
    app: cubes.Application, server: tuple[str, int]
) -> tuple[str, int]:
    app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, _handshake)
    app.add_low_level_handler(cubes.ConnectionStatus.LOGIN, 0x00, _login_start)
    return server


async def test_login(server_login: tuple[str, int]):
    conn = await asyncio.wait_for(
        cubes.ClientConnection.connect(*server_login, _PROTOCOL, _PLAYER_NAME), 1
    )
    await asyncio.wait_for(conn.close(), 1)


async def test_login_with_disconnect(login_close_conn_server: tuple[str, int]):
    with pytest.raises(cubes.DisconnectedByServerError):
        await asyncio.wait_for(
            cubes.ClientConnection.connect(
                *login_close_conn_server, _PROTOCOL, _PLAYER_NAME
            ),
            1,
        )


async def test_login_with_unexpected_packet(play_close_conn_server: tuple[str, int]):
    with pytest.raises(cubes.UnexpectedPacketError):
        await asyncio.wait_for(
            cubes.ClientConnection.connect(
                *play_close_conn_server, _PROTOCOL, _PLAYER_NAME
            ),
            1,
        )


async def _login_invalid_name(_, packet: cubes.ReadBuffer):
    await packet.connection.send_packet(
        cubes.WriteBuffer()
        .pack_varint(0x02)
        .write(uuid.uuid4().bytes)
        .pack_string("invalid name")
    )


@pytest.fixture
async def login_invalid_name_server(
    app: cubes.Application, server: tuple[str, int]
) -> tuple[str, int]:
    app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, _handshake)
    app.add_low_level_handler(cubes.ConnectionStatus.LOGIN, 0x00, _login_invalid_name)
    return server


async def test_invalid_player_name(login_invalid_name_server: tuple[str, int]):
    with pytest.raises(cubes.InvalidPlayerNameError):
        await asyncio.wait_for(
            cubes.ClientConnection.connect(
                *login_invalid_name_server, _PROTOCOL, _PLAYER_NAME
            ),
            1,
        )
