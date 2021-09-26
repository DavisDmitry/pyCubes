import asyncio
import json
import logging

from cubes import Buffer, Server, utils
from cubes.connection import CloseConnection, Connection, ConnectionStatus

CURRRENT_PROTOCOL_VERSION = 756


log = logging.getLogger(__name__)


async def process_handshake(packet: Buffer) -> None:
    conn = Connection.get_current()
    protocol = packet.unpack_varint()
    packet.unpack_string()
    packet.read(2)
    conn.status = intention = ConnectionStatus(packet.unpack_varint())
    if intention == ConnectionStatus.LOGIN and protocol != CURRRENT_PROTOCOL_VERSION:
        log.warning("Protocol version %i not implemented.", protocol)
        raise CloseConnection


async def process_legacy_ping(_) -> None:
    log.warning("Legacy ping not implemeted")
    raise CloseConnection


async def process_status(_) -> Buffer:
    return (
        Buffer()
        .pack_varint(0x00)
        .pack_string(
            json.dumps(
                {
                    "version": {
                        "name": "1.17.1",
                        "protocol": CURRRENT_PROTOCOL_VERSION,
                    },
                    "players": {"max": 0, "online": 0},
                    "description": {"text": "Test Server"},
                }
            )
        )
    )


async def process_status_ping(packet: Buffer) -> Buffer:
    return Buffer().pack_varint(0x01).write(packet.read(8))


async def process_login_start(packet: Buffer) -> Buffer:
    conn = Connection.get_current()
    player_name = packet.unpack_string()
    log.info("Player %s trying to login", player_name)
    uuid = utils.generate_uuid(player_name)
    conn.status = ConnectionStatus.PLAY
    await asyncio.sleep(10)
    await conn.send_packet(
        Buffer().pack_varint(0x02).write(uuid.bytes).pack_string(player_name)
    )
    await asyncio.sleep(10)
    return (
        Buffer()
        .pack_varint(0x1A)
        .pack_string(json.dumps({"text": "Playing not implemented =("}))
    )


def main() -> None:
    logging.basicConfig(level="DEBUG")
    server = Server("127.0.0.1", 25565)

    server.add_low_level_handler(ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
    server.add_low_level_handler(ConnectionStatus.HANDSHAKE, 0xFE, process_legacy_ping)
    server.add_low_level_handler(ConnectionStatus.STATUS, 0x00, process_status)
    server.add_low_level_handler(ConnectionStatus.STATUS, 0x01, process_status_ping)
    server.add_low_level_handler(ConnectionStatus.LOGIN, 0x00, process_login_start)

    server.run()


if __name__ == "__main__":
    main()
