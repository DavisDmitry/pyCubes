import io
import logging
import signal

try:
    # ujson available in fast extra (pip install pycubes[fast])
    import ujson as json
except ImportError:
    import json

import anyio
import anyio.abc

from cubes import net
from cubes.net import types_

_VERSION = "1.17.1"
_PROTOCOL = 756
_SERVER_DESCRIPTION = "Example server"


async def process_handshake(conn: net.Connection, packet: io.BytesIO):
    protocol = types_.VarInt.from_buffer(packet)
    types_.String.from_buffer(packet)  # host
    types_.UnsignedShort.from_buffer(packet)  # port
    conn.status = intention = net.ConnectionStatus(types_.VarInt.from_buffer(packet))
    if intention == net.ConnectionStatus.LOGIN and protocol != _PROTOCOL:
        disconnect_packet = io.BytesIO()
        types_.VarInt(0).to_buffer(disconnect_packet)
        types_.String(
            json.dumps(
                {
                    "translate": "disconnect.genericReason",
                    "with": [{"text": f'Unsupported protocol version "{protocol}".'}],
                }
            )
        ).to_buffer(disconnect_packet)
        await conn.send(disconnect_packet)
        await conn.close()


async def process_legacy_ping(conn: net.Connection):
    await conn.close()


async def process_status(conn: net.Connection):
    response = io.BytesIO()
    types_.VarInt(0).to_buffer(response)
    types_.String(
        json.dumps(
            {
                "version": {"name": _VERSION, "protocol": _PROTOCOL},
                "players": {"max": 0, "online": 0},
                "description": {"text": _SERVER_DESCRIPTION},
            }
        )
    ).to_buffer(response)
    await conn.send(response)


async def process_status_ping(conn: net.Connection, packet: io.BytesIO):
    packet.seek(0)
    await conn.send(packet)


async def process_packet(conn: net.Connection, packet: io.BytesIO):
    packet_id = types_.VarInt.from_buffer(packet)
    match (conn.status, packet_id):
        case (net.ConnectionStatus.HANDSHAKE, 0x00):
            await process_handshake(conn, packet)
        case (net.ConnectionStatus.HANDSHAKE, 0xFE):
            await process_legacy_ping(conn)
        case (net.ConnectionStatus.STATUS, 0x00):
            await process_status(conn)
        case (net.ConnectionStatus.STATUS, 0x01):
            await process_status_ping(conn, packet)
        case _:
            pass


async def process_new_connection(conn: net.Connection):
    logging.info('"%s:%i" connected to server.', *conn.remote_address)


async def process_packet_receive_timeout(conn: net.Connection):
    if conn.status == net.ConnectionStatus.LOGIN:
        packet = io.BytesIO()
        types_.VarInt(0x00).to_buffer(packet)
        types_.String(json.dumps({"translate": "disconnect.timeout"})).to_buffer(packet)
        await conn.send(packet)
    await conn.close()


async def process_close_connection(conn: net.Connection, reason: Exception):
    logging.info(
        '"%s:%i" disconnected from server. Reason: %s.',
        *conn.remote_address,
        repr(reason),
    )


async def sygnal_handler(scope: anyio.CancelScope):
    with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
        async for _ in signals:
            scope.cancel()


async def main():
    server = net.Server(
        process_new_connection,
        process_packet_receive_timeout,
        process_packet,
        process_close_connection,
        packet_receive_timeout=5,
    )
    async with anyio.create_task_group() as task_group:
        task_group.start_soon(sygnal_handler, task_group.cancel_scope)
        task_group.start_soon(server.run, "127.0.0.1", 25560)


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    # you shoud use anyio for run server
    # you can use trio or asyncio as backend
    anyio.run(main, backend="trio")
