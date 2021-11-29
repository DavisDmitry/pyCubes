import io
from typing import Iterator

import anyio
import anyio.abc
import pytest

from cubes import net

pytestmark = pytest.mark.anyio


_HOST = "127.0.0.1"
_PORT = 25560


@pytest.fixture
async def stats_server() -> Iterator[tuple[dict[str, bool], net.Server]]:
    stats = {"new_conn": False, "timeout": False, "close_conn": False}

    async def _process_new_conn(_):
        stats["new_conn"] = True

    async def _process_packet_receive_timeout(conn: net.Connection):
        stats["timeout"] = True
        await conn.close()

    async def _process_packet(conn: net.Connection, packet: io.BytesIO):
        await conn.send(packet)

    async def _process_close_conn(_, __):
        stats["close_conn"] = True

    server = net.Server(
        _process_new_conn,
        _process_packet_receive_timeout,
        _process_packet,
        _process_close_conn,
        packet_receive_timeout=0.25,
    )

    yield stats, server


async def test_server(stats_server: tuple[dict[str, bool], net.Server]):
    stats, server = stats_server
    data = b"\x01\x00"

    async with anyio.create_task_group() as task_group:
        await task_group.start(server.run, _HOST, _PORT)
        assert server.is_running

        async with await anyio.connect_tcp(_HOST, _PORT) as stream:
            await stream.send(data)
            assert await stream.receive() == data

        async with await anyio.connect_tcp(_HOST, _PORT):
            await anyio.sleep(0.5)

        task_group.cancel_scope.cancel()

    assert {"new_conn": True, "timeout": True, "close_conn": True} == stats


async def test_conn(stats_server: tuple[dict, net.Server]):
    _, server = stats_server
    async with anyio.create_task_group() as task_group:
        await task_group.start(server.run, _HOST, _PORT)
        assert server.is_running
        async with await anyio.connect_tcp(_HOST, _PORT) as stream:
            conn = net.Connection(stream)
            conn.status = net.ConnectionStatus.LOGIN
            assert conn.status == net.ConnectionStatus.LOGIN
            conn.remote_address
            conn.local_address
        task_group.cancel_scope.cancel()
