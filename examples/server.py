import enum
import io
import json
import logging
import signal

import anyio
import anyio.abc

from cubes import net
from cubes.net import serializers

_VERSION = "1.20.5-1.20.6"
_PROTOCOL = 766
_SERVER_DESCRIPTION = "Example server"


class ConnectionState(enum.IntEnum):
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    TRANSFER = 3
    CONFIGURATION = 4
    PLAY = 5


CONNECTION_STATES: dict[net.Connection, ConnectionState] = {}


async def process_handshake(conn: net.Connection, packet: io.BytesIO):
    protocol = serializers.VarIntSerializer.from_buffer(packet)
    serializers.StringSerializer.from_buffer(packet)  # host
    serializers.UnsignedShortSerializer.from_buffer(packet)  # port
    CONNECTION_STATES[conn] = intention = ConnectionState(
        serializers.VarIntSerializer.from_buffer(packet)
    )
    if (
        intention in (ConnectionState.LOGIN, ConnectionState.TRANSFER)
        and protocol != _PROTOCOL
    ):
        disconnect_packet = io.BytesIO()
        serializers.VarIntSerializer(0).to_buffer(disconnect_packet)
        serializers.StringSerializer(
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
    serializers.VarIntSerializer(0).to_buffer(response)
    serializers.StringSerializer(
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
    await conn.close()


async def process_packet(conn: net.Connection, packet: io.BytesIO):
    state = CONNECTION_STATES[conn]
    packet_id = serializers.VarIntSerializer.from_buffer(packet)
    match (state, packet_id):
        case (ConnectionState.HANDSHAKE, 0x00):
            await process_handshake(conn, packet)
        case (ConnectionState.HANDSHAKE, 0xFE):
            await process_legacy_ping(conn)
        case (ConnectionState.STATUS, 0x00):
            await process_status(conn)
        case (ConnectionState.STATUS, 0x01):
            await process_status_ping(conn, packet)
        case _:
            pass


async def process_new_connection(conn: net.Connection):
    logging.info('"%s:%i" connected to server.', *conn.remote_address)
    CONNECTION_STATES[conn] = ConnectionState.HANDSHAKE


async def process_packet_receive_timeout(conn: net.Connection):
    if CONNECTION_STATES[conn] == ConnectionState.LOGIN:
        packet = io.BytesIO()
        serializers.VarIntSerializer(0x00).to_buffer(packet)
        serializers.StringSerializer(
            json.dumps({"translate": "disconnect.timeout"})
        ).to_buffer(packet)
        await conn.send(packet)
    await conn.close()


async def process_close_connection(conn: net.Connection, reason: Exception | None):
    logging.info(
        '"%s:%i" disconnected from server. Reason: %s.',
        *conn.remote_address,
        repr(reason),
    )
    del CONNECTION_STATES[conn]


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
    # you shoud use anyio to run the server
    # you can use trio or asyncio as backend
    anyio.run(main, backend="trio")
